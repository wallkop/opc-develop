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

    def test_span_usage_delta_and_json_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            ledger = root / "ledger.jsonl"
            usage = root / "usage.json"
            usage.write_text(json.dumps({"session_id": "s1", "usage": {"input_tokens": 100, "output_tokens": 10, "total_tokens": 110}}))
            started = run("opc_ledger.py", "span-start", "--repo", str(root), "--ledger", str(ledger),
                          "--usage-source", "normalized", "--usage-input", str(usage),
                          "--json", json.dumps({"type": "gate", "gate": "prd", "status": "Approved", "rounds": 1}))
            self.assertEqual(started.returncode, 0, started.stderr)
            span = json.loads(started.stdout)["span_id"]
            usage.write_text(json.dumps({"session_id": "s1", "usage": {"input_tokens": 160, "output_tokens": 25, "total_tokens": 185}}))
            ended = run("opc_ledger.py", "span-end", "--repo", str(root), "--span", span,
                        "--usage-source", "normalized", "--usage-input", str(usage), "--json", "{}")
            self.assertEqual(ended.returncode, 0, ended.stderr)
            entry = json.loads(ledger.read_text())
            self.assertEqual(entry["token_usage"]["total_tokens"], 75)
            self.assertIn("wall_secs", entry)
            summary = run("opc_ledger.py", "summary", "--ledger", str(ledger), "--json")
            self.assertEqual(json.loads(summary.stdout)["phases"]["prd"]["tokens"], 75)

    def test_v2_audit_rejects_missing_evidence_label(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            ledger.write_text(json.dumps({"schema_version": "opc-ledger-v2", "type": "evidence", "ac": "AC-1"}) + "\n")
            result = run("opc_ledger.py", "audit", "--ledger", str(ledger))
            self.assertEqual(result.returncode, 1)
            self.assertIn("evidence", result.stdout)


class TestUsage(unittest.TestCase):
    def test_codex_snapshot_uses_latest_cumulative_event(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            session = Path(tmp) / "rollout-thread-1.jsonl"
            session.write_text("\n".join([
                json.dumps({"type": "session_meta", "payload": {"session_id": "s1"}}),
                json.dumps({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 10, "output_tokens": 2, "total_tokens": 12}}}}),
                json.dumps({"type": "event_msg", "payload": {"type": "token_count", "info": {"total_token_usage": {"input_tokens": 20, "output_tokens": 5, "total_tokens": 25}}}}),
            ]) + "\n")
            code = ("from pathlib import Path; from opc_usage import read_codex_usage; "
                    f"import json; print(json.dumps(read_codex_usage(Path({str(session)!r}))))")
            proc = subprocess.run([sys.executable, "-c", code], cwd=SCRIPTS, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            self.assertEqual(json.loads(proc.stdout)["usage"]["total_tokens"], 25)


class TestBenchmark(unittest.TestCase):
    def _registry(self, root: Path, bad_command: list[str]) -> Path:
        registry = root / "registry.json"
        registry.write_text(json.dumps({"cases": [{
            "schema_version": "opc-benchmark-case-v1", "id": "OPC-TEST", "title": "detect bad variant",
            "provenance": {"source": "synthetic"}, "initial_state": {}, "task": {"instruction": "test"},
            "ground_truth": {"expected_detection_stage": "unit"},
            "profiles": [{"id": "fixture", "kind": "fixture", "fidelity": "fixture", "verification": {
                "good": {"command": [sys.executable, "-c", "raise SystemExit(0)"], "expected_exit": 0},
                "bad": {"command": bad_command, "expected_exit": 1}
            }}]
        }]}))
        return registry

    def test_green_red_green_and_html_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = self._registry(root, [sys.executable, "-c", "raise SystemExit(1)"])
            out = root / "out"
            result = run("opc_benchmark.py", "run", str(registry), "--repo", str(root), "--out", str(out))
            self.assertEqual(result.returncode, 0, result.stderr)
            report = json.loads((out / "report.json").read_text())
            self.assertTrue(report["runs"][0]["cleanup_ok"])
            self.assertTrue((out / "report.html").exists())

    def test_vacuous_bad_variant_fails_benchmark(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            registry = self._registry(root, [sys.executable, "-c", "raise SystemExit(0)"])
            result = run("opc_benchmark.py", "run", str(registry), "--repo", str(root))
            self.assertEqual(result.returncode, 1)

    def test_bundled_synthetic_incidents(self) -> None:
        registry = SCRIPTS.parent / "fixtures" / "opc-benchmark" / "registry.json"
        result = run("opc_benchmark.py", "run", str(registry), "--repo", str(SCRIPTS.parent.parent))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(json.loads(result.stdout)["runs"]), 3)

    def test_historical_refs_run_bad_and_good_in_temporary_worktrees(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"; repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "opc@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "OPC Test"], cwd=repo, check=True)
            check = repo / "check.py"; state = repo / "state.txt"
            check.write_text("from pathlib import Path\nraise SystemExit(0 if Path('state.txt').read_text() == 'good' else 1)\n")
            state.write_text("bad"); subprocess.run(["git", "add", "."], cwd=repo, check=True); subprocess.run(["git", "commit", "-qm", "bad"], cwd=repo, check=True)
            bad_ref = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
            state.write_text("good"); subprocess.run(["git", "commit", "-qam", "good"], cwd=repo, check=True)
            good_ref = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True, check=True).stdout.strip()
            registry = repo / "registry.json"
            registry.write_text(json.dumps({"cases": [{"schema_version": "opc-benchmark-case-v1", "id": "HIST", "title": "history", "provenance": {}, "initial_state": {}, "task": {}, "ground_truth": {}, "profiles": [{"id": "history", "kind": "historical_ref", "fidelity": "local_service", "good_ref": good_ref, "bad_ref": bad_ref, "verification": {"good": {"command": [sys.executable, "check.py"], "expected_exit": 0}, "bad": {"command": [sys.executable, "check.py"], "expected_exit": 1}}}]}]}))
            subprocess.run(["git", "add", "registry.json"], cwd=repo, check=True); subprocess.run(["git", "commit", "-qm", "registry"], cwd=repo, check=True)
            result = run("opc_benchmark.py", "run", str(registry), "--repo", str(repo))
            self.assertEqual(result.returncode, 0, result.stderr)
            worktrees = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=repo, capture_output=True, text=True, check=True).stdout
            self.assertEqual(worktrees.count("worktree "), 1)

    def test_mutation_patch_is_killed_and_restored(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"; repo.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.email", "opc@example.invalid"], cwd=repo, check=True)
            subprocess.run(["git", "config", "user.name", "OPC Test"], cwd=repo, check=True)
            (repo / "state.txt").write_text("good\n")
            (repo / "check.py").write_text("from pathlib import Path\nraise SystemExit(0 if Path('state.txt').read_text().strip() == 'good' else 1)\n")
            subprocess.run(["git", "add", "."], cwd=repo, check=True); subprocess.run(["git", "commit", "-qm", "good"], cwd=repo, check=True)
            (repo / "state.txt").write_text("bad\n")
            patch = subprocess.run(["git", "diff", "--", "state.txt"], cwd=repo, capture_output=True, text=True, check=True).stdout
            subprocess.run(["git", "checkout", "--", "state.txt"], cwd=repo, check=True)
            (repo / "mutation.patch").write_text(patch)
            registry = repo / "registry.json"
            registry.write_text(json.dumps({"cases": [{"schema_version": "opc-benchmark-case-v1", "id": "MUT", "title": "mutation", "provenance": {}, "initial_state": {}, "task": {}, "ground_truth": {}, "profiles": [{"id": "mutation", "kind": "mutation", "fidelity": "mutation", "patch": "mutation.patch", "verification": {"good": {"command": [sys.executable, "check.py"], "expected_exit": 0}, "bad": {"command": [sys.executable, "check.py"], "expected_exit": 1}}}]}]}))
            result = run("opc_benchmark.py", "run", str(registry), "--repo", str(repo))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual((repo / "state.txt").read_text(), "good\n")


