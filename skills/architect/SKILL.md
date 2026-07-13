---
name: architect
description: "Use after approved testcase artifacts only when an increment changes a public boundary, makes a one-way technical decision, or has an explicit product-to-architecture handoff. Produces a gated ADR-style design before build."
license: MIT
---

# architect

The engineering decision document. Start with intake because the architect may not have shaped the
approved testcase chain and result card.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/technical-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/risk-readiness.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/technical.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Process

1. **Intake**: pull the branch; require fresh approved demo, PRD, and testcase artifacts, then read
   the result card, current code/architecture, and living spec. Exercise the existing
   real entry or demo when relevant. Record the outcome, constraints, and understanding questions;
   never silently answer missing product judgment.
2. **Matching risk spike**: run only the smallest real experiment that could invalidate this public
   or one-way decision. Do not estimate it or spike every category by default.
3. Commit to one route. Write `technical.md` per the format: numbered TD records with
   reversibility tags, public contracts, system boundaries, the runtime evidence plan written
   against the project's actual observability and core-slice impact. Inspect the codebase for
   the architecture baseline; divergence is a `[ONE-WAY]` TD record.
4. Gate it (fresh reviewer, `rubrics/technical.md`, L0 precheck). Repair and re-review until it
   passes or reaches a genuine decision blocker. Ledger each round; no fixed round quota applies.
5. **Architecture sign-off touchpoint**: write `reports/technical.md` as a faithful plain-language
   summary with the technical artifact SHA, render/lint `reports/technical.html` per
   `formats/report-style.md`, then present the TD decision sheet to the human architect.
   Every `[ONE-WAY]` record needs an explicit yes; questions get evidence-backed answers or
   become decision-spikes. Feedback routes tune/revise/park; report regenerates with the md.
6. Commit and push the updated feature branch.

## Fail-open

An unresolvable baseline conflict (competing datastores, contradictory conventions) goes to the
human as a five-piece decision. Missing observability for the evidence plan: write the plan
against what should exist, record `gap` entries (verb: observe) for `harness`, note the label
caps. Cross-role revises carry an `actor` field in the ledger so ownership is visible.

## Output

Intake note, `risk-spike.md` when applicable, `technical.md` (gated), sign-off recorded, pushed
branch. Next: `build`.
