# Risk and Readiness

Identify risk early, then add only the check that reduces that risk. Risk does not automatically
load the full artifact chain.

## Categories and matching checks

- **Data/schema/migration** — read-only source snapshot + hash, dry run, invariant query, backup and
  rollback/one-way acknowledgment.
- **Auth/permissions/security** — real session/origin path, allow + deny cases, no test bypass.
- **Money/quotas** — deterministic calculation, idempotency, limit/rollback evidence.
- **External provider** — independent fake, saved-response replay, then one real canary.
- **Runtime capability** — smallest real production-assembly experiment for queues, workers,
  streaming, heavy compute, etc.
- **Long-running/concurrency** — lease/restart/idempotency/concurrency checks and an appropriate
  observation window.
- **Shared state coupling** — scratch copy, invariants, compatibility and rollback.
- **Cross-shell UI** — one core journey per materially different shell only when both are in scope;
  otherwise split.

## Time-boxed spike

Run a spike only when a risk remains unproven and could invalidate the chosen slice. Time-box it
inside the increment budget and test the smallest real capability. Record evidence and a verdict:
ready, ready-with-constraints, or blocked. Reasoning without execution is not a spike.

If the risk cannot be retired without pushing the increment beyond four hours, split or stop. Do
not hide the spike cost outside the budget.

## First slice

Put the highest-risk boundary inside the 45-minute vertical slice when feasible, but keep the slice
to one user-visible result. A slice that combines many unrelated risk categories is too broad and
must be decomposed.
