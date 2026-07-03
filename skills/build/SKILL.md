---
name: build
description: "Use after the contract gate is Approved to implement the contract tree: dispatches one implementer subagent per contract (worktrees when parallel, serial otherwise), enforces TDD with RED/GREEN evidence, runs the merged per-contract review gate, retires prototype mocks with a final residual audit, applies debugging discipline to failures, and integrates. Never runs black-box E2E."
license: MIT
---

# build

The controller phase. Implementers implement; the controller dispatches, verifies evidence,
routes, and integrates.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/tdd-implement.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- For gates: `packs/gate-protocol.md` + `rubrics/implementation.md`
- Implementer prompt: `${CLAUDE_PLUGIN_ROOT}/shared/prompts/implementer.md`

## Process

1. Precheck: contract-gate freshness (`check_freshness.py`), readiness blockers from
   `risk-spike.md` (blocked verdicts stop only the affected contracts).
2. Choose dispatch mode per `tdd-implement.md`: parallel ⇒ one worktree per implementer;
   otherwise serial in place. Ledger a `dispatch` entry per contract with mode and isolation.
3. Dispatch implementers (prefer the `opc-implementer` agent; else the environment's
   isolated subagent with `prompts/implementer.md`). Context per `tdd-implement.md`: paths and
   section pointers, not pasted documents.
4. Per completed contract: verify the report against reality (diff, test output, RED/GREEN
   fields), then run the merged review gate — fresh reviewer, `rubrics/implementation.md`, actual
   diff + tests. Blocking issues → implementer → targeted re-review. Stop-loss: 2 rounds, then
   escalate per `gate-protocol.md`.
5. Failures with unclear cause get debugging discipline (`tdd-implement.md`): reproduce →
   hypothesis → runtime evidence (correlation-ID logs, DB state) → root cause → fix with a
   covering test. On resolution, append the root-cause record to `docs/opc/error-ledger.jsonl`
   via `opc_ledger.py` — resolution time is capture time; skipping this starves `retro`.
6. Handle status tokens: `NEEDS_CONTEXT` → supply or route `revise` if the contract is wrong;
   `BLOCKED` → ledger and escalate; `DONE_WITH_CONCERNS` → resolve the concern before counting
   the contract done.
7. Integration: after all contracts pass their gates, run the index's integration steps, then the
   final mock-residual audit when any prototype mock existed (fresh reviewer + grep/static
   evidence per `mock-retirement.md`). Merge worktrees back per `branch-worktree.md`.
8. Ledger throughout: gate results, rework routings, dispatch records, evidence labels for
   implementation-facing checks (typically `mock passed` / `seeded passed` — never higher from
   this phase).

## Fail-open

No subagent support: degrade per `tdd-implement.md` (inline, one contract at a time, full TDD
evidence, `self-implemented (no isolation)` labels) and surface the degradation at the next
touchpoint. Missing commands/runbooks: discover, record `gap`, continue.

## Output

Implemented feature with unit/API tests, per-contract review records, mock residual audit,
error-ledger records for resolved failures, ledger trail. Next: `verify`.
