#!/usr/bin/env python3
"""Append validated entries to opc ledgers, or summarize them.

Usage:
  opc_ledger.py append --ledger docs/features/7-export/ledger.jsonl \
      --json '{"type":"gate","gate":"prd","status":"Approved","rounds":1}'
  opc_ledger.py append --ledger docs/opc/error-ledger.jsonl --json '{...error record...}'
  opc_ledger.py summary --ledger docs/features/7-export/ledger.jsonl
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

FEATURE_TYPES = {
    "gate": {"gate", "status"},
    "rework": {"routed_to", "source"},
    "change": {"source", "note"},
    "evidence": {"ac", "label"},
    "decision": {"id", "door"},
    "gap": {"verb", "blocks"},
    "dispatch": {"contract", "mode"},
    "release": {"stage", "result"},
    "park": {"note"},
}

RELEASE_STAGES = {
    "manifest", "env-test", "deploy-test", "regression-test", "acceptance-test",
    "preflight", "env-prod", "deploy-prod", "regression-prod", "watch",
}

EVIDENCE_LABELS = {
    "mock passed", "seeded passed", "local real service passed",
    "external provider passed", "human accepted", "long-run passed",
    "not run", "pending", "blocked",
}

ERROR_TAGS = {
    "env-assumption", "api-misuse", "stale-knowledge", "missing-project-rule",
    "spec-gap", "test-blindspot", "taste-misjudgment", "harness-gap",
}

ERROR_REQUIRED = {"symptom", "tag", "root_cause"}


def fail(msg: str) -> int:
    print(f"ERROR: {msg}", file=sys.stderr)
    return 1


def validate(entry: dict, is_error_ledger: bool) -> str | None:
    if is_error_ledger:
        missing = ERROR_REQUIRED - entry.keys()
        if missing:
            return f"error-ledger record missing fields: {sorted(missing)}"
        if entry["tag"] not in ERROR_TAGS:
            return f"unknown error tag {entry['tag']!r}; allowed: {sorted(ERROR_TAGS)}"
        return None

    etype = entry.get("type")
    if etype not in FEATURE_TYPES:
        return f"unknown entry type {etype!r}; allowed: {sorted(FEATURE_TYPES)}"
    missing = FEATURE_TYPES[etype] - entry.keys()
    if missing:
        return f"{etype} entry missing fields: {sorted(missing)}"
    if etype == "evidence" and entry["label"] not in EVIDENCE_LABELS:
        return f"unknown evidence label {entry['label']!r}; allowed: {sorted(EVIDENCE_LABELS)}"
    if etype == "gate" and entry["status"] not in {"Approved", "Issues Found"}:
        return f"gate status must be 'Approved' or 'Issues Found', got {entry['status']!r}"
    if etype == "release":
        if entry["stage"] not in RELEASE_STAGES:
            return f"unknown release stage {entry['stage']!r}; allowed: {sorted(RELEASE_STAGES)}"
        if entry["result"] not in {"ok", "failed", "blocked"}:
            return f"release result must be ok/failed/blocked, got {entry['result']!r}"
    return None


def cmd_append(args: argparse.Namespace) -> int:
    try:
        entry = json.loads(args.json)
    except json.JSONDecodeError as exc:
        return fail(f"invalid JSON: {exc}")
    if not isinstance(entry, dict):
        return fail("entry must be a JSON object")

    ledger = Path(args.ledger)
    is_error_ledger = ledger.name == "error-ledger.jsonl"
    problem = validate(entry, is_error_ledger)
    if problem:
        return fail(problem)

    entry.setdefault("ts", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    ledger.parent.mkdir(parents=True, exist_ok=True)
    with ledger.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"appended to {ledger}")
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    ledger = Path(args.ledger)
    if not ledger.exists():
        return fail(f"no ledger at {ledger}")

    entries = []
    for i, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            entries.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"WARN: line {i} is not valid JSON, skipped", file=sys.stderr)

    by_type = Counter(e.get("type", e.get("tag", "unknown")) for e in entries)
    print(f"{ledger}: {len(entries)} entries")
    for key, count in by_type.most_common():
        print(f"  {key}: {count}")
    rework = Counter(e["routed_to"] for e in entries if e.get("type") == "rework")
    if rework:
        print("rework routing:")
        for layer, count in rework.most_common():
            print(f"  -> {layer}: {count}")
    labels = Counter(e["label"] for e in entries if e.get("type") == "evidence")
    if labels:
        print("evidence labels:")
        for label, count in labels.most_common():
            print(f"  {label}: {count}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p_append = sub.add_parser("append")
    p_append.add_argument("--ledger", required=True)
    p_append.add_argument("--json", required=True)
    p_summary = sub.add_parser("summary")
    p_summary.add_argument("--ledger", required=True)
    args = parser.parse_args()
    return cmd_append(args) if args.cmd == "append" else cmd_summary(args)


if __name__ == "__main__":
    raise SystemExit(main())