class TestHumanReport(unittest.TestCase):
    def test_chinese_report_requires_plain_sections_and_term_annotation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); source = root / "retro.md"; output = root / "retro.html"
            terms = SCRIPTS.parent / "formats" / "report-terms.json"
            source.write_text("# 复盘\n\n## 结论\nGT 没通过。\n\n## 对用户意味着什么\n会漏问题。\n\n## 证据\n测试失败。\n\n## 下一步\n修复。\n")
            render = run("render_report.py", "render", str(source), "--out", str(output))
            self.assertEqual(render.returncode, 0, render.stderr)
            lint = run("render_report.py", "lint", str(source), "--html", str(output), "--terms", str(terms))
            self.assertEqual(lint.returncode, 1)
            self.assertIn("GT", lint.stdout)
            source.write_text(source.read_text().replace("GT 没通过", "GT（机器判定结果对不对的标准）没通过"))
            run("render_report.py", "render", str(source), "--out", str(output))
            lint = run("render_report.py", "lint", str(source), "--html", str(output), "--terms", str(terms))
            self.assertEqual(lint.returncode, 0, lint.stdout)


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

    def test_prd_chinese_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            prd = Path(tmp) / "prd.md"
            prd.write_text(
                "# 产品需求文档\n\n## 决策表\n内容\n\n## 验收标准\n"
                "AC-1: 用户可以看到结果\nAC-2: 未授权用户被拒绝\n\n## 附录\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(prd)).returncode, 0)

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

    def test_technical_chinese_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tech = Path(tmp) / "technical.md"
            tech.write_text(
                "# 技术方案\n\n## 决策记录\nTD-1: 选择现有存储 [two-way]\n说明\n\n"
                "## 公共契约\n接口\n\n## 运行时证据计划\n日志\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(tech)).returncode, 0)

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
