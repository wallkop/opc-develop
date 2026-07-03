#!/usr/bin/env python3
"""Verify a feature's full gate chain: every expected review exists, is Approved, and is fresh.

Expected reviews under <feature-dir>/reviews/:
  requirement-review.md, prd-review.md, technical-review.md, e2e-review.md   (always)
  demo-review.md                       (when <feature-dir>/demo/ exists)
  impl-contract-review.md              (when <feature-dir>/contracts/ exists)
  C-XX-implementation-review.md        (one per <feature-dir>/contracts/C-*.md)

Each review must contain exactly one `**Status:** Approved` line and >=1 Reviewed-SHA line whose
recorded content hash matches the current file (git hash-object).

Usage:
  check_gate_chain.py docs/features/7-export [--repo-root .] [--skip demo] [--skip e2e]

`--skip <name>` accepts a recorded, human-visible exception (e.g. no demo layer); each skip is
printed so it can't pass silently. Exit codes: 0 chain intact, 1 broken, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(Approved|Issues Found)\s*$", re.M)
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


def check_review(review: Path, root: Path) -> list[str]:
    problems: list[str] = []
    if not review.exists():
        return [f"missing review: {review.name}"]
    text = review.read_text(encoding="utf-8")
    statuses = STATUS_RE.findall(text)
    if len(statuses) != 1:
        problems.append(f"{review.name}: expected exactly one status line, found {len(statuses)}")
    elif statuses[0] != "Approved":
        problems.append(f"{review.name}: status is Issues Found")
    records = list(REVIEWED_RE.finditer(text))
    if not records:
        problems.append(f"{review.name}: no Reviewed-SHA lines — freshness unverifiable")
    for match in records:
        artifact = root / match.group("path")
        if not artifact.exists():
            problems.append(f"{review.name}: reviewed file missing: {match.group('path')}")
            continue
        current = git_hash(artifact)
        if current is None:
            problems.append(f"{review.name}: git unavailable")
            break
        recorded = match.group("sha")
        if not current.startswith(recorded):
            problems.append(
                f"{review.name}: {match.group('path')} stale "
                f"(recorded {recorded[:12]} != current {current[:12]})"
            )
    return problems


def expected_reviews(feature_dir: Path) -> list[str]:
    names = ["requirement-review.md", "prd-review.md", "technical-review.md"]
    if (feature_dir / "demo").exists():
        names.insert(1, "demo-review.md")
    if (feature_dir / "contracts").exists():
        names.append("impl-contract-review.md")
        for contract in sorted((feature_dir / "contracts").glob("C-*.md")):
            names.append(f"{contract.stem.split('-', 2)[0]}-{contract.stem.split('-', 2)[1]}-implementation-review.md")
    names.append("e2e-review.md")
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("feature_dir", help="feature directory, e.g. docs/features/7-export")
    parser.add_argument("--repo-root", default=".", help="base for Reviewed-SHA relative paths")
    parser.add_argument("--skip", action="append", default=[],
                        help="review name (without -review.md) to skip, with a recorded reason")
    args = parser.parse_args()

    feature_dir = Path(args.feature_dir)
    if not feature_dir.exists():
        print(f"ERROR: no feature directory at {feature_dir}", file=sys.stderr)
        return 2
    root = Path(args.repo_root)
    reviews_dir = feature_dir / "reviews"

    problems: list[str] = []
    checked = 0
    for name in expected_reviews(feature_dir):
        short = name.replace("-review.md", "")
        if short in args.skip:
            print(f"SKIPPED (declared exception): {name}")
            continue
        problems.extend(check_review(reviews_dir / name, root))
        checked += 1

    if problems:
        print(f"GATE CHAIN BROKEN: {feature_dir}", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    print(f"GATE CHAIN INTACT: {feature_dir} ({checked} reviews verified, "
          f"{len(args.skip)} declared skips)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
