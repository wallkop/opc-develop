#!/usr/bin/env python3
"""Extract the status token (and Reviewed-SHA records) from a review file.

Prints `Approved` or `Issues Found` on stdout. Exit codes:
  0 Approved, 3 Issues Found, 1 malformed (zero or multiple status lines), 2 usage error.

With --json, prints {"status": ..., "reviewed": [{"path":..., "sha":...}]}.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(Approved|Issues Found)\s*$", re.M)
REVIEWED_RE = re.compile(r"^Reviewed-SHA:\s+(?P<path>\S+)\s+(?P<sha>[0-9a-f]{7,64})\s*$", re.M)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.review)
    if not path.exists():
        print(f"ERROR: no review file at {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    statuses = STATUS_RE.findall(text)
    if len(statuses) != 1:
        print(
            f"ERROR: expected exactly one '**Status:**' line, found {len(statuses)} in {path}",
            file=sys.stderr,
        )
        return 1

    status = statuses[0]
    if args.json:
        reviewed = [
            {"path": m.group("path"), "sha": m.group("sha")}
            for m in REVIEWED_RE.finditer(text)
        ]
        print(json.dumps({"status": status, "reviewed": reviewed}))
    else:
        print(status)
    return 0 if status == "Approved" else 3


if __name__ == "__main__":
    raise SystemExit(main())
