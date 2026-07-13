---
name: build
description: "Use after the mandatory Approved demo, PRD, and testcase phases for a product increment that creates or changes user-visible behavior. Routes by product semantics and risk, never by predicted duration; enforces approved-case-driven E2E, a one-page feature-plan.md, serial runnable slices, trusted runner evidence, and convergent reviews."
license: MIT
---

# build

Deliver one useful increment through a real working path, then add coverage and evidence that
protect it. Never estimate or enforce an elapsed-time or implementation-cost budget.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/increment.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/feature-plan-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/acceptance-receipt-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/testcase-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- When `demo/mock-inventory.md` exists: `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- On matching risk: `packs/risk-readiness.md`
- On branch/worktree questions: `packs/branch-worktree.md`
- For reviews: `packs/gate-protocol.md` + `rubrics/increment.md`

## Process

1. Read project rules and inspect the real entry, runtime assembly, target data, and harness before
   asking questions. Run `opc_testcase.py check --require-approved`; missing/stale demo, PRD,
   testcase review, compiled manifest, or product approval blocks build and routes to that phase.
2. Route by semantics and risk only. Localized non-semantic changes and changes that reuse an
   already approved oracle unchanged may use `lite`; new or changed user journeys, state, data,
   permissions, cross-module contracts, or release evidence use `build`. Decompose independent
   journeys when that improves reviewability, but never block work based on a duration estimate.
3. Use the current authorized feature branch. Write `feature-plan.md`, choose `Core-Case` from the
   approved manifest, map PRD constraints and every demo mock to replacement slices, and make both
   core/regression commands invoke the project testcase runner. Validate and initialize
   `acceptance.json`; initialization independently rechecks the mandatory chain.
4. Execute the approved Core-Case before implementation and confirm a meaningful product failure.
   For UI, the testcase runner performs the Playwright action and atomically observes success and
   failure. Repair a broken runner/harness before feature breadth; never improvise a new oracle.
5. Implement Slice-1 through the production assembly. Use targeted lower-level tests while coding,
   then run the real core journey once. If the path cannot run or be observed, route the harness
   gap before depending on that missing evidence.
6. Run the independent reality review. Then implement remaining independently runnable slices serially,
   preserving the previous core journey and adding one valuable regression per slice. The main
   executor implements by default; subagents are exceptional and receive cold one-page context.
7. Verify in cost order through `opc_increment.py`: build/logic, local service + scratch state,
   approved testcase runner for every E2E, provider replay, one external canary when applicable.
   Browser/core/provider commands must attach fresh `opc-case-evidence-v1`; authenticity labels are
   derived from its axes, not caller flags. Never use the canary as a debug loop.
8. Run one final independent integration review. Repair and re-review until it passes or a genuine
   blocker requires user input or redesign; there is no fixed repair-round quota. When an inventory
   exists, prove every mock is retired from production runtime. Audit with
   `opc_ledger.py audit --require-increment-complete` so missing review records cannot pass.
9. Run `opc_increment.py check --require real-service-core-journey`. Report its exact completion
   level and remaining caps. Do not claim completion when the receipt is stale or the core journey
   is below real-service level.

## Re-entry

Test/human rejection of the same intent re-enters the affected slice: invalidate stale receipt
results, add a covering regression, fix, rerun cheap checks, then the core journey and targeted
final review. If the user says the target object or intended journey is wrong, invalidate all
downstream conclusions and rewrite the result card before continuing.

## Output

One runnable increment, `feature-plan.md`, generated `acceptance.json`, focused regressions, review
records, and an honest completion level. Next: `ship` for test-environment acceptance.
