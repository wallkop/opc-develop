#!/usr/bin/env python3
"""Structural validation for opc artifacts (gate L0 precheck).

Detects artifact type from the filename and checks required structure:
  requirement.md   Decision Summary present, <=150 lines
  prd.md           Decision Sheet + Acceptance Criteria with AC-N ids, no duplicate ids
  technical.md     Decision Records (TD-N with reversibility tags), Public Contracts,
                   Runtime Evidence Plan
  contracts/       index.md contract table; C-XX files have Boundary / TDD Seed / Done Means
  *-review.md      exactly one status token, >=1 Reviewed-SHA line

Cross-checks with --prd: contract AC references must exist in the PRD.

Exit codes: 0 ok, 1 findings, 2 usage error.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

AC_ACTIVE_RE = re.compile(r"^(?:[-*]\s*)?(AC-\d+)\s*:", re.M)
AC_STRUCK_RE = re.compile(r"^(?:[-*]\s*)?~~\s*(AC-\d+)", re.M)
AC_SECTION_RE = re.compile(
    r"^## (?:Acceptance Criteria|验收标准|验收条件)\s*$(.*?)(?=^## |\Z)", re.M | re.S
)
AC_REF_RE = re.compile(r"\bAC-\d+\b")
TD_RE = re.compile(r"^(?:#{2,3}\s+)?(TD-\d+)\s*:.*?\[(ONE-WAY|one-way|two-way)\]", re.M)
TD_ANY_RE = re.compile(r"^(?:#{2,3}\s+)?(TD-\d+)\s*:", re.M)
STATUS_RE = re.compile(r"^\*\*Status:\*\*\s+(Approved|Issues Found)\s*$", re.M)
REVIEWED_RE = re.compile(r"^Reviewed-SHA:\s+\S+\s+[0-9a-f]{7,40}\s*$", re.M)


def check_requirement(text: str, findings: list[str]) -> None:
    if not any(section in text for section in ("## Decision Summary", "## 决策摘要")):
        findings.append("missing decision-summary section ('Decision Summary' / '决策摘要')")
    lines = len(text.splitlines())
    if lines > 150:
        findings.append(f"requirement.md is {lines} lines (cap 150) — move detail out")
    if not any(marker in text for marker in ("Risk profile", "risk profile", "风险概况", "风险画像")):
        findings.append("no risk profile recorded")


def check_prd(text: str, findings: list[str]) -> None:
    if not any(section in text for section in ("## Decision Sheet", "## 决策表")):
        findings.append("missing decision-sheet section ('Decision Sheet' / '决策表')")
    section = AC_SECTION_RE.search(text)
    if not section:
        findings.append("missing acceptance-criteria section ('Acceptance Criteria' / '验收标准' / '验收条件')")
        return
    # AC definitions only count inside the AC section; struck-through lines are retired ids
    body = section.group(1)
    struck = set(AC_STRUCK_RE.findall(body))
    active = [
        ac for ac in AC_ACTIVE_RE.findall(
            "\n".join(l for l in body.splitlines() if not l.lstrip().lstrip("-* ").startswith("~~"))
        )
    ]
    if not active and not struck:
        findings.append("no AC-N acceptance criteria defined")
    dupes = {ac for ac in active if active.count(ac) > 1}
    if dupes:
        findings.append(f"duplicate AC ids: {sorted(dupes)}")
    reused = struck & set(active)
    if reused:
        findings.append(f"retired AC ids reused as active: {sorted(reused)} (never renumber)")


def check_technical(text: str, findings: list[str]) -> None:
    required_sections = (
        (("## Decision Records", "## 决策记录"), "decision records / 决策记录"),
        (("## Public Contracts", "## 公共契约"), "public contracts / 公共契约"),
        (("## Runtime Evidence Plan", "## 运行时证据计划"), "runtime evidence plan / 运行时证据计划"),
    )
    for aliases, label in required_sections:
        if not any(section in text for section in aliases):
            findings.append(f"missing '{label}' section")
    tds = TD_ANY_RE.findall(text)
    tagged = {m[0] for m in TD_RE.findall(text)}
    untagged = [td for td in tds if td not in tagged]
    if untagged:
        findings.append(f"decision records missing reversibility tag: {untagged}")
    if not tds:
        findings.append("no TD-N decision records found")


def check_contract(text: str, findings: list[str], name: str) -> None:
    if name == "index.md":
        if not re.search(r"^\|\s*C-\d+", text, re.M):
            findings.append("index.md has no contract table rows (| C-XX ...)")
        if "Integration steps" not in text:
            findings.append("index.md missing integration steps")
        return
    required_sections = (
        (("## Boundary", "## 边界"), "Boundary / 边界"),
        (("## TDD Seed", "## TDD 种子"), "TDD Seed / TDD 种子"),
        (("## Done Means", "## 完成标准"), "Done Means / 完成标准"),
    )
    for aliases, label in required_sections:
        if not any(section in text for section in aliases):
            findings.append(f"missing '{label}' section")
    if not AC_REF_RE.search(text):
        findings.append("contract references no AC ids")


def check_review(text: str, findings: list[str]) -> None:
    statuses = STATUS_RE.findall(text)
    if len(statuses) != 1:
        findings.append(f"expected exactly one '**Status:**' line, found {len(statuses)}")
    if not REVIEWED_RE.search(text):
        findings.append("no Reviewed-SHA lines — freshness cannot be verified")


def cross_check_acs(contract_text: str, prd_text: str, findings: list[str]) -> None:
    prd_acs: set[str] = set()
    section = AC_SECTION_RE.search(prd_text)
    if section:
        body = section.group(1)
        prd_acs = set(AC_ACTIVE_RE.findall(body)) | set(AC_STRUCK_RE.findall(body))
    for ref in set(AC_REF_RE.findall(contract_text)):
        if ref not in prd_acs:
            findings.append(f"references {ref}, which is not defined in the PRD")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact", help="artifact file to validate")
    parser.add_argument("--prd", help="PRD path for AC cross-checks (contracts only)")
    args = parser.parse_args()

    path = Path(args.artifact)
    if not path.exists():
        print(f"ERROR: no file at {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")

    findings: list[str] = []
    name = path.name
    if name == "requirement.md":
        check_requirement(text, findings)
    elif name == "prd.md":
        check_prd(text, findings)
    elif name == "technical.md":
        check_technical(text, findings)
    elif name.endswith("-review.md"):
        check_review(text, findings)
    elif path.parent.name == "contracts" or re.match(r"^C-\d+-", name) or (
        name == "index.md" and "contracts" in path.parts
    ):
        check_contract(text, findings, name)
        if args.prd:
            prd = Path(args.prd)
            if prd.exists():
                cross_check_acs(text, prd.read_text(encoding="utf-8"), findings)
            else:
                findings.append(f"--prd path does not exist: {prd}")
    else:
        print(f"NOTE: no structural rules for {name}; nothing checked")
        return 0

    if findings:
        print(f"FINDINGS in {path}:", file=sys.stderr)
        for f in findings:
            print(f"  - {f}", file=sys.stderr)
        return 1
    print(f"OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
