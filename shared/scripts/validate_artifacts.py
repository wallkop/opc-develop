#!/usr/bin/env python3
"""Structural validation for opc artifacts (gate L0 precheck).

Detects artifact type from the filename and checks required structure:
  feature-plan.md  <=150 lines, budget/class fields, one core journey, bounded slices
  requirement.md   Decision Summary present, <=150 lines
  prd.md           Decision Sheet + Acceptance Criteria with AC-N ids, no duplicate ids
  testcases.md     TC metadata, Given/When/Then, AC coverage, browser-driven UI actions
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
REVIEWED_RE = re.compile(r"^Reviewed-SHA:\s+\S+\s+[0-9a-f]{7,64}\s*$", re.M)
FIELD_RE_TEMPLATE = r"^{name}:\s*(\S.*)$"
SLICE_RE = re.compile(r"^Slice-(\d+):\s*(\d+)\s*\|\s*(\S.*?)\s*\|\s*(\S.*?)\s*$", re.M)
TC_HEADER_RE = re.compile(r"^###\s+(TC-\d+):(?P<header>.*)$", re.M)
COVERAGE_RE = re.compile(r"^\|\s*(AC-\d+)\s*\|\s*([^|]+?)\s*\|\s*$", re.M)
TC_REF_RE = re.compile(r"\bTC-\d+\b")
MOCK_ID_RE = re.compile(r"^- id:\s*(M-\d+)\s*$", re.M)
MOCK_RETIREMENT_RE = re.compile(
    r"^Mock-Retirement:\s*(M-\d+)\s*\|\s*(Slice-\d+)\s*\|\s*(\S.*?)\s*\|\s*(\S.*?)\s*$",
    re.M,
)
CONSTRAINT_RE = re.compile(
    r"^Constraint:\s*((?:AC|TD)-\d+)\s*\|\s*(Slice-\d+)\s*\|\s*(\S.*?)\s*$", re.M,
)


def field(text: str, name: str) -> str | None:
    match = re.search(FIELD_RE_TEMPLATE.format(name=re.escape(name)), text, re.M)
    return match.group(1).strip() if match else None


def check_feature_plan(
    text: str, findings: list[str], mock_inventory_text: str | None = None,
    prd_text: str | None = None, technical_text: str | None = None,
) -> None:
    lines = len(text.splitlines())
    if lines > 150:
        findings.append(f"feature-plan.md is {lines} lines (cap 150)")

    required_sections = (
        (("## Outcome", "## 结果", "## 目标"), "Outcome / 结果"),
        (("## Core Journey", "## 核心旅程"), "Core Journey / 核心旅程"),
        (("## Slices", "## 切片", "## 实现切片"), "Slices / 切片"),
        (("## Acceptance", "## 验收"), "Acceptance / 验收"),
    )
    for aliases, label in required_sections:
        count = sum(
            len(re.findall(rf"^{re.escape(section)}\s*$", text, re.M))
            for section in aliases
        )
        if count == 0:
            findings.append(f"missing '{label}' section")
        elif count > 1:
            findings.append(f"expected exactly one '{label}' section, found {count}")

    required_fields = (
        "Plan-Version", "Class", "Budget-Minutes", "User-Action", "Entry-Point",
        "Success-Signal", "Non-Goals", "Journey-Type", "Given", "When", "Then",
        "Production-Assembly", "Data-Kind", "Data-Source", "Safety-1", "Safety-2",
        "Build-Command", "Core-Command",
    )
    values = {name: field(text, name) for name in required_fields}
    for name, value in values.items():
        occurrences = re.findall(rf"^{re.escape(name)}:\s*(.*)$", text, re.M)
        if not value:
            findings.append(f"missing or empty {name} field")
        if len(occurrences) > 1:
            findings.append(f"expected exactly one {name} field, found {len(occurrences)}")

    data_hash_occurrences = re.findall(r"^Data-Hash:\s*(.*)$", text, re.M)
    if len(data_hash_occurrences) > 1:
        findings.append(f"expected at most one Data-Hash field, found {len(data_hash_occurrences)}")

    if values.get("Plan-Version") not in {None, "opc-increment-v1"}:
        findings.append("Plan-Version must be opc-increment-v1")

    flow_class = values.get("Class")
    if flow_class not in {None, "quick", "standard", "split"}:
        findings.append("Class must be quick, standard, or split")

    budget: int | None = None
    raw_budget = values.get("Budget-Minutes")
    if raw_budget:
        try:
            budget = int(raw_budget)
            if budget <= 0:
                raise ValueError
        except ValueError:
            findings.append("Budget-Minutes must be a positive integer")
        else:
            if flow_class == "quick" and budget > 60:
                findings.append("quick increments have a 60-minute budget cap")
            if flow_class == "standard" and not 61 <= budget <= 240:
                findings.append("standard increments require a 61-240 minute budget; use quick or split")
            if flow_class == "split" and budget <= 240:
                findings.append("split classification is only for work above 240 minutes")

    journey_type = values.get("Journey-Type")
    if journey_type not in {None, "ui", "api", "cli", "job"}:
        findings.append("Journey-Type must be ui, api, cli, or job")
    data_kind = values.get("Data-Kind")
    if data_kind not in {None, "synthetic", "snapshot", "real"}:
        findings.append("Data-Kind must be synthetic, snapshot, or real")
    if data_kind in {"snapshot", "real"} and not field(text, "Data-Hash"):
        findings.append("snapshot/real data requires Data-Hash provenance")

    slices = [(int(number), int(minutes), result, proof)
              for number, minutes, result, proof in SLICE_RE.findall(text)]
    if not slices:
        findings.append("no Slice-N entries; use 'Slice-1: <minutes> | <user result> | <black-box proof>'")
    else:
        numbers = [item[0] for item in slices]
        if numbers != list(range(1, len(numbers) + 1)):
            findings.append(f"slice ids must be consecutive from 1, found {numbers}")
        if flow_class == "split":
            for number, minutes, _, _ in slices:
                if minutes > 240:
                    findings.append(f"Slice-{number} exceeds the 240-minute standard-increment cap")
        else:
            if slices[0][1] > 45:
                findings.append("Slice-1 must reach a runnable core path within 45 minutes")
            for number, minutes, _, _ in slices[1:]:
                if minutes > 90:
                    findings.append(f"Slice-{number} exceeds the 90-minute increment cap")
        if budget is not None and sum(item[1] for item in slices) > budget:
            findings.append("slice estimates exceed Budget-Minutes")

    retirement_rows = MOCK_RETIREMENT_RE.findall(text)
    retirement_ids = [row[0] for row in retirement_rows]
    if len(retirement_ids) != len(set(retirement_ids)):
        findings.append("duplicate Mock-Retirement ids")
    slice_ids = {f"Slice-{number}" for number, _, _, _ in slices}
    for mock_id, slice_id, _, _ in retirement_rows:
        if slice_id not in slice_ids:
            findings.append(f"{mock_id} retirement references missing {slice_id}")
    if mock_inventory_text is not None:
        inventory_ids = set(MOCK_ID_RE.findall(mock_inventory_text))
        mapped_ids = set(retirement_ids)
        if inventory_ids and not any(
            heading in text for heading in ("## Mock Retirement", "## 模拟退役", "## 模拟淘汰")
        ):
            findings.append("demo mock inventory requires a 'Mock Retirement' section")
        missing = inventory_ids - mapped_ids
        extra = mapped_ids - inventory_ids
        if missing:
            findings.append(f"mock inventory entries missing retirement mappings: {sorted(missing)}")
        if extra:
            findings.append(f"retirement mappings reference unknown mocks: {sorted(extra)}")

    constraints = CONSTRAINT_RE.findall(text)
    if (prd_text is not None or technical_text is not None) and not constraints:
        findings.append("optional PRD/technical inputs require explicit Constraint rows")
    known_constraints: set[str] = set()
    if prd_text is not None:
        section = AC_SECTION_RE.search(prd_text)
        if section:
            known_constraints |= set(AC_ACTIVE_RE.findall(section.group(1)))
    if technical_text is not None:
        known_constraints |= set(TD_ANY_RE.findall(technical_text))
    for constraint_id, slice_id, _ in constraints:
        if slice_id not in slice_ids:
            findings.append(f"{constraint_id} constraint references missing {slice_id}")
        if known_constraints and constraint_id not in known_constraints:
            findings.append(f"constraint references unknown optional record {constraint_id}")


def check_testcases(text: str, findings: list[str], prd_text: str | None = None) -> None:
    headers = list(TC_HEADER_RE.finditer(text))
    if not headers:
        findings.append("no TC-N cases found")
        return

    case_ids = [match.group(1) for match in headers]
    dupes = {tc for tc in case_ids if case_ids.count(tc) > 1}
    if dupes:
        findings.append(f"duplicate TC ids: {sorted(dupes)}")

    cases: dict[str, set[str]] = {}
    for index, match in enumerate(headers):
        tc_id = match.group(1)
        header = match.group("header")
        end = headers[index + 1].start() if index + 1 < len(headers) else len(text)
        body = text[match.end():end]
        level_match = re.search(r"\[level:\s*(api|ui-e2e)\]", header)
        seed_match = re.search(r"\[seed:\s*seed:([^\]\s]+)\]", header)
        acs = set(AC_REF_RE.findall(header))
        if not level_match:
            findings.append(f"{tc_id} missing [level: api|ui-e2e]")
        if not seed_match:
            findings.append(f"{tc_id} missing named [seed: seed:<name>]")
        if not acs:
            findings.append(f"{tc_id} references no AC ids")
        cases[tc_id] = acs
        for aliases, label in (
            ((r"^Given\s+\S", r"^给定\s*\S"), "Given / 给定"),
            ((r"^When\s+\S", r"^当\s*\S"), "When / 当"),
            ((r"^Then\s+\S", r"^(?:则|那么)\s*\S"), "Then / 则"),
        ):
            if not any(re.search(pattern, body, re.M) for pattern in aliases):
                findings.append(f"{tc_id} missing {label} step")
        if level_match and level_match.group(1) == "ui-e2e":
            if not re.search(r"^Driver-Action:\s*browser\s*\|\s*\S", body, re.M):
                findings.append(f"{tc_id} ui-e2e must declare a browser-driven Driver-Action")

    coverage: dict[str, set[str]] = {}
    for ac, tc_text in COVERAGE_RE.findall(text):
        coverage[ac] = set(TC_REF_RE.findall(tc_text))
    if not coverage:
        findings.append("coverage map has no AC rows")
    for ac, mapped in coverage.items():
        if not mapped:
            findings.append(f"coverage for {ac} names no TC cases")
        missing = mapped - set(cases)
        if missing:
            findings.append(f"coverage for {ac} references missing cases: {sorted(missing)}")
        for tc_id in mapped & set(cases):
            if ac not in cases[tc_id]:
                findings.append(f"coverage maps {ac} to {tc_id}, but the case does not reference {ac}")
    for tc_id, acs in cases.items():
        for ac in acs:
            if tc_id not in coverage.get(ac, set()):
                findings.append(f"coverage is missing {ac} -> {tc_id}")

    if prd_text is not None:
        section = AC_SECTION_RE.search(prd_text)
        if section:
            active = set(AC_ACTIVE_RE.findall(section.group(1)))
            missing = active - set(coverage)
            extra = set(coverage) - active
            if missing:
                findings.append(f"coverage missing active PRD ACs: {sorted(missing)}")
            if extra:
                findings.append(f"coverage references non-active PRD ACs: {sorted(extra)}")


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
        (("## Local Notes", "## Internal Design", "## 本地说明", "## 内部设计"), "Local Notes / 本地说明"),
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
    if name == "feature-plan.md":
        inventory = path.parent / "demo" / "mock-inventory.md"
        inventory_text = inventory.read_text(encoding="utf-8") if inventory.exists() else None
        prd = path.parent / "prd.md"
        technical = path.parent / "technical.md"
        check_feature_plan(
            text, findings, inventory_text,
            prd.read_text(encoding="utf-8") if prd.exists() else None,
            technical.read_text(encoding="utf-8") if technical.exists() else None,
        )
    elif name == "requirement.md":
        check_requirement(text, findings)
    elif name == "prd.md":
        check_prd(text, findings)
    elif name == "testcases.md":
        prd_text = None
        if args.prd:
            prd = Path(args.prd)
            if prd.exists():
                prd_text = prd.read_text(encoding="utf-8")
            else:
                findings.append(f"--prd path does not exist: {prd}")
        check_testcases(text, findings, prd_text)
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
