#!/usr/bin/env python3
"""Pre-group the error ledger for retro's recurrence detection.

Groups resolved-failure records by (tag, normalized pattern string) and reports clusters with
>= --threshold occurrences (default 2). This is exact-match PRE-GROUPING only: two semantically
identical failures phrased differently will land in different groups. The retro agent must
semantically cluster ACROSS the pre-groups (especially within a tag) before concluding anything
is non-recurring — treat this script's output as a starting index, not the verdict.

Usage:
  recurrence_scan.py docs/opc/error-ledger.jsonl [--threshold 2] [--json]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path


def normalize(pattern: str) -> str:
    return re.sub(r"\s+", " ", pattern.strip().lower())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledger")
    parser.add_argument("--threshold", type=int, default=2)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ledger = Path(args.ledger)
    if not ledger.exists():
        print(f"No error ledger at {ledger} — nothing to scan.")
        return 0

    records = []
    for i, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError:
            print(f"WARN: line {i} invalid JSON, skipped", file=sys.stderr)

    clusters: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for rec in records:
        tag = rec.get("tag", "untagged")
        key_pattern = normalize(rec.get("pattern") or rec.get("root_cause", ""))
        clusters[(tag, key_pattern)].append(rec)

    recurring = {
        key: recs for key, recs in clusters.items() if len(recs) >= args.threshold
    }

    if args.json:
        out = [
            {
                "tag": tag,
                "pattern": pattern,
                "count": len(recs),
                "features": sorted({r.get("feature", "?") for r in recs}),
                "occurrences": [r.get("ts", "?") for r in recs],
                "sample_root_cause": recs[-1].get("root_cause", ""),
            }
            for (tag, pattern), recs in sorted(
                recurring.items(), key=lambda kv: -len(kv[1])
            )
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    print(f"{ledger}: {len(records)} records, {len(recurring)} recurring clusters "
          f"(threshold {args.threshold})")
    for (tag, pattern), recs in sorted(recurring.items(), key=lambda kv: -len(kv[1])):
        features = sorted({r.get("feature", "?") for r in recs})
        print(f"\n[{tag}] x{len(recs)} — {pattern or '(no pattern)'}")
        print(f"  features: {', '.join(features)}")
        print(f"  latest root cause: {recs[-1].get('root_cause', '')}")
        print("  -> rule-crystallization candidate: propose L0 check first, prose last")
    if not recurring:
        print("No recurring clusters. Nothing to crystallize this round.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
