#!/usr/bin/env python3
"""Behavior tests for opc helper scripts. Run: python3 test_opc_scripts.py"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent


def run(script: str, *args: str, cwd: Path | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True, text=True, cwd=cwd,
    )


class TestNextFeatureSlug(unittest.TestCase):
    def test_first_and_incrementing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            features = Path(tmp) / "docs/features"
            res = run("next_feature_slug.py", "Export Center!", "--features-dir", str(features))
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertEqual(res.stdout.strip(), "1-export-center")
            (features / "3-other").mkdir(parents=True)
            res = run("next_feature_slug.py", "export-center", "--features-dir", str(features))
            self.assertEqual(res.stdout.strip(), "4-export-center")

    def test_legacy_dir_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            features = Path(tmp) / "docs/features"
            (features / "export-center").mkdir(parents=True)
            res = run("next_feature_slug.py", "export-center", "--features-dir", str(features))
            self.assertEqual(res.returncode, 1)
            self.assertIn("legacy", res.stderr)


class TestLedger(unittest.TestCase):
    def test_append_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            entry = {"type": "gate", "gate": "prd", "status": "Approved", "rounds": 1}
            res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(entry))
            self.assertEqual(res.returncode, 0, res.stderr)
            data = json.loads(ledger.read_text().strip())
            self.assertIn("ts", data)
            res = run("opc_ledger.py", "summary", "--ledger", str(ledger))
            self.assertEqual(res.returncode, 0)
            self.assertIn("gate: 1", res.stdout)

    def test_rejects_bad_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            bad = [
                {"type": "nope"},
                {"type": "gate", "gate": "prd", "status": "Maybe"},
                {"type": "evidence", "ac": "AC-1", "label": "definitely passed"},
            ]
            for entry in bad:
                res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(entry))
                self.assertEqual(res.returncode, 1, f"accepted bad entry: {entry}")
            self.assertFalse(ledger.exists())

    def test_release_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            good = {"type": "release", "stage": "deploy-test", "result": "ok"}
            res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(good))
            self.assertEqual(res.returncode, 0, res.stderr)
            for bad in (
                {"type": "release", "stage": "nope", "result": "ok"},
                {"type": "release", "stage": "deploy-test", "result": "maybe"},
            ):
                res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(bad))
                self.assertEqual(res.returncode, 1, f"accepted bad entry: {bad}")

    def test_error_ledger_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "error-ledger.jsonl"
            good = {"symptom": "tz off", "tag": "stale-knowledge", "root_cause": "naive datetime"}
            res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(good))
            self.assertEqual(res.returncode, 0, res.stderr)
            bad = {"symptom": "x", "tag": "not-a-tag", "root_cause": "y"}
            res = run("opc_ledger.py", "append", "--ledger", str(ledger), "--json", json.dumps(bad))
            self.assertEqual(res.returncode, 1)


class TestReviewStatus(unittest.TestCase):
    def _write(self, tmp: str, body: str) -> Path:
        path = Path(tmp) / "prd-review.md"
        path.write_text(body, encoding="utf-8")
        return path

    def test_approved_and_issues(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "# r\n\n**Status:** Approved\nReviewed-SHA: prd.md abcdef1\n")
            res = run("parse_review_status.py", str(path))
            self.assertEqual((res.returncode, res.stdout.strip()), (0, "Approved"))
            path = self._write(tmp, "# r\n\n**Status:** Issues Found\n")
            res = run("parse_review_status.py", str(path))
            self.assertEqual((res.returncode, res.stdout.strip()), (3, "Issues Found"))

    def test_malformed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "no status here\n")
            self.assertEqual(run("parse_review_status.py", str(path)).returncode, 1)
            path = self._write(tmp, "**Status:** Approved\n**Status:** Issues Found\n")
            self.assertEqual(run("parse_review_status.py", str(path)).returncode, 1)

    def test_json_output(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = self._write(tmp, "**Status:** Approved\nReviewed-SHA: prd.md abcdef1\n")
            res = run("parse_review_status.py", str(path), "--json")
            data = json.loads(res.stdout)
            self.assertEqual(data["status"], "Approved")
            self.assertEqual(data["reviewed"][0]["path"], "prd.md")


class TestFreshness(unittest.TestCase):
    def test_fresh_and_stale(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            artifact = root / "prd.md"
            artifact.write_text("v1\n")
            sha = subprocess.run(
                ["git", "hash-object", "prd.md"], cwd=root, capture_output=True, text=True
            ).stdout.strip()
            review = root / "prd-review.md"
            review.write_text(f"**Status:** Approved\nReviewed-SHA: prd.md {sha}\n")
            res = run("check_freshness.py", str(review), "--repo-root", str(root))
            self.assertEqual(res.returncode, 0, res.stderr)
            artifact.write_text("v2 changed\n")
            res = run("check_freshness.py", str(review), "--repo-root", str(root))
            self.assertEqual(res.returncode, 1)
            self.assertIn("STALE", res.stderr)

    def test_missing_records(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review = Path(tmp) / "r.md"
            review.write_text("**Status:** Approved\n")
            res = run("check_freshness.py", str(review), "--repo-root", tmp)
            self.assertEqual(res.returncode, 1)


class TestRecurrence(unittest.TestCase):
    def test_detects_clusters(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "error-ledger.jsonl"
            records = [
                {"feature": "1-a", "symptom": "tz", "tag": "stale-knowledge",
                 "root_cause": "naive dt", "pattern": "datetime.now() without tz"},
                {"feature": "2-b", "symptom": "tz again", "tag": "stale-knowledge",
                 "root_cause": "naive dt", "pattern": "datetime.now()  WITHOUT tz"},
                {"feature": "2-b", "symptom": "one-off", "tag": "api-misuse",
                 "root_cause": "x", "pattern": "unique thing"},
            ]
            ledger.write_text("\n".join(json.dumps(r) for r in records) + "\n")
            res = run("recurrence_scan.py", str(ledger), "--json")
            clusters = json.loads(res.stdout)
            self.assertEqual(len(clusters), 1)
            self.assertEqual(clusters[0]["count"], 2)
            self.assertEqual(sorted(clusters[0]["features"]), ["1-a", "2-b"])


class TestGateChain(unittest.TestCase):
    def _feature(self, root: Path) -> Path:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        feature = root / "docs/features/1-export"
        (feature / "reviews").mkdir(parents=True)
        (feature / "demo").mkdir()
        for name in ("requirement.md", "prd.md", "technical.md", "acceptance.md"):
            (feature / name).write_text(f"content of {name}\n")

        def sha(rel: str) -> str:
            return subprocess.run(
                ["git", "hash-object", rel], cwd=root, capture_output=True, text=True
            ).stdout.strip()

        pairs = {
            "requirement-review.md": "docs/features/1-export/requirement.md",
            "demo-review.md": "docs/features/1-export/requirement.md",
            "prd-review.md": "docs/features/1-export/prd.md",
            "technical-review.md": "docs/features/1-export/technical.md",
            "e2e-review.md": "docs/features/1-export/acceptance.md",
        }
        for review, artifact in pairs.items():
            (feature / "reviews" / review).write_text(
                f"ok\n\n**Status:** Approved\nReviewed-SHA: {artifact} {sha(artifact)}\n"
            )
        return feature

    def test_intact_then_broken(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature = self._feature(root)
            res = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("INTACT", res.stdout)
            # stale artifact breaks the chain
            (feature / "prd.md").write_text("changed\n")
            res = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(res.returncode, 1)
            self.assertIn("stale", res.stderr)

    def test_missing_review_and_skip(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature = self._feature(root)
            (feature / "reviews/demo-review.md").unlink()
            res = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(res.returncode, 1)
            self.assertIn("missing review: demo-review.md", res.stderr)
            res = run("check_gate_chain.py", str(feature), "--repo-root", str(root), "--skip", "demo")
            self.assertEqual(res.returncode, 0, res.stderr)
            self.assertIn("SKIPPED", res.stdout)

    def test_contract_reviews_expected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            feature = self._feature(root)
            (feature / "contracts").mkdir()
            (feature / "contracts/C-01-export.md").write_text("c\n")
            res = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(res.returncode, 1)
            self.assertIn("impl-contract-review.md", res.stderr)
            self.assertIn("C-01-implementation-review.md", res.stderr)


class TestValidateArtifacts(unittest.TestCase):
    def test_prd(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            prd = Path(tmp) / "prd.md"
            prd.write_text(
                "# PRD\n\n## Decision Sheet\nstuff\n\n## Acceptance Criteria\n"
                "AC-1: exports finish under 5s\nAC-2: denied without role\n\n## Appendix\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(prd)).returncode, 0)
            prd.write_text("# PRD\n\nno sections\n")
            self.assertEqual(run("validate_artifacts.py", str(prd)).returncode, 1)

    def test_prd_ac_section_scoping_and_struck(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            prd = Path(tmp) / "prd.md"
            # AC-1 mentioned at line start in the appendix must not count as a duplicate definition
            prd.write_text(
                "# PRD\n\n## Decision Sheet\nstuff\n\n## Acceptance Criteria\n"
                "AC-1: exports finish under 5s\n~~AC-2: old behavior~~\nAC-3: new behavior\n\n"
                "## Appendix\nAC-1: is referenced here in prose\n"
            )
            res = run("validate_artifacts.py", str(prd))
            self.assertEqual(res.returncode, 0, res.stderr)
            # reusing a retired id as active is a finding
            prd.write_text(
                "# PRD\n\n## Decision Sheet\nstuff\n\n## Acceptance Criteria\n"
                "~~AC-1: retired~~\nAC-1: reused\n\n## Appendix\n"
            )
            res = run("validate_artifacts.py", str(prd))
            self.assertEqual(res.returncode, 1)
            self.assertIn("retired", res.stderr)

    def test_contract_ref_to_struck_ac_ok(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            contracts = Path(tmp) / "contracts"
            contracts.mkdir()
            prd = Path(tmp) / "prd.md"
            prd.write_text(
                "## Decision Sheet\nx\n\n## Acceptance Criteria\nAC-1: x\n~~AC-2: retired~~\n"
            )
            contract = contracts / "C-01-export.md"
            contract.write_text(
                "# C-01\n\n## Boundary\nACs owned: AC-1, AC-2\n\n## Internal Design\nd\n\n"
                "## TDD Seed\ns\n\n## Done Means\nm\n"
            )
            res = run("validate_artifacts.py", str(contract), "--prd", str(prd))
            self.assertEqual(res.returncode, 0, res.stderr)

    def test_technical_reversibility(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tech = Path(tmp) / "technical.md"
            # TD records as plain lines (per technical-format.md) and as headings both count
            tech.write_text(
                "# T\n\n## Decision Records\nTD-1: pick sqlite [two-way]\n  Context ...\n\n"
                "### TD-2: queue choice [ONE-WAY]\nok\n\n"
                "## Public Contracts\napi\n\n## Runtime Evidence Plan\nlogs\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(tech)).returncode, 0)
            tech.write_text(
                "# T\n\n## Decision Records\nTD-1: pick sqlite\nok\n\n"
                "## Public Contracts\napi\n\n## Runtime Evidence Plan\nlogs\n"
            )
            res = run("validate_artifacts.py", str(tech))
            self.assertEqual(res.returncode, 1)
            self.assertIn("reversibility", res.stderr)

    def test_contract_ac_cross_check(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            contracts = Path(tmp) / "contracts"
            contracts.mkdir()
            prd = Path(tmp) / "prd.md"
            prd.write_text("## Decision Sheet\n\n## Acceptance Criteria\nAC-1: x\n")
            contract = contracts / "C-01-export.md"
            contract.write_text(
                "# C-01\n\n## Boundary\nACs owned: AC-9\n\n## Internal Design\nd\n\n"
                "## TDD Seed\ns\n\n## Done Means\nm\n"
            )
            res = run("validate_artifacts.py", str(contract), "--prd", str(prd))
            self.assertEqual(res.returncode, 1)
            self.assertIn("AC-9", res.stderr)

    def test_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            review = Path(tmp) / "prd-review.md"
            review.write_text("**Status:** Approved\nReviewed-SHA: prd.md abcdef1\n")
            self.assertEqual(run("validate_artifacts.py", str(review)).returncode, 0)
            review.write_text("**Status:** Approved\n")
            res = run("validate_artifacts.py", str(review))
            self.assertEqual(res.returncode, 1)
            self.assertIn("Reviewed-SHA", res.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
