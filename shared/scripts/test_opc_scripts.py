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
REPO_ROOT = SCRIPTS.parents[1]


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
            self.assertEqual(data["schema_version"], "opc-ledger-v3")
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

    def test_historical_v2_gate_and_dispatch_remain_readable(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            rows = [
                {"schema_version": "opc-ledger-v2", "type": "gate", "gate": "prd", "status": "Approved"},
                {"schema_version": "opc-ledger-v2", "type": "dispatch", "contract": "C-01", "mode": "serial"},
            ]
            ledger.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            result = run("opc_ledger.py", "audit", "--ledger", str(ledger))
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_increment_guardrails_reject_full_context_and_excess_review_rounds(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            bad_dispatch = {
                "type": "dispatch", "contract": "slice-1", "mode": "serial",
                "context_mode": "all",
            }
            result = run(
                "opc_ledger.py", "append", "--ledger", str(ledger),
                "--json", json.dumps(bad_dispatch),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("context", result.stderr)

            invalid_rounds = {
                "type": "gate", "gate": "final", "status": "Issues Found",
                "rounds": 0, "flow": "increment-v1",
            }
            result = run(
                "opc_ledger.py", "append", "--ledger", str(ledger),
                "--json", json.dumps(invalid_rounds),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("round", result.stderr)

            for bad_gate in (
                {"type": "gate", "gate": "reality", "status": "Approved", "rounds": 1},
                {"type": "gate", "gate": "final", "status": "Approved", "rounds": 1, "flow": "increment-vl"},
            ):
                result = run(
                    "opc_ledger.py", "append", "--ledger", str(ledger),
                    "--json", json.dumps(bad_gate),
                )
                self.assertEqual(result.returncode, 1)
                self.assertIn("flow", result.stderr)

    def test_increment_audit_allows_any_positive_repair_count(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            rows = [
                {
                    "schema_version": "opc-ledger-v3", "type": "gate",
                    "gate": "reality", "status": "Approved", "rounds": 20,
                    "flow": "increment-v1",
                },
                {
                    "schema_version": "opc-ledger-v3", "type": "gate",
                    "gate": "final", "status": "Approved", "rounds": 15,
                    "flow": "increment-v1",
                },
            ]
            ledger.write_text("\n".join(json.dumps(row) for row in rows) + "\n")
            result = run("opc_ledger.py", "audit", "--ledger", str(ledger))
            self.assertEqual(result.returncode, 0, result.stdout)

    def test_complete_increment_audit_requires_both_approved_gates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "ledger.jsonl"
            missing = run(
                "opc_ledger.py", "audit", "--ledger", str(ledger),
                "--require-increment-complete",
            )
            self.assertEqual(missing.returncode, 1)
            self.assertIn("incomplete", missing.stdout)
            for gate in ("reality", "final"):
                entry = {
                    "type": "gate", "gate": gate, "status": "Approved",
                    "rounds": 1, "flow": "increment-v1",
                }
                appended = run(
                    "opc_ledger.py", "append", "--ledger", str(ledger),
                    "--json", json.dumps(entry),
                )
                self.assertEqual(appended.returncode, 0, appended.stderr)
            complete = run(
                "opc_ledger.py", "audit", "--ledger", str(ledger),
                "--require-increment-complete",
            )
            self.assertEqual(complete.returncode, 0, complete.stdout)

            reversed_ledger = Path(tmp) / "reversed.jsonl"
            for gate in ("final", "reality"):
                entry = {
                    "type": "gate", "gate": gate, "status": "Approved",
                    "rounds": 1, "flow": "increment-v1",
                }
                self.assertEqual(run(
                    "opc_ledger.py", "append", "--ledger", str(reversed_ledger),
                    "--json", json.dumps(entry),
                ).returncode, 0)
            reversed_result = run(
                "opc_ledger.py", "audit", "--ledger", str(reversed_ledger),
                "--require-increment-complete",
            )
            self.assertEqual(reversed_result.returncode, 1)
            self.assertIn("ordered", reversed_result.stdout)


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


class TestReadmeOnboardingContract(unittest.TestCase):
    def test_architecture_routing_and_adoption_guides_remain_discoverable(self) -> None:
        required_sections = {
            "README.md": (
                "## Who it is for",
                "## System architecture",
                "## Five-minute quick start",
                "## Which skill does what",
                "## Best practices",
                "## New-project onboarding",
                "## Existing-project adoption",
                "assets/opc-develop-skills.png",
                "assets/opc-develop-routing.png",
            ),
            "README.zh-CN.md": (
                "## 适合谁",
                "## 全景架构",
                "## 5 分钟上手",
                "## 哪个 skill 在什么场景做什么",
                "## 最佳实践",
                "## 新项目怎么落地",
                "## 老项目怎么接入",
                "assets/opc-develop-skills.zh-CN.png",
                "assets/opc-develop-routing.zh-CN.png",
            ),
        }
        for relative, markers in required_sections.items():
            content = (REPO_ROOT / relative).read_text(encoding="utf-8")
            for marker in markers:
                with self.subTest(readme=relative, marker=marker):
                    self.assertIn(marker, content)

        for stem in (
            "opc-develop-skills",
            "opc-develop-skills.zh-CN",
            "opc-develop-routing",
            "opc-develop-routing.zh-CN",
        ):
            for suffix in (".svg", ".png"):
                path = REPO_ROOT / "assets" / f"{stem}{suffix}"
                with self.subTest(asset=path.name):
                    self.assertTrue(path.is_file(), f"missing README diagram: {path}")


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

    def test_sha256_repository_review_hash(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            initialized = subprocess.run(
                ["git", "init", "-q", "--object-format=sha256"], cwd=root,
                capture_output=True, text=True,
            )
            if initialized.returncode != 0:
                self.skipTest("git build lacks SHA-256 repository support")
            artifact = root / "prd.md"
            artifact.write_text("sha256 content\n")
            sha = subprocess.run(
                ["git", "hash-object", "prd.md"], cwd=root,
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            self.assertEqual(len(sha), 64)
            review = root / "review.md"
            review.write_text(f"Reviewed-SHA: prd.md {sha}\n")
            result = run("check_freshness.py", str(review), "--repo-root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_relative_repo_root_is_resolved_once(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            root = parent / "repo"
            root.mkdir()
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            artifact = root / "plan.md"
            artifact.write_text("content\n")
            sha = subprocess.run(
                ["git", "hash-object", "plan.md"], cwd=root,
                capture_output=True, text=True, check=True,
            ).stdout.strip()
            review = parent / "review.md"
            review.write_text(f"Reviewed-SHA: plan.md {sha}\n")
            result = run(
                "check_freshness.py", "review.md", "--repo-root", "repo", cwd=parent,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


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

    def test_standard_increment_uses_two_review_chain(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            helper = TestIncrementReceipt(methodName="runTest")
            plan, receipt = helper._repo(root)
            helper._init(root, plan, receipt)
            self.assertEqual(helper._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(helper._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            feature = root
            reviews = root / "reviews"
            plan_rel = "feature-plan.md"
            def sha(path: Path) -> str:
                return subprocess.run(
                    ["git", "hash-object", str(path)], cwd=root,
                    capture_output=True, text=True, check=True,
                ).stdout.strip()
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)
            revision = json.loads(checked.stdout)["revision"]
            (reviews / "reality-review.md").write_text(
                f"**Status:** Approved\nReviewed-SHA: {plan_rel} {sha(plan)}\n"
                f"Reviewed-Revision: {revision}\n"
            )
            (reviews / "final-review.md").write_text(
                f"**Status:** Approved\nReviewed-SHA: {plan_rel} {sha(plan)}\n"
                f"Reviewed-Revision: {revision}\n"
            )
            result = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("5 reviews", result.stdout)

            skipped = run(
                "check_gate_chain.py", str(feature), "--repo-root", str(root),
                "--skip", "reality", "--skip", "final",
            )
            self.assertNotEqual(skipped.returncode, 0)
            self.assertIn("mandatory", skipped.stderr)

            (reviews / "reality-review.md").write_text(
                f"**Status:** Approved\nReviewed-SHA: {plan_rel} {sha(plan)}\n"
            )
            result = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("Reviewed-Revision", result.stderr)
            (reviews / "reality-review.md").write_text(
                f"**Status:** Approved\nReviewed-SHA: {plan_rel} {sha(plan)}\n"
                f"Reviewed-Revision: {revision}\n"
            )

            (root / "app.txt").write_text("changed code\n")
            result = run("check_gate_chain.py", str(feature), "--repo-root", str(root))
            self.assertEqual(result.returncode, 1)
            self.assertIn("final-review.md", result.stderr)


class TestValidateArtifacts(unittest.TestCase):
    def _write_cases(self, directory: Path) -> None:
        (directory / "testcases.md").write_text(
            "# Test Cases\n\n## Coverage Map\n| AC | Cases |\n| --- | --- |\n| AC-1 | TC-1 |\n\n"
            "## Cases\n### TC-1: Core case [level: ui-e2e] [seed: seed:core] [AC-1]\n"
            "Given a named starting world\nWhen the user performs the action\n"
            "Driver-Action: playwright | click the primary action\nThen the result is visible and stored\n"
            "Success-Signal: result appears\nFailure-Signal: error alert appears\n"
            "Data-Provenance: canonical-clone | named-source\nProvider-Mode: stub\n"
            "Observe: interface | result or error\nObserve: logs | trace terminal event\n"
            "Observe: state | read-only durable assertion\nFallback: computer-use | atomic-only\n"
        )

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

    def test_feature_plan_has_no_duration_budget_gate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            plan = Path(tmp) / "feature-plan.md"
            self._write_cases(plan.parent)
            plan.write_text(
                "# Feature Plan\n\n"
                "Plan-Version: opc-increment-v1\n"
                "\n"
                "## Outcome\n"
                "User-Action: run the existing workflow\n"
                "Entry-Point: /workflows/vera\n"
                "Success-Signal: completed run is visible\n"
                "Non-Goals: bulk migration\n\n"
                "## Core Journey\n"
                "Journey-Type: ui\n"
                "Given: the traced snapshot\n"
                "When: the user clicks Run\n"
                "Then: the canvas shows completion\n"
                "Production-Assembly: page -> session -> router -> service -> scratch DB\n"
                "Data-Kind: snapshot\n"
                "Data-Source: vera-workflow\n"
                "Data-Hash: sha256:abc123\n"
                "Safety-1: preserve the original workflow\n"
                "Safety-2: do not affect other users\n\n"
                "## Slices\n"
                "Slice-1: click creates a run | browser core journey\n"
                "Slice-2: reload keeps state | browser core journey\n\n"
                "## Acceptance\n"
                "Build-Command: python -m compileall src\n"
                "Core-Case: TC-1\nCore-Command: npm run case -- TC-1\n"
                "Regression-Command: npm run case -- --suite feature\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(plan)).returncode, 0)

            # Legacy estimate fields remain parseable for migration but never gate work.
            plan.write_text(
                plan.read_text()
                .replace("Plan-Version: opc-increment-v1\n", (
                    "Plan-Version: opc-increment-v1\nClass: split\nBudget-Minutes: 999999\n"
                ))
                .replace("Slice-1: click", "Slice-1: 999999 | click")
            )
            self.assertEqual(run("validate_artifacts.py", str(plan)).returncode, 0)

            plan.write_text(plan.read_text() + (
                "\n## Core Journey\nData-Hash: sha256:different\n"
            ))
            result = run("validate_artifacts.py", str(plan))
            self.assertEqual(result.returncode, 1)
            self.assertIn("exactly one", result.stderr.lower())
            self.assertIn("data-hash", result.stderr.lower())

    def test_feature_plan_must_retire_every_demo_mock(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "docs/features/1-export"
            (feature / "demo").mkdir(parents=True)
            self._write_cases(feature)
            inventory = feature / "demo/mock-inventory.md"
            inventory.write_text(
                "- id: M-1\n  file: ui.ts\n  type: stubbed-endpoint\n"
                "  scenario: export\n  replacement: export API\n"
            )
            plan = feature / "feature-plan.md"
            plan.write_text(
                "# Feature Plan\n\nPlan-Version: opc-increment-v1\n\n"
                "## Outcome\nUser-Action: export one report\n"
                "Entry-Point: /exports\nSuccess-Signal: report appears\nNon-Goals: bulk export\n\n"
                "## Core Journey\nJourney-Type: ui\nGiven: source-hashed report\n"
                "When: user clicks Export\nThen: report appears\n"
                "Production-Assembly: page -> route -> service -> scratch DB\n"
                "Data-Kind: snapshot\nData-Source: report\nData-Hash: sha256:abc\n"
                "Safety-1: source unchanged\nSafety-2: other users unchanged\n\n"
                "## Slices\nSlice-1: one report exports | browser regression\n\n"
                "## Acceptance\nBuild-Command: make check\nCore-Case: TC-1\n"
                "Core-Command: make case TC-1\nRegression-Command: make testcase suite\n"
            )
            missing = run("validate_artifacts.py", str(plan))
            self.assertEqual(missing.returncode, 1)
            self.assertIn("retirement", missing.stderr.lower())
            plan.write_text(plan.read_text() + (
                "\n## Mock Retirement\n"
                "Mock-Retirement: M-1 | Slice-1 | export API | browser export regression\n"
            ))
            self.assertEqual(run("validate_artifacts.py", str(plan)).returncode, 0)
            plan.write_text(plan.read_text().replace("## Mock Retirement", "## 模拟退役"))
            self.assertEqual(run("validate_artifacts.py", str(plan)).returncode, 0)

    def test_feature_plan_maps_optional_prd_constraints(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            feature = Path(tmp) / "docs/features/1-export"
            feature.mkdir(parents=True)
            self._write_cases(feature)
            prd = feature / "prd.md"
            prd.write_text(
                "# PRD\n\n## Decision Sheet\nx\n\n## Acceptance Criteria\n"
                "AC-1: one report exports\n\n## Appendix\n"
            )
            plan = feature / "feature-plan.md"
            plan.write_text(
                "# Feature Plan\n\nPlan-Version: opc-increment-v1\n\n"
                "## Outcome\nUser-Action: export one report\n"
                "Entry-Point: /exports\nSuccess-Signal: report appears\nNon-Goals: bulk export\n\n"
                "## Core Journey\nJourney-Type: ui\nGiven: source-hashed report\n"
                "When: user clicks Export\nThen: report appears\n"
                "Production-Assembly: page -> route -> service -> scratch DB\n"
                "Data-Kind: snapshot\nData-Source: report\nData-Hash: sha256:abc\n"
                "Safety-1: source unchanged\nSafety-2: other users unchanged\n\n"
                "## Slices\nSlice-1: one report exports | browser regression\n\n"
                "## Acceptance\nBuild-Command: make check\nCore-Case: TC-1\n"
                "Core-Command: make case TC-1\nRegression-Command: make testcase suite\n"
            )
            missing = run("validate_artifacts.py", str(plan))
            self.assertEqual(missing.returncode, 1)
            self.assertIn("constraint", missing.stderr.lower())
            plan.write_text(plan.read_text() + (
                "\n## Optional Constraints\n"
                "Constraint: AC-1 | Slice-1 | TC-1 browser export\n"
            ))
            self.assertEqual(run("validate_artifacts.py", str(plan)).returncode, 0)

    def test_testcases_validate_coverage_and_browser_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cases = Path(tmp) / "testcases.md"
            cases.write_text(
                "# Test Cases\n\n"
                "## Coverage Map\n"
                "| AC | Cases |\n"
                "| --- | --- |\n"
                "| AC-1 | TC-1 |\n\n"
                "## Cases\n"
                "### TC-1: Run from canvas [level: ui-e2e] [seed: seed:vera] [AC-1]\n"
                "Given the traced workflow snapshot\n"
                "When the user runs it\n"
                "Driver-Action: playwright | click the Run button\n"
                "Then the completed run is visible and stored\n"
                "Success-Signal: completed result appears\nFailure-Signal: error alert appears\n"
                "Data-Provenance: canonical-clone | vera-workflow\nProvider-Mode: stub\n"
                "Observe: interface | result or error\nObserve: logs | trace terminal event\n"
                "Observe: state | read-only run row\nFallback: computer-use | atomic-only\n"
            )
            self.assertEqual(run("validate_artifacts.py", str(cases)).returncode, 0)

            cases.write_text(cases.read_text().replace(
                "Driver-Action: playwright | click the Run button\n", ""
            ))
            result = run("validate_artifacts.py", str(cases))
            self.assertEqual(result.returncode, 1)
            self.assertIn("playwright", result.stderr.lower())

            cases.write_text(
                cases.read_text().replace("| AC-1 | TC-1 |", "| AC-1 | TC-9 |")
            )
            result = run("validate_artifacts.py", str(cases))
            self.assertEqual(result.returncode, 1)
            self.assertIn("coverage", result.stderr.lower())

            cases.write_text(cases.read_text().replace("| AC-1 | TC-9 |", "| AC-1 | TBD |"))
            result = run("validate_artifacts.py", str(cases))
            self.assertEqual(result.returncode, 1)
            self.assertIn("names no tc", result.stderr.lower())


class TestIncrementReceipt(unittest.TestCase):
    def _repo(self, root: Path, journey_type: str = "ui") -> tuple[Path, Path]:
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "opc@example.invalid"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "OPC Test"], cwd=root, check=True)
        (root / "app.txt").write_text("v1\n")
        (root / "demo").mkdir()
        (root / "reviews").mkdir()
        (root / "demo/prototype.md").write_text("# Prototype\n\nEntry: /workflows/vera\n")
        (root / "demo/mock-inventory.md").write_text("# Mock inventory\n\nNo mocks.\n")
        (root / "prd.md").write_text(
            "# PRD\n\n## Decision Sheet\nRun one workflow.\n\n"
            "## Acceptance Criteria\nAC-1: the selected workflow completes and is stored\n\n"
            "## Appendix\nDemo alignment: run button and result are contractual.\n"
        )
        (root / "testcases.md").write_text(
            "# Test Cases\n\n## Coverage Map\n| AC | Cases |\n| --- | --- |\n"
            "| AC-1 | TC-1 |\n\n## Cases\n"
            "### TC-1: Run from canvas [level: ui-e2e] [seed: seed:vera] [AC-1]\n"
            "Given the traced workflow snapshot\nWhen the user runs it\n"
            "Driver-Action: playwright | click the Run button\n"
            "Then the completed run is visible and stored\n"
            "Success-Signal: completed result appears\nFailure-Signal: error alert appears\n"
            "Data-Provenance: canonical-clone | vera-workflow\nProvider-Mode: stub\n"
            "Observe: interface | result or error alert\nObserve: logs | trace-linked terminal event\n"
            "Observe: state | read-only run row and source invariant\n"
            "Fallback: computer-use | atomic-only\n"
        )

        def hash_object(path: Path) -> str:
            return subprocess.run(
                ["git", "hash-object", relative := path.relative_to(root).as_posix()], cwd=root,
                capture_output=True, text=True, check=True,
            ).stdout.strip()

        (root / "reviews/demo-review.md").write_text(
            "**Status:** Approved\n"
            f"Reviewed-SHA: demo/prototype.md {hash_object(root / 'demo/prototype.md')}\n"
            f"Reviewed-SHA: demo/mock-inventory.md {hash_object(root / 'demo/mock-inventory.md')}\n"
        )
        (root / "reviews/prd-review.md").write_text(
            "**Status:** Approved\n"
            f"Reviewed-SHA: prd.md {hash_object(root / 'prd.md')}\n"
        )
        compiled = run("opc_testcase.py", "compile", "--repo", str(root), "--feature-dir", str(root))
        self.assertEqual(compiled.returncode, 0, compiled.stderr)
        (root / "reviews/testcase-review.md").write_text(
            "**Status:** Approved\n"
            f"Reviewed-SHA: testcases.md {hash_object(root / 'testcases.md')}\n"
            f"Reviewed-SHA: testcases.json {hash_object(root / 'testcases.json')}\n"
        )
        approved = run(
            "opc_testcase.py", "approve", "--repo", str(root), "--feature-dir", str(root),
            "--actor", "product-owner", "--decision-note", "case semantics accepted",
        )
        self.assertEqual(approved.returncode, 0, approved.stderr)

        runner = root / "case_runner.py"
        runner.write_text(
            "import argparse, hashlib, json, os\n"
            "from pathlib import Path\n"
            "p=argparse.ArgumentParser(); p.add_argument('--driver',default='playwright'); "
            "p.add_argument('--data',default='canonical-clone'); p.add_argument('--provider',default='stub'); "
            "p.add_argument('--outcome',default='passed'); p.add_argument('--static',action='store_true'); a=p.parse_args()\n"
            "root=Path.cwd().resolve(); evidence=Path(os.environ['OPC_CASE_EVIDENCE']); evidence.parent.mkdir(parents=True,exist_ok=True)\n"
            "records=[]\n"
            "for kind in ('interface','logs','state'):\n"
            " path=evidence.parent/f'{kind}.txt'; path.write_text(f'{kind}:ok\\n'); content=path.read_bytes(); "
            "records.append({'path':path.resolve().relative_to(root).as_posix(),'sha256':'sha256:'+hashlib.sha256(content).hexdigest(),'kind':'report'})\n"
            "payload={'schema_version':'opc-case-evidence-v1','case_id':os.environ['OPC_CASE_ID'],"
            "'manifest_sha256':os.environ['OPC_CASE_MANIFEST_SHA256'],"
            "'driver':{'type':a.driver,'action_performed':a.driver in ('playwright','computer-use'),'atomic_scope':True,'fallback_reason':'test fallback' if a.driver=='computer-use' else None},"
            "'assembly':{'kind':'production','origin':'http://127.0.0.1:7777','session_type':'scratch','build_id':'test-build'},"
            "'data':{'kind':a.data,'source':'vera-workflow','source_sha256':'sha256:abc123','isolation':'isolated-copy','db_path':str(evidence.parent/'scratch.db')},"
            "'provider':{'mode':a.provider},'observation':{'complete':a.outcome=='passed',"
            "'interface':{'passed':a.outcome=='passed','artifact':records[0]['path']},"
            "'logs':{'passed':a.outcome=='passed','artifact':records[1]['path']},"
            "'state':{'passed':a.outcome=='passed','artifact':records[2]['path']}},"
            "'outcome':{'product':a.outcome},'correlations':{'case_id':os.environ['OPC_CASE_ID'],'trace_id':'trace-1','object_ids':['obj-1']},"
            "'steps':[{'step_id':'STEP-1','status':'passed' if a.outcome=='passed' else 'failed'}],'artifacts':records}\n"
            "evidence.write_text(json.dumps(payload,sort_keys=True)+'\\n')\n"
        )
        plan = root / "feature-plan.md"
        plan.write_text(
            "# Feature Plan\n\n"
            "Plan-Version: opc-increment-v1\n\n"
            "## Outcome\n"
            "User-Action: run the existing workflow\n"
            "Entry-Point: /workflows/vera\n"
            "Success-Signal: completed run is visible\n"
            "Non-Goals: bulk migration\n\n"
            "## Core Journey\n"
            f"Journey-Type: {journey_type}\n"
            "Given: the traced snapshot\n"
            "When: the user runs it\n"
            "Then: the completed result is visible\n"
            "Production-Assembly: entry -> session -> router -> service -> scratch DB\n"
            "Data-Kind: snapshot\n"
            "Data-Source: vera-workflow\n"
            "Data-Hash: sha256:abc123\n"
            "Safety-1: preserve the original workflow\n"
            "Safety-2: do not affect other users\n\n"
            "## Slices\n"
            "Slice-1: run produces a result | core journey\n\n"
            "## Optional Constraints\n"
            "Constraint: AC-1 | Slice-1 | TC-1\n\n"
            "## Acceptance\n"
            "Build-Command: python -c pass\n"
            "Core-Case: TC-1\n"
            "Core-Command: npm run case -- TC-1\n"
            "Regression-Command: npm run case -- --suite feature\n"
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        return plan, root / "acceptance.json"

    def _init(self, root: Path, plan: Path, receipt: Path) -> None:
        result = run(
            "opc_increment.py", "init", "--repo", str(root),
            "--plan", str(plan), "--receipt", str(receipt),
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def _record_success(
        self, root: Path, receipt: Path, kind: str, *flags: str,
    ) -> subprocess.CompletedProcess:
        label = "external provider passed" if kind == "provider" else (
            "seeded passed" if kind in {"build", "logic", "replay"} else "local real service passed"
        )
        extra: list[str] = []
        command = [sys.executable, "-c", "raise SystemExit(0)"]
        if (kind == "browser" and "--core" in flags) or kind == "provider":
            artifact = root / ".git" / f"opc-{kind}-evidence.json"
            extra = [
                "--case-id", "TC-1", "--case-evidence", str(artifact),
            ]
            command = [
                sys.executable, str(root / "case_runner.py"),
                "--provider", "live" if kind == "provider" else "stub",
            ]
        return run(
            "opc_increment.py", "run", "--repo", str(root),
            "--receipt", str(receipt), "--kind", kind,
            "--label", label, *flags, *extra,
            "--", *command,
        )

    def test_real_ui_journey_passes_and_code_change_invalidates_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            result = self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)

            (root / "reviews").mkdir(exist_ok=True)
            (root / "reviews/final-review.md").write_text("review\n")
            (root / "ledger.jsonl").write_text("{}\n")
            (root / "release-manifest.md").write_text("manifest\n")
            process_only = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(process_only.returncode, 0, process_only.stderr)

            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "record receipt"], cwd=root, check=True)
            committed = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(committed.returncode, 0, committed.stderr)

            (root / "app.txt").write_text("v2\n")
            stale = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(stale.returncode, 1)
            self.assertIn("stale", stale.stderr.lower())

    def test_ui_journey_requires_browser_driven_key_action(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            result = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "browser",
                "--label", "local real service passed", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
                "--", sys.executable, "-c", "raise SystemExit(0)",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("approved testcase runner", result.stderr)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 1)
            self.assertIn("browser", checked.stderr.lower())

    def test_deleted_evidence_artifact_invalidates_real_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            (root / ".git/opc-browser-evidence.json").unlink()
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 1)

    def test_preexisting_unchanged_artifact_cannot_prove_real_core(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            artifact = root / ".git/opc-browser-evidence.json"
            result = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "browser",
                "--label", "local real service passed", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
                "--case-id", "TC-1", "--case-evidence", str(artifact),
                "--", sys.executable, str(root / "case_runner.py"), "--provider", "stub",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("content was not created or changed", result.stderr)

    def test_other_feature_process_records_do_not_stale_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            other = root / "docs/features/2-other/reviews"
            other.mkdir(parents=True)
            (other / "reality-review.md").write_text("process-only\n")
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_completion_levels_are_cumulative_from_build(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "automated-core-journey",
            )
            self.assertEqual(checked.returncode, 1)
            self.assertIn("required", checked.stderr.lower())

    def test_provider_requires_offline_layers_and_refuses_repeat(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            early = self._record_success(root, receipt, "provider")
            self.assertEqual(early.returncode, 1)
            self.assertIn("offline", early.stderr.lower())

            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            self.assertEqual(self._record_success(root, receipt, "replay").returncode, 0)
            first = self._record_success(root, receipt, "provider")
            self.assertEqual(first.returncode, 0, first.stderr)
            second = self._record_success(root, receipt, "provider")
            self.assertEqual(second.returncode, 1)
            self.assertIn("repeat", second.stderr.lower())

    def test_concurrent_provider_runs_execute_only_one_canary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            self.assertEqual(self._record_success(root, receipt, "replay").returncode, 0)

            processes = []
            artifacts = []
            for index in (1, 2):
                artifact = root / ".git" / f"provider-concurrent-{index}.json"
                artifacts.append(artifact)
                command = [
                    sys.executable, str(SCRIPTS / "opc_increment.py"), "run",
                    "--repo", str(root), "--receipt", str(receipt),
                    "--kind", "provider", "--label", "external provider passed",
                    "--case-id", "TC-1", "--case-evidence", str(artifact),
                    "--", sys.executable, str(root / "case_runner.py"), "--provider", "live",
                ]
                processes.append(subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True))
            results = [process.communicate(timeout=10) + (process.returncode,) for process in processes]
            self.assertEqual(sorted(result[2] for result in results), [0, 1], results)
            self.assertEqual(sum(path.exists() for path in artifacts), 1)
            data = json.loads(receipt.read_text())
            providers = [row for row in data["commands"] if row["kind"] == "provider"]
            self.assertEqual(len(providers), 1)

    def test_human_acceptance_is_a_distinct_fresh_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            self.assertEqual(self._record_success(
                root, receipt, "browser", "--core", "--browser-action",
                "--production-assembly", "--data-hash", "sha256:abc123",
            ).returncode, 0)
            accepted = run(
                "opc_increment.py", "accept", "--repo", str(root),
                "--receipt", str(receipt), "--actor", "owner",
            )
            self.assertEqual(accepted.returncode, 0, accepted.stderr)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "human-accepted",
            )
            self.assertEqual(checked.returncode, 0, checked.stderr)

    def test_later_failed_core_attempt_invalidates_pass_and_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            flags = (
                "--core", "--browser-action", "--production-assembly",
                "--data-hash", "sha256:abc123",
            )
            self.assertEqual(self._record_success(root, receipt, "browser", *flags).returncode, 0)
            self.assertEqual(run(
                "opc_increment.py", "accept", "--repo", str(root),
                "--receipt", str(receipt), "--actor", "owner",
            ).returncode, 0)
            artifact = root / ".git" / "failed-browser-evidence.json"
            failed = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "browser",
                "--label", "local real service passed", *flags,
                "--case-id", "TC-1", "--case-evidence", str(artifact),
                "--", sys.executable, "-c", "raise SystemExit(1)",
            )
            self.assertEqual(failed.returncode, 1)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "real-service-core-journey",
            )
            self.assertEqual(checked.returncode, 1)

    def test_command_launch_failure_invalidates_older_layer_pass(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            failed = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "build",
                "--label", "seeded passed", "--", "/definitely/not/a/command",
            )
            self.assertNotEqual(failed.returncode, 0)
            data = json.loads(receipt.read_text())
            self.assertEqual(len(data["commands"]), 2)
            self.assertEqual(data["commands"][-1]["label"], "blocked")
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "code-build",
            )
            self.assertEqual(checked.returncode, 1)

    def test_invalid_utf8_failure_is_recorded_and_dominates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            failed = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "build",
                "--label", "seeded passed", "--", sys.executable, "-c",
                "import sys; sys.stdout.buffer.write(b'\\xff'); raise SystemExit(1)",
            )
            self.assertEqual(failed.returncode, 1)
            data = json.loads(receipt.read_text())
            self.assertEqual(len(data["commands"]), 2)
            checked = run(
                "opc_increment.py", "check", "--repo", str(root),
                "--receipt", str(receipt), "--require", "code-build",
            )
            self.assertEqual(checked.returncode, 1)

    def test_legacy_estimates_do_not_block_receipt_and_exclusions_cannot_be_overridden(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            plan.write_text(plan.read_text().replace(
                "Plan-Version: opc-increment-v1\n",
                "Plan-Version: opc-increment-v1\nClass: split\nBudget-Minutes: 999999\n",
            ))
            result = run(
                "opc_increment.py", "init", "--repo", str(root),
                "--plan", str(plan), "--receipt", str(receipt),
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            receipt.unlink()

            result = run(
                "opc_increment.py", "init", "--repo", str(root),
                "--plan", str(plan), "--receipt", str(receipt),
                "--exclude", "app.txt",
            )
            self.assertNotEqual(result.returncode, 0)

    def test_tampered_receipt_cannot_exclude_product_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            data = json.loads(receipt.read_text())
            data["excluded_paths"].append("app.txt")
            receipt.write_text(json.dumps(data) + "\n")
            result = self._record_success(root, receipt, "build")
            self.assertEqual(result.returncode, 1)
            self.assertIn("tampered", result.stderr.lower())

    def test_reinitialization_cannot_erase_command_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._repo(root)
            self._init(root, plan, receipt)
            self.assertEqual(self._record_success(root, receipt, "build").returncode, 0)
            before = receipt.read_text()
            result = run(
                "opc_increment.py", "init", "--repo", str(root),
                "--plan", str(plan), "--receipt", str(receipt),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("already exists", result.stderr)
            self.assertEqual(receipt.read_text(), before)

    def test_same_revision_receipts_keep_separate_command_logs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source_plan, _ = self._repo(root)
            plan_text = source_plan.read_text()
            source_plan.unlink()
            plan_a = root / "docs/features/1-a/feature-plan.md"
            plan_b = root / "docs/features/2-b/feature-plan.md"

            def prepare_feature(plan: Path, text: str) -> None:
                feature = plan.parent
                (feature / "demo").mkdir(parents=True)
                (feature / "reviews").mkdir()
                for rel in ("demo/prototype.md", "demo/mock-inventory.md", "prd.md", "testcases.md"):
                    target = feature / rel
                    target.write_text((root / rel).read_text())
                def hashed(path: Path) -> str:
                    return subprocess.run(
                        ["git", "hash-object", path.relative_to(root).as_posix()], cwd=root,
                        capture_output=True, text=True, check=True,
                    ).stdout.strip()
                prefix = feature.relative_to(root).as_posix()
                (feature / "reviews/demo-review.md").write_text(
                    "**Status:** Approved\n"
                    f"Reviewed-SHA: {prefix}/demo/prototype.md {hashed(feature / 'demo/prototype.md')}\n"
                    f"Reviewed-SHA: {prefix}/demo/mock-inventory.md {hashed(feature / 'demo/mock-inventory.md')}\n"
                )
                (feature / "reviews/prd-review.md").write_text(
                    "**Status:** Approved\n"
                    f"Reviewed-SHA: {prefix}/prd.md {hashed(feature / 'prd.md')}\n"
                )
                compiled = run(
                    "opc_testcase.py", "compile", "--repo", str(root),
                    "--feature-dir", str(feature),
                )
                self.assertEqual(compiled.returncode, 0, compiled.stderr)
                (feature / "reviews/testcase-review.md").write_text(
                    "**Status:** Approved\n"
                    f"Reviewed-SHA: {prefix}/testcases.md {hashed(feature / 'testcases.md')}\n"
                    f"Reviewed-SHA: {prefix}/testcases.json {hashed(feature / 'testcases.json')}\n"
                )
                approved = run(
                    "opc_testcase.py", "approve", "--repo", str(root),
                    "--feature-dir", str(feature), "--actor", "owner",
                    "--decision-note", "approved for receipt isolation test",
                )
                self.assertEqual(approved.returncode, 0, approved.stderr)
                plan.write_text(text)

            prepare_feature(plan_a, plan_text)
            prepare_feature(plan_b, plan_text.replace("/workflows/vera", "/workflows/b"))
            subprocess.run(["git", "add", "-A"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "two plans"], cwd=root, check=True)
            receipt_a = plan_a.parent / "acceptance.json"
            receipt_b = plan_b.parent / "acceptance.json"
            self._init(root, plan_a, receipt_a)
            self._init(root, plan_b, receipt_b)
            for receipt, output in ((receipt_a, "alpha"), (receipt_b, "beta")):
                result = run(
                    "opc_increment.py", "run", "--repo", str(root),
                    "--receipt", str(receipt), "--kind", "build",
                    "--label", "seeded passed", "--",
                    sys.executable, "-c", f"print({output!r})",
                )
                self.assertEqual(result.returncode, 0, result.stderr)
            for receipt in (receipt_a, receipt_b):
                checked = run(
                    "opc_increment.py", "check", "--repo", str(root),
                    "--receipt", str(receipt), "--require", "code-build",
                )
                self.assertEqual(checked.returncode, 0, checked.stderr)


class TestTestcaseWorkflow(unittest.TestCase):
    def _ready_repo(self, root: Path) -> tuple[Path, Path]:
        helper = TestIncrementReceipt(methodName="runTest")
        return helper._repo(root)

    def test_compile_fails_when_demo_review_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._ready_repo(root)
            (root / "reviews/demo-review.md").unlink()
            result = run(
                "opc_testcase.py", "compile", "--repo", str(root),
                "--feature-dir", str(root),
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("demo-review.md", result.stderr)

    def test_product_approval_stales_when_testcase_changes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._ready_repo(root)
            before = run(
                "opc_testcase.py", "check", "--repo", str(root),
                "--feature-dir", str(root), "--require-approved",
            )
            self.assertEqual(before.returncode, 0, before.stderr)
            (root / "testcases.md").write_text(
                (root / "testcases.md").read_text().replace(
                    "completed result appears", "completed result and timestamp appear",
                )
            )
            after = run(
                "opc_testcase.py", "check", "--repo", str(root),
                "--feature-dir", str(root), "--require-approved",
            )
            self.assertEqual(after.returncode, 1)
            self.assertIn("stale", after.stderr.lower())

    def test_testcase_wrapper_executes_only_an_approved_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._ready_repo(root)
            evidence = root / ".git/wrapper-evidence.json"
            result = run(
                "opc_testcase.py", "run", "--repo", str(root),
                "--feature-dir", str(root), "--case", "TC-1",
                "--evidence", str(evidence), "--",
                sys.executable, str(root / "case_runner.py"),
                cwd=root,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("local real service passed", result.stdout)

    def test_synthetic_case_cannot_be_upgraded_to_real_service(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan, receipt = self._ready_repo(root)
            helper = TestIncrementReceipt(methodName="runTest")
            helper._init(root, plan, receipt)
            self.assertEqual(helper._record_success(root, receipt, "build").returncode, 0)
            evidence = root / ".git/synthetic-evidence.json"
            result = run(
                "opc_increment.py", "run", "--repo", str(root),
                "--receipt", str(receipt), "--kind", "browser", "--core",
                "--case-id", "TC-1", "--case-evidence", str(evidence), "--",
                sys.executable, str(root / "case_runner.py"), "--data", "synthetic",
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("data provenance", result.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=1)
