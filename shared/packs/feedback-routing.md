# Feedback Routing

One state machine for every human touchpoint. Classify first, route second.

## Classification

- **tune** — intent unchanged, execution wrong ("move the button", "ask the question differently",
  "this copy is off"). Stay in the current phase and iterate. Not recorded, not counted, unlimited.
  The demo vibe-loop is tune by definition.
- **revise** — an upstream artifact captured the wrong judgment. Identify the **earliest broken
  layer** (feature plan, or an explicitly used requirement → demo → PRD → technical record, then
  slice implementation), fix there,
  cascade staleness downward, replay forward. Record one ledger `rework` entry with `routed_to`.
- **park** — this line of work stops (deprioritized, cancelled, superseded). Record the decision
  and its reason in the ledger, close the branch per `branch-worktree.md`.

The tune/revise boundary: tune changes *how it's expressed*; revise changes *what is true*.
When unsure, ask the human one classification question with a recommendation — never guess a revise.

## Stale Cascade

On `revise` of layer N:
1. Fix layer N's artifact.
2. Every downstream approval (layer > N) is invalid — their `Reviewed-SHA` no longer matches, and
   `check_freshness.py` will prove it. Do not hand-wave partial validity.
3. Replay forward: for each downstream artifact, either confirm it is unaffected (targeted re-review
   citing why) or update it and re-gate. Confirmations are cheap; skipping them is how drift starts.

### Demo replay after mock retirement (honest limitation)

The demo is a perishable artifact: once `build` retires its mocks, the prototype no longer exists
in runnable form, so a post-build `revise` to requirement/PRD **cannot** replay the demo gate as
originally run. The demo layer's replay is defined as, in order:
1. cross-check the revision against PRD's Demo alignment section (which demo behaviors were
   contractual), and
2. verify demo parity **on the real implementation** — exercise the affected interactions there.

Relatedly, the demo gate's `Reviewed-SHA` only ever covered documents (`mock-inventory.md`,
`prototype.md`) — runtime behavior is not hashable. Demo freshness is document freshness; treat
its guarantee accordingly and do not present it as equivalent to the other gates'.

## Acceptance Triage

When the human rejects at acceptance, classify before routing — the three cases have different
destinations and different ledger records:

| Case | Test | Route | Ledger |
|---|---|---|---|
| Implementation defect | code ≠ plan/artifact | fix the affected `build` slice | `rework` → `implementation` |
| Plan/artifact defect | code matches the wrong journey/object | revise the result card or earliest opt-in artifact; invalidate receipts | `rework` → `<layer>` |
| Taste change | captured intent was right, intent moved | start a new result card/increment; use `brainstorm` only when product judgment needs it | `change` (not rework) |

Never let a taste change masquerade as a defect: it poisons rework metrics and creates unwinnable
fix loops. Attribution is the agent's job; arbitration is the human's.

## Cost Asymmetry

Inner loops (tune) are designed to be free. Cross-layer rollbacks (revise) are designed to be
recorded. If retro shows a layer accumulating revise entries, that layer's capture process — not
the downstream fixers — is what needs improving.
