---
name: demo
description: "Use only when interaction taste is unresolved and the human explicitly wants an experienceable prototype before implementation. Builds a high-fidelity prototype in the real frontend (or a runnable non-UI skeleton), runs the vibe-loop, and inventories mocks. It is optional and not required for an ordinary standard increment with a clear core journey."
license: MIT
---

# demo

Data fake, feeling real. Taste is verified by experience, not by reading — this phase exists so
that `revise` happens at its cheapest possible moment.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/feedback-routing.md`
- For the gate: `${CLAUDE_PLUGIN_ROOT}/shared/packs/gate-protocol.md` +
  `${CLAUDE_PLUGIN_ROOT}/shared/rubrics/demo.md`

## Process

1. Verify a result card or `requirement.md` exists on the feature branch. Decide the variant:
   - **UI surface exists** → prototype in the real frontend codebase, reachable through the real
     app shell. No detached playgrounds, no query-param-only roots.
   - **No UI surface** (API/CLI/job/migration) → runnable skeleton: one real request/response or
     command chain with production-shaped stub data. Skip nothing else; the inventory and gate
     apply the same way.
2. Build fast and shallow-but-honest: frontend-only mocks for missing backend data, every mock
   entered in `docs/features/<slug>/demo/mock-inventory.md` as you create it (id, file, type,
   scenario, replacement). Restart local services per the project runbook; get a preview URL or
   run command.
3. **Vibe-loop (the main work):** hand the human the preview. Their feedback is `tune` by
   default — iterate freely, no records, no re-gates. Watch for the tune/revise boundary: feedback
   that changes *what is true* (wrong audience, wrong core flow) is a `revise` to the source result
   card or `requirement.md` — say so, route it, cascade staleness.
4. Record demo run notes in `docs/features/<slug>/demo/prototype.md`: entry path, preview
   command/URL, which source-card/requirement key paths it demonstrates, known placeholder areas.
5. When the human says the feel is right, gate it: fresh reviewer, `rubrics/demo.md`, reviewer
   must exercise the running prototype. Ledger the gate result.

## Fail-open

Missing local runbook: get it running anyway, record a `gap` (verb: run) with what you had to
discover by hand. If ≥80% fidelity is genuinely unreachable (missing design system, dead frontend
build), record the gap, show the closest reachable fidelity, and let the human decide park vs
proceed-with-cap — do not silently lower the bar.

## Output

Running prototype in the real codebase, `mock-inventory.md`, `prototype.md`, demo gate Approved,
ledger entries. Next: `build` by default; use `prd` only when the prototype reveals durable product
decisions worth a product contract.
