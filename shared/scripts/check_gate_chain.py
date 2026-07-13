#!/usr/bin/env python3
"""Verify a feature's full gate chain: every expected review exists, is Approved, and is fresh.

Expected reviews under <feature-dir>/reviews/:
  demo-review.md, prd-review.md, testcase-review.md,
  reality-review.md, final-review.md      (standard increment with feature-plan.md)
  requirement-review.md, prd-review.md, technical-review.md, e2e-review.md   (always)
  demo-review.md                       (when <feature-dir>/demo/ exists)
  impl-contract-review.md              (when <feature-dir>/contracts/ exists)
  C-XX-implementation-review.md        (one per <feature-dir>/contracts/C-*.md)

Each review must contain exactly one `**Status:** Approved` line and >=1 Reviewed-SHA line whose
recorded content hash matches the current file (git hash-object).

Usage:
  check_gate_chain.py docs/features/7-export [--repo-root .] [--skip demo] [--skip e2e]

`--skip <name>` accepts a recorded, human-visible exception for legacy optional layers (e.g. no
demo); standard-increment reality/final reviews cannot be skipped. Exit codes: 0 chain intact,
1 broken, 2 usage error.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(Approved|Issues Found)\s*$", re.M)
REVIEWED_RE = re.compile(r"^Reviewed-SHA:\s+(?P<path>\S+)\s+(?P<sha>[0-9a-f]{7,64})\s*$", re.M)
REVISION_RE = re.compile(r"^Reviewed-Revision:\s+(?P<revision>(?:[0-9a-f]{40}|[0-9a-f]{64}))\s*$", re.M)


def git_hash(path: Path, root: Path) -> str | None:
    try:
        out = subprocess.run(
            ["git", "hash-object", str(path)],
            cwd=root,
            capture_output=True, text=True, check=True,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None
    return out.stdout.strip()


def check_review(
    review: Path, root: Path, current_revision: str | None = None,
    require_revision: bool = False, allowed_revisions: set[str] | None = None,
) -> list[str]:
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
        current = git_hash(artifact, root)
        if current is None:
            problems.append(f"{review.name}: git unavailable")
            break
        recorded = match.group("sha")
        if not current.startswith(recorded):
            problems.append(
                f"{review.name}: {match.group('path')} stale "
                f"(recorded {recorded[:12]} != current {current[:12]})"
            )
    if require_revision or current_revision is not None:
        revisions = REVISION_RE.findall(text)
        if len(revisions) != 1:
            problems.append(f"{review.name}: expected exactly one Reviewed-Revision line")
        elif current_revision is not None and revisions[0] != current_revision:
            problems.append(
                f"{review.name}: reviewed revision stale "
                f"(recorded {revisions[0][:12]} != current {current_revision[:12]})"
            )
        elif allowed_revisions is not None and revisions[0] not in allowed_revisions:
            problems.append(
                f"{review.name}: Reviewed-Revision is not backed by a receipt command "
                f"({revisions[0][:12]})"
            )
    return problems


def increment_revision(
    feature_dir: Path, root: Path,
) -> tuple[str | None, set[str], str | None]:
    receipt = feature_dir / "acceptance.json"
    if not receipt.exists():
        return None, set(), "missing acceptance.json"
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
        if data.get("schema_version") != "opc-acceptance-v1":
            return None, set(), "acceptance.json has unsupported schema"
        from opc_increment import receipt_exclusions, tree_fingerprint
        revisions = {
            command.get("revision")
            for command in data.get("commands", [])
            if command.get("exit_code") == 0
            and command.get("core") is True
            and command.get("production_assembly") is True
            and command.get("evidence_complete") is True
            and command.get("mutated_worktree") is False
            and command.get("label") in {
                "local real service passed", "external provider passed", "long-run passed",
            }
            and isinstance(command.get("revision"), str)
            and re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", command["revision"])
        }
        resolved_root = root.resolve()
        return tree_fingerprint(
            resolved_root, receipt_exclusions(resolved_root, receipt.resolve(), data)
        ), revisions, None
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        return None, set(), f"cannot compute acceptance revision: {exc}"


def expected_reviews(feature_dir: Path) -> list[str]:
    if (feature_dir / "feature-plan.md").exists():
        return [
            "demo-review.md", "prd-review.md", "testcase-review.md",
            "reality-review.md", "final-review.md",
        ]
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
    root = Path(args.repo_root).resolve()
    reviews_dir = feature_dir / "reviews"
    standard_increment = (feature_dir / "feature-plan.md").exists()
    if standard_increment and args.skip:
        print(
            "ERROR: standard increment reality/final reviews are mandatory and cannot be skipped",
            file=sys.stderr,
        )
        return 2
    current_revision = None
    receipt_revisions: set[str] = set()

    problems: list[str] = []
    if standard_increment:
        current_revision, receipt_revisions, revision_problem = increment_revision(feature_dir, root)
        if revision_problem:
            problems.append(revision_problem)
        try:
            from opc_testcase import check_feature_ready
            check_feature_ready(root, feature_dir.resolve(), require_approved=True)
        except (ValueError, OSError) as exc:
            problems.append(f"testcase chain invalid: {exc}")
    checked = 0
    for name in expected_reviews(feature_dir):
        short = name.replace("-review.md", "")
        if short in args.skip:
            print(f"SKIPPED (declared exception): {name}")
            continue
        revision_bound = standard_increment and name in {"reality-review.md", "final-review.md"}
        revision = current_revision if revision_bound and name == "final-review.md" else None
        problems.extend(check_review(
            reviews_dir / name, root, revision,
            require_revision=revision_bound,
            allowed_revisions=receipt_revisions if revision_bound else None,
        ))
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
