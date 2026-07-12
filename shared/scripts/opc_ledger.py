#!/usr/bin/env python3
"""Append, meter, audit, and summarize OPC ledgers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import uuid
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

from opc_usage import capture_usage, usage_delta

SCHEMA_V2 = "opc-ledger-v2"
FEATURE_TYPES = {
    "gate": {"gate", "status"}, "rework": {"id", "routed_to", "source"},
    "change": {"source", "note"}, "evidence": {"ac", "label"},
    "decision": {"id", "door"}, "gap": {"id", "verb", "blocks", "label_cap", "state"},
    "dispatch": {"contract", "mode"}, "release": {"stage", "result"}, "park": {"note"},
}
LEGACY_REQUIRED = {
    **FEATURE_TYPES,
    "rework": {"routed_to", "source"}, "gap": {"verb", "blocks"},
}
EVIDENCE_LABELS = {"mock passed", "seeded passed", "local real service passed", "external provider passed", "human accepted", "long-run passed", "not run", "pending", "blocked"}
ERROR_TAGS = {"env-assumption", "api-misuse", "stale-knowledge", "missing-project-rule", "spec-gap", "test-blindspot", "taste-misjudgment", "harness-gap"}
RULE_STATES = {"proposed", "approved", "implemented", "verified", "active-unmeasured", "effective", "recurring", "strengthened", "retired"}
RELEASE_STAGES = {"manifest", "env-test", "deploy-test", "regression-test", "acceptance-test", "preflight", "env-prod", "deploy-prod", "regression-prod", "watch"}


def fail(message: str) -> int:
    print(f"ERROR: {message}", file=sys.stderr); return 1


def validate(entry: dict, is_error: bool, strict: bool = True) -> str | None:
    if is_error:
        missing = {"symptom", "tag", "root_cause"} - entry.keys()
        if missing: return f"error-ledger record missing fields: {sorted(missing)}"
        if entry["tag"] not in ERROR_TAGS: return f"unknown error tag {entry['tag']!r}"
        return None
    etype = entry.get("type")
    if etype not in FEATURE_TYPES: return f"unknown entry type {etype!r}"
    required = FEATURE_TYPES[etype] if strict else LEGACY_REQUIRED[etype]
    missing = required - entry.keys()
    if missing: return f"{etype} entry missing fields: {sorted(missing)}"
    if etype == "evidence" and entry["label"] not in EVIDENCE_LABELS: return f"unknown evidence label {entry['label']!r}"
    if etype == "gap" and strict and entry.get("state") not in {"open", "resolved", "accepted"}: return "gap state must be open/resolved/accepted"
    if etype == "gate" and entry["status"] not in {"Approved", "Issues Found"}: return "gate status must be Approved or Issues Found"
    if etype == "release" and entry.get("stage") not in RELEASE_STAGES: return f"unknown release stage {entry.get('stage')!r}"
    if etype == "release" and entry.get("result") not in {"ok", "failed", "blocked"}: return "release result must be ok/failed/blocked"
    if "rule_state" in entry and entry["rule_state"] not in RULE_STATES: return f"unknown rule state {entry['rule_state']!r}"
    return None


def append_entry(ledger: Path, entry: dict, strict: bool = True) -> None:
    is_error = ledger.name == "error-ledger.jsonl"
    problem = validate(entry, is_error, strict)
    if problem: raise ValueError(problem)
    entry.setdefault("ts", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    if strict: entry.setdefault("schema_version", SCHEMA_V2)
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as handle: handle.write(json.dumps(entry, ensure_ascii=False) + "\n")


def state_dir(repo: Path) -> Path:
    proc = subprocess.run(["git", "rev-parse", "--git-path", "opc-spans"], cwd=repo, capture_output=True, text=True)
    path = Path(proc.stdout.strip()) if proc.returncode == 0 else repo / ".opc-spans"
    return path if path.is_absolute() else repo / path


def read_entries(ledger: Path) -> list[tuple[int, dict | None, str | None]]:
    rows = []
    if not ledger.exists(): return rows
    for number, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip(): continue
        try: rows.append((number, json.loads(line), None))
        except json.JSONDecodeError as exc: rows.append((number, None, str(exc)))
    return rows


def cmd_append(args) -> int:
    entry = json.loads(args.json)
    try: append_entry(Path(args.ledger), entry, not args.legacy)
    except ValueError as exc: return fail(str(exc))
    print(f"appended to {args.ledger}"); return 0


def cmd_span_start(args) -> int:
    entry = json.loads(args.json)
    if entry.get("type") not in {"gate", "dispatch"}: return fail("spans support gate or dispatch entries")
    span_id = f"span-{uuid.uuid4().hex[:16]}"
    repo = Path(args.repo).resolve(); directory = state_dir(repo); directory.mkdir(parents=True, exist_ok=True)
    state = {"span_id": span_id, "ledger": str(Path(args.ledger).resolve()), "entry": entry, "started_at": datetime.now(timezone.utc).isoformat(), "started_ns": time.time_ns(), "usage_start": capture_usage(args.usage_source, args.usage_input)}
    path = directory / f"{span_id}.json"; path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"span_id": span_id, "state_path": str(path)}, ensure_ascii=False)); return 0


def cmd_span_end(args) -> int:
    repo = Path(args.repo).resolve(); path = state_dir(repo) / f"{args.span}.json"
    if not path.exists(): return fail(f"span not found: {args.span}")
    state = json.loads(path.read_text(encoding="utf-8")); entry = {**state["entry"], **json.loads(args.json)}
    entry["wall_secs"] = round(max(0, time.time_ns() - int(state["started_ns"])) / 1_000_000_000, 3)
    end = capture_usage(args.usage_source, args.usage_input); delta = usage_delta(state.get("usage_start"), end)
    if delta:
        entry["token_usage"] = delta; entry["tokens_est"] = delta["total_tokens"]
        entry["cost_source"] = end.get("source"); entry["session_id"] = end.get("session_id")
    else: entry["cost_source"] = "wall-only"
    if args.child_session: entry["child_session_ids"] = args.child_session
    try: append_entry(Path(state["ledger"]), entry, True)
    except ValueError as exc: return fail(str(exc))
    path.unlink(); print(json.dumps(entry, ensure_ascii=False)); return 0


def audit_ledger(ledger: Path, enforce_from: str | None = None) -> dict:
    threshold = datetime.fromisoformat(enforce_from).timestamp() if enforce_from else None
    errors, warnings = [], []
    for line, entry, parse_error in read_entries(ledger):
        if parse_error:
            errors.append({"line": line, "code": "invalid_json", "message": parse_error}); continue
        strict = entry.get("schema_version") == SCHEMA_V2
        problem = validate(entry, ledger.name == "error-ledger.jsonl", strict)
        if not problem: continue
        finding = {"line": line, "code": problem.split(":", 1)[0].replace(" ", "_"), "message": problem, "ts": entry.get("ts")}
        timestamp = datetime.fromisoformat(entry["ts"]).timestamp() if entry.get("ts") else None
        (errors if strict or threshold is None or timestamp is None or timestamp >= threshold else warnings).append(finding)
    return {"ok": not errors, "ledger": str(ledger), "errors": errors, "warnings": warnings}


def cmd_audit(args) -> int:
    report = audit_ledger(Path(args.ledger), args.enforce_from); print(json.dumps(report, ensure_ascii=False, indent=2)); return 0 if report["ok"] else 1


def cmd_summary(args) -> int:
    entries = [entry for _, entry, error in read_entries(Path(args.ledger)) if entry and not error]
    by_type = Counter(entry.get("type", entry.get("tag", "unknown")) for entry in entries)
    phases = defaultdict(lambda: {"entries": 0, "wall_secs": 0.0, "tokens": 0, "cost_coverage": 0})
    for entry in entries:
        if entry.get("type") not in {"gate", "dispatch"}: continue
        key = entry.get("phase") or entry.get("gate") or entry.get("contract") or "unknown"
        phases[key]["entries"] += 1; phases[key]["wall_secs"] += float(entry.get("wall_secs", 0)); phases[key]["tokens"] += int(entry.get("token_usage", {}).get("total_tokens", entry.get("tokens_est", 0)) or 0)
        if "wall_secs" in entry: phases[key]["cost_coverage"] += 1
    report = {"ledger": args.ledger, "entries": len(entries), "by_type": dict(by_type), "phases": dict(phases)}
    if args.json: print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"{args.ledger}: {len(entries)} entries")
        for key, count in by_type.most_common(): print(f"  {key}: {count}")
        for key, data in phases.items(): print(f"  phase {key}: wall={data['wall_secs']:.3f}s tokens={data['tokens']} cost={data['cost_coverage']}/{data['entries']}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(); sub = parser.add_subparsers(dest="command", required=True)
    app = sub.add_parser("append"); app.add_argument("--ledger", required=True); app.add_argument("--json", required=True); app.add_argument("--legacy", action="store_true"); app.set_defaults(func=cmd_append)
    start = sub.add_parser("span-start"); start.add_argument("--ledger", required=True); start.add_argument("--json", required=True); start.add_argument("--repo", default="."); start.add_argument("--usage-source", default="auto"); start.add_argument("--usage-input"); start.set_defaults(func=cmd_span_start)
    end = sub.add_parser("span-end"); end.add_argument("--span", required=True); end.add_argument("--json", required=True); end.add_argument("--repo", default="."); end.add_argument("--usage-source", default="auto"); end.add_argument("--usage-input"); end.add_argument("--child-session", action="append"); end.set_defaults(func=cmd_span_end)
    audit = sub.add_parser("audit"); audit.add_argument("--ledger", required=True); audit.add_argument("--enforce-from"); audit.set_defaults(func=cmd_audit)
    summary = sub.add_parser("summary"); summary.add_argument("--ledger", required=True); summary.add_argument("--json", action="store_true"); summary.set_defaults(func=cmd_summary)
    args = parser.parse_args(); return args.func(args)


if __name__ == "__main__": raise SystemExit(main())
