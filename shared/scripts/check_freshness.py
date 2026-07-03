#!/usr/bin/env python3
"""Verify a review is fresh: its recorded Reviewed-SHA lines match current file content.

Review files record one line per reviewed artifact:
  Reviewed-SHA: <path> <sha>
where <sha> is `git hash-object <path>` at review time (content hash — survives checkout/rebase,
unlike mtimes).

Usage:
  check_freshness.py docs/features/7-export/reviews/prd-review.md
  check_freshness.py reviews/prd-review.md --repo-root /path/to/project

Exit codes: 0 fresh, 1 stale or malformed, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REVIEWED_RE = re.compile(r"^Reviewed-SHA:\s+(?P<path>\S+)\s+(?P<sha>[0-9a-f]{7,40})\s*$", re.M)


def git_hash(path: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "hash-object", str(path)],
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("review", help="review file containing Reviewed-SHA lines")
    parser.add_argument("--repo-root", default=".", help="base for relative artifact paths")
    args = parser.parse_args()

    review = Path(args.review)
    if not review.exists():
        print(f"STALE: review file missing: {review}", file=sys.stderr)
        return 1

    text = review.read_text(encoding="utf-8")
    records = list(REVIEWED_RE.finditer(text))
    if not records:
        print(f"STALE: no Reviewed-SHA lines in {review}", file=sys.stderr)
        return 1

    root = Path(args.repo_root)
    stale = []
    for match in records:
        artifact = root / match.group("path")
        recorded = match.group("sha")
        if not artifact.exists():
            stale.append(f"{match.group('path')}: file missing")
            continue
        current = git_hash(artifact)
        if current is None:
            print("ERROR: git unavailable; cannot verify freshness", file=sys.stderr)
            return 2
        if not current.startswith(recorded):
            stale.append(f"{match.group('path')}: recorded {recorded[:12]} != current {current[:12]}")

    if stale:
        print(f"STALE: {review}", file=sys.stderr)
        for line in stale:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"FRESH: {review} ({len(records)} artifacts verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
