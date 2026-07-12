#!/usr/bin/env python3
"""Validate and run OPC benchmark cases with GREEN -> RED -> GREEN proof."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import subprocess
import tempfile
import time
from pathlib import Path

KINDS = {"fixture", "fake", "mutation", "historical_ref", "local_service", "real"}
FIDELITY_ORDER = {"fixture": 0, "fake": 1, "mutation": 2, "local_service": 3, "real": 4}
REQUIRED = {"schema_version", "id", "title", "provenance", "initial_state", "task", "ground_truth", "profiles"}


def load_cases(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    return data.get("cases", []) if isinstance(data, dict) else data


def validate_case(case: dict) -> list[str]:
    errors = [f"missing {key}" for key in sorted(REQUIRED - case.keys())]
    if not isinstance(case.get("profiles"), list) or not case.get("profiles"):
        errors.append("profiles must be a non-empty list")
    ids = set()
    for profile in case.get("profiles", []):
        for key in ("id", "kind", "fidelity"):
            if key not in profile:
                errors.append(f"profile missing {key}")
        if profile.get("kind") not in KINDS:
            errors.append(f"unsupported profile kind: {profile.get('kind')}")
        if profile.get("id") in ids:
            errors.append(f"duplicate profile id: {profile.get('id')}")
        ids.add(profile.get("id"))
        if profile.get("kind") in {"mutation", "historical_ref"}:
            needed = {"good_ref", "bad_ref"} if profile.get("kind") == "historical_ref" else {"patch"}
            for key in needed:
                if key not in profile:
                    errors.append(f"{profile.get('kind')} profile missing {key}")
        if "verification" not in profile:
            errors.append(f"profile {profile.get('id')} missing verification")
    return errors


def command_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(x) for x in value]
    return shlex.split(str(value))


def run_command(recipe: dict, cwd: Path, env: dict | None = None) -> dict:
    started = time.time()
    try:
        proc = subprocess.run(command_list(recipe["command"]), cwd=cwd, env={**os.environ, **(env or {})}, capture_output=True, text=True, timeout=recipe.get("timeout_secs", 120))
    except subprocess.TimeoutExpired as exc:
        return {"ok": False, "exit_code": None, "expected_exit": int(recipe.get("expected_exit", 0)), "missing": [], "forbidden_claims": [], "stdout_tail": str(exc.stdout or "")[-2000:], "stderr_tail": str(exc.stderr or "")[-2000:], "wall_secs": round(time.time() - started, 3), "error": "timeout"}
    expected = int(recipe.get("expected_exit", 0))
    output = proc.stdout + proc.stderr
    forbidden = recipe.get("must_not_claim", [])
    missing = [text for text in recipe.get("must_include", []) if text not in output]
    claims = [text for text in forbidden if text in output]
    return {
        "ok": proc.returncode == expected and not missing and not claims,
        "exit_code": proc.returncode,
        "expected_exit": expected,
        "missing": missing,
        "forbidden_claims": claims,
        "stdout_tail": proc.stdout[-2000:],
        "stderr_tail": proc.stderr[-2000:],
        "wall_secs": round(time.time() - started, 3),
    }


def add_worktree(repo: Path, ref: str, target: Path) -> None:
    subprocess.run(["git", "worktree", "add", "--detach", str(target), ref], cwd=repo, check=True, capture_output=True, text=True)


def remove_worktree(repo: Path, target: Path) -> bool:
    proc = subprocess.run(["git", "worktree", "remove", "--force", str(target)], cwd=repo, capture_output=True, text=True)
    subprocess.run(["git", "worktree", "prune"], cwd=repo, capture_output=True)
    return proc.returncode == 0 and not target.exists()


def run_profile(case: dict, profile: dict, repo: Path) -> dict:
    if profile.get("kind") == "real" and not profile.get("allow_real"):
        raise ValueError("real profile requires --allow-real")
    verification = profile["verification"]
    temp_root = Path(tempfile.mkdtemp(prefix=f"opc-bench-{case['id']}-"))
    cleanup_ok = True
    phases = {}
    worktrees = []
    try:
        if profile["kind"] == "historical_ref":
            good = temp_root / "good"; bad = temp_root / "bad"
            add_worktree(repo, profile["good_ref"], good); worktrees.append(good)
            add_worktree(repo, profile["bad_ref"], bad); worktrees.append(bad)
            phases["good_before"] = run_command(verification["good"], good)
            phases["bad_variant"] = run_command(verification["bad"], bad)
            phases["good_after"] = run_command(verification.get("restore", verification["good"]), good)
            cleanup_ok = remove_worktree(repo, bad) and remove_worktree(repo, good)
            worktrees.clear()
        elif profile["kind"] == "mutation":
            work = temp_root / "work"
            add_worktree(repo, profile.get("good_ref", "HEAD"), work); worktrees.append(work)
            phases["good_before"] = run_command(verification["good"], work)
            patch = (repo / profile["patch"]).resolve()
            applied = subprocess.run(["git", "apply", str(patch)], cwd=work, capture_output=True, text=True)
            if applied.returncode != 0:
                phases["bad_variant"] = {"ok": False, "error": applied.stderr}
            else:
                phases["bad_variant"] = run_command(verification["bad"], work)
                subprocess.run(["git", "apply", "-R", str(patch)], cwd=work, check=True)
            phases["good_after"] = run_command(verification.get("restore", verification["good"]), work)
            cleanup_ok = remove_worktree(repo, work); worktrees.clear()
        else:
            cwd = repo
            phases["good_before"] = run_command(verification["good"], cwd)
            setup = profile.get("bad_setup")
            if setup:
                setup_result = run_command({"command": setup, "expected_exit": 0}, cwd)
                if not setup_result["ok"]:
                    phases["bad_variant"] = {"ok": False, "error": "bad_setup failed"}
                else:
                    phases["bad_variant"] = run_command(verification["bad"], cwd)
            else:
                phases["bad_variant"] = run_command(verification["bad"], cwd)
            teardown = profile.get("bad_teardown")
            if teardown:
                cleanup_ok = run_command({"command": teardown, "expected_exit": 0}, cwd)["ok"]
            phases["good_after"] = run_command(verification.get("restore", verification["good"]), cwd)
    finally:
        for worktree in reversed(worktrees):
            cleanup_ok = remove_worktree(repo, worktree) and cleanup_ok
        try:
            temp_root.rmdir()
        except OSError:
            pass
    ok = all(phases.get(name, {}).get("ok") for name in ("good_before", "bad_variant", "good_after")) and cleanup_ok
    return {"case_id": case["id"], "profile_id": profile["id"], "kind": profile["kind"], "fidelity": profile["fidelity"], "ok": ok, "phases": phases, "cleanup_ok": cleanup_ok}


def html_report(report: dict) -> str:
    rows = "".join(f"<tr><td>{r['case_id']}</td><td>{r['profile_id']}</td><td>{r['fidelity']}</td><td>{'通过' if r['ok'] else '失败'}</td></tr>" for r in report["runs"])
    digest = hashlib.sha256(json.dumps(report, sort_keys=True).encode()).hexdigest()
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="opc-report-sha256" content="{digest}"><style>body{{font:16px/1.7 system-ui;max-width:76ch;margin:40px auto}}table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #ddd;padding:8px}}</style><title>OPC Benchmark</title></head><body><h1>Benchmark（把历史问题压缩成可重复实验）</h1><h2>结论</h2><p>{'全部通过' if report['ok'] else '存在失败'}</p><h2>对用户意味着什么</h2><p>流程会先证明好版本可用，再注入缺陷确认检查会变红，最后恢复并重新变绿。</p><h2>证据</h2><table><tr><th>Case</th><th>Profile</th><th>真实性</th><th>结果</th></tr>{rows}</table><h2>下一步</h2><p>失败 case 必须修复后才能进入发布门禁。</p></body></html>'''


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    val = sub.add_parser("validate"); val.add_argument("registry")
    run = sub.add_parser("run"); run.add_argument("registry"); run.add_argument("--case"); run.add_argument("--profile", default="auto"); run.add_argument("--all-profiles", action="store_true"); run.add_argument("--allow-real", action="store_true"); run.add_argument("--repo", default="."); run.add_argument("--out")
    args = parser.parse_args()
    cases = load_cases(Path(args.registry))
    errors = {case.get("id", "unknown"): validate_case(case) for case in cases}
    errors = {key: value for key, value in errors.items() if value}
    if args.command == "validate":
        print(json.dumps({"ok": not errors, "errors": errors}, ensure_ascii=False, indent=2))
        return 1 if errors else 0
    if errors:
        print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False)); return 1
    selected = [case for case in cases if not args.case or case["id"] == args.case]
    runs = []
    for case in selected:
        profiles = case["profiles"]
        if args.all_profiles:
            chosen = profiles
        elif args.profile == "auto":
            chosen = [sorted(profiles, key=lambda p: FIDELITY_ORDER.get(p["fidelity"], 99))[0]]
        else:
            chosen = [p for p in profiles if p["id"] == args.profile]
        for profile in chosen:
            if profile["kind"] == "real" and not args.allow_real:
                runs.append({"case_id": case["id"], "profile_id": profile["id"], "kind": "real", "fidelity": profile["fidelity"], "ok": False, "blocked": "--allow-real required", "cleanup_ok": True, "phases": {}})
            else:
                profile = {**profile, "allow_real": args.allow_real}
                runs.append(run_profile(case, profile, Path(args.repo).resolve()))
    report = {"schema_version": "opc-benchmark-report-v1", "ok": bool(runs) and all(r["ok"] for r in runs), "runs": runs}
    if args.out:
        out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
        (out / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        (out / "report.html").write_text(html_report(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
