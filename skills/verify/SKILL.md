---
name: verify
description: "Use after build integration succeeds to prove the feature black-box: drives the app agentically against each AC, distills important verifications into committed Tier-1 E2E specs on named seeds, assembles evidence triangles with honest authenticity labels, checks demo parity, produces the acceptance sheet for the human touchpoint, and triages the human's verdict."
license: MIT
---

# verify

Prove behavior from the outside, then let the human judge. Every claim carries its authenticity
label; the harness caps what can be claimed, not optimism.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/harness-verbs.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/feedback-routing.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/e2e.md`

## Process

1. Precheck: build's gates fresh, stack starts per L1 (`run`), reset + seed per L2. Missing verbs
   ⇒ record `gap` entries and note the label caps they force.
2. **Agentic pass (Tier 2)**: drive the running app through every AC — browser tooling for UI,
   real requests for APIs. For each AC, assemble the evidence triangle: interface assertion,
   correlation-ID log chain, state assertion. Record per-AC `evidence` ledger entries with the
   honest label.
3. **Distill (Tier 1)**: every AC-proving interaction becomes a committed spec (Playwright or the
   project's equivalent), annotated with its AC-IDs and named seed. Run the full Tier-1 suite
   including pre-existing regression specs; capture output and exit codes.
4. **Demo parity**: exercise the contractual interactions from PRD Demo alignment against the
   real implementation; divergence is a finding (implementation defect or artifact defect —
   triage, don't assume).
5. Write the acceptance sheet to `docs/features/<slug>/acceptance.md` — one line per AC:
   verdict, label, evidence pointer, reproduction entry point; plus recorded gaps and their caps.
   The sheet is immutable after the gate; human verdicts go to the ledger, not into the sheet.
6. Gate the stage: fresh reviewer, `rubrics/e2e.md`, reviewing `acceptance.md` against coverage,
   seeds, triangles, label honesty, distillation, regression.
7. **Acceptance touchpoint**: present the gated acceptance sheet. The human exercises what they
   choose and returns a verdict, recorded as ledger entries (`evidence` with `human accepted`,
   or `rework`/`change`).
8. **Triage the verdict** per `feedback-routing.md`: implementation defect → `build` (targeted);
   artifact defect → `revise` + cascade; taste change → `change` ledger entry → `brainstorm`
   fast path. Ledger everything; rework entries carry `routed_to`.

## Fail-open

An environment that cannot reach a corner of the triangle downgrades the label and says so on the
acceptance sheet — a capped honest sheet beats a full-looking dishonest one. Computer-use style
verification stays advisory; the blocking evidence is Tier-1 output.

## Output

Committed Tier-1 specs, acceptance sheet, per-AC evidence ledger entries, human verdict recorded,
routed rework when any. Next: `ship` (or routed rework).
