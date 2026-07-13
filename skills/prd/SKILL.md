---
name: prd
description: "Use after an Approved demo as the mandatory product-contract phase before testcase and build. Produces numbered PD/AC records and demo alignment only; black-box cases belong to the separate testcase phase."
license: MIT
---

# prd

Record durable product truth. Owned by whoever holds product judgment — the PM in a duo, the
builder solo. Ends with a pushed branch when another person must pick it up.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/prd-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- For the sign-off rendering: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/prd.md`

## Process

1. Require the running demo, `demo/prototype.md`, `demo/mock-inventory.md`, and a fresh Approved
   `reviews/demo-review.md`. Exercise the demo before writing product truth. Missing or stale demo
   is blocking, not an optional gap.
2. From those inputs and the human's durable product decisions, write `prd.md` per the
   format. Before writing ACs, check the owning domain's living spec (`docs/opc/specs/`, when it
   exists) for conflicts with existing system behavior — a new AC that contradicts a live one
   must declare the supersession explicitly. ACs are the spine — every contractual demo
   behavior, acceptance signal, and edge case maps to a numbered AC. The decision sheet stays ≤2 pages; contested decisions get numbered PD
   records with the five-piece set; product one-way doors are tagged.
3. Gate the PRD alone (fresh reviewer, `rubrics/prd.md`, L0 precheck via
   `validate_artifacts.py <prd>`). Repair and re-review until it passes or returns to a genuine
   product-decision blocker. Ledger each round; no fixed round quota applies.
4. **Product sign-off touchpoint**: write faithful plain-language `reports/prd.md` with source
   artifact SHAs, render/lint its `.html` companion per `report-style.md`, and present the decision
   sheet and demo-alignment table to the product owner. Two-way doors were decided and logged;
   `[ONE-WAY]` PD records need an explicit yes.
   Feedback routes tune/revise/park.
5. **Handoff when needed**: commit and push. Print branch, entry point, AC count, open questions,
   risk profile, and gaps. Continue to `testcase`; architecture is considered after testcase.

## Fail-open

Product questions the available inputs cannot answer go back to the product owner as five-piece
decisions—never guessed. An absent demo blocks this phase; claiming interaction taste was exercised
when it was not is a defect.

## Output

`prd.md` (PD/AC numbered), HTML sign-off report, pushed feature branch, handoff summary, ledger
entries. Next: `testcase`.
