---
name: architect
description: "Use after the PRD gate is Approved — typically after pulling a feature branch handed off by the product owner — to run architecture intake and produce the gated technical design: ADR-style TD records with reversibility tags, public contracts, system boundaries, runtime evidence plan, risk spikes, thin slice. Ends at the architecture sign-off touchpoint."
license: MIT
---

# architect

The engineering taste document. Starts with intake — understand before designing — because in a
duo the architect was not in the room when the requirement and PRD were shaped.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/technical-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/risk-readiness.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/technical.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Process

1. **Intake** (skippable when the same person just ran `prd`): pull the feature branch; verify
   PRD/demo gate freshness (`check_freshness.py`); read the owning domain's living spec
   (`docs/opc/specs/`, when it exists) for the current system truth, then requirement.md and
   prd.md; exercise the demo. Produce an intake note: what the feature does, the ACs that constrain architecture, and
   any understanding questions. Questions route to the product owner as `revise` (PRD/requirement
   wrong or incomplete) or get answered from artifacts — never silently self-answered.
2. **Risk spike**: if the risk profile has categories and no `risk-spike.md` yet, run the
   time-boxed spike now (`risk-readiness.md`). Technical decisions made before the spike are
   guesses.
3. Commit to one route. Write `technical.md` per the format: numbered TD records with
   reversibility tags, public contracts, system boundaries, the runtime evidence plan written
   against the project's actual observability, thin-slice designation. Inspect the codebase for
   the architecture baseline; divergence is a `[ONE-WAY]` TD record.
4. Gate it (fresh reviewer, `rubrics/technical.md`, L0 precheck). Fix-and-re-gate until
   Approved. Ledger each round.
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
