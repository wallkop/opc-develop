---
name: build
description: "Use for a standard 1-4 hour product increment, or a release-bound/oncall quick increment that needs ship/deploy evidence, starting from a raw request or optional approved artifacts. Enforces a 4-hour budget gate, one-page feature-plan.md, one real core journey, a 45-minute first slice, serial runnable slices, cost-ordered verification, at most two review repair rounds, and a revision-bound receipt. UI completion requires a browser action through production assembly. Work above 4 hours is split; ordinary small work routes to lite."
license: MIT
---

# build

Deliver one useful increment within the stated budget. Optimize time to a real working path, then
add coverage and evidence that protect it.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/increment.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/feature-plan-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/acceptance-receipt-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- When `demo/mock-inventory.md` exists: `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- On matching risk: `packs/risk-readiness.md`
- On branch/worktree questions: `packs/branch-worktree.md`
- For reviews: `packs/gate-protocol.md` + `rubrics/increment.md`

## Process

1. Read project rules and inspect the real entry, runtime assembly, target data, and harness before
   asking questions. Establish the user's time budget; default a standard increment to 240 minutes.
2. Apply the budget gate from `increment.md`. Route ordinary <=60-minute work to `lite`. A hotfix
   or other release-bound change that must pass `ship`/`deploy` stays in `build` as `Class: quick`
   so it receives a receipt and reviews. If credible scope is >240 minutes or contains multiple
   independently useful journeys, write the split result card, recommend the first increment, and
   stop before broad implementation.
3. Use the current authorized feature branch, or create a numbered `feature/<slug>` branch. Write
   only `docs/features/<slug>/feature-plan.md`; existing requirement/PRD/technical records are
   constraints when present, not mandatory predecessors. Map every existing demo mock to its
   replacement slice and regression. Validate the plan and initialize the generated
   `acceptance.json` receipt.
4. Run the core journey before implementation and confirm a meaningful failure. For UI, the browser
   performs the key action. Repair a broken harness before writing breadth.
5. Implement Slice-1 through the production assembly within 45 minutes. Use targeted lower-level
   tests while coding, then run the real core journey once. If the path still cannot run/observe,
   pause and route the harness gap.
6. Run the independent reality review. Then implement remaining 30-90 minute slices serially,
   preserving the previous core journey and adding one valuable regression per slice. The main
   executor implements by default; subagents are exceptional and receive cold one-page context.
7. Verify in cost order through `opc_increment.py`: build/logic, local service + scratch state,
   browser for UI, provider replay, one external canary when applicable. Never use the canary as a
   debug loop.
8. Run one final independent integration review. Reality + final share a maximum of two repair
   rounds; if blockers remain, stop and reduce scope/redesign. When an inventory exists, prove
   every mock is retired from production runtime. Audit with
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

One runnable increment, `feature-plan.md`, generated `acceptance.json`, focused regressions, at most
two review records, and an honest completion level. Next: `ship` for test-environment acceptance.
