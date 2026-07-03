# Risk & Readiness

High-risk work is identified early and de-risked with evidence before broad implementation.

## Risk Categories

Classify every feature at `brainstorm` (record in requirement.md; `none identified` is a valid answer):

- **External Provider** — depends on a third-party API/SaaS whose behavior is unverified here.
- **Runtime Capability** — needs a capability the stack has not proven (streaming, websockets,
  background jobs, heavy computation).
- **Long-running / Streaming** — correctness depends on sustained operation, not single requests.
- **State Coupling** — touches shared state machines, migrations, or cross-feature invariants.
- **Cross-shell UI** — spans multiple app shells/platforms with divergent behavior.

## Risk Spike

Any category present ⇒ a time-boxed spike before `build`'s contracting phase: the smallest experiment that proves the
risky capability actually works in this project (real provider call, prototype worker, migration
dry-run). Output: `docs/features/<slug>/risk-spike.md` — what was tried, evidence with authenticity
labels, verdict (ready / ready-with-constraints / blocked). A spike that only reasons without
running anything is not a spike.

## Thin Slice

High-risk features implement a thin slice first: one end-to-end path through the risky capability,
gated and verified, before parallel breadth work. The impl-contract tree must show the slice as the
first contract with the rest depending on it.

## Readiness Blockers

Unresolved `blocked` verdicts stop `build` dispatch for the affected contracts only; unaffected
contracts may proceed. Record the blocker in the ledger and surface it at the next touchpoint.
