# Standard Increment

Use this pack for `build` after demo, PRD, and testcase are approved: one coherent user outcome,
one plan, one approved core case, and runnable slices. The case oracle leads acceptance; cheap
lower-level tests localize failures.

## Semantic route

Classify from the actual semantic surface and risk. Do not ask for, infer, record, or enforce an
elapsed-time or implementation-cost budget:

- localized non-semantic changes use `lite`;
- behavior that reuses an approved oracle unchanged may use `lite` with proportional evidence;
- new or changed journeys, state transitions, persistence, permissions, provider behavior,
  cross-module contracts, or release evidence use `build`;
- independent outcomes may be decomposed for clarity, but uncertainty about duration never blocks
  implementation.

Risk adds only its matching protection. A migration adds snapshot/rollback checks; permission work
adds authn/authz checks; an external provider adds replay + one canary. Architecture and contracting
remain conditional; demo/PRD/testcase are already the mandatory product-definition chain.

## Result card and core journey

Run `opc_testcase.py check --require-approved`. Then write `feature-plan.md`, select Core-Case,
validate it, and initialize `acceptance.json`. Resolve at most three questions that would change the
route; inspect code/runtime/data for everything discoverable.

Run the approved Core-Case once before implementation. It must fail for the missing behavior, not
for a broken harness. For UI, Playwright performs the accepted action and atomic observers race
success against failure. API/DB setup may prepare state but may not manufacture the result. If
historical data matters, use a source-hashed canonical isolated clone.

## First vertical slice

Pass through the real assembly boundary:

`real entry -> real session/auth -> production router -> production service -> scratch state -> result`

Implement the smallest independently visible result. Do not combine authentication, compiler,
scheduler, provider, persistence, migration, audit, and UI breadth without a product reason. If the
entry cannot run or be observed, route the missing run/reset/observe/drive capability to `harness`.

After the slice works, run one independent reality review with `rubrics/increment.md`. Give the
reviewer only the plan, diff, receipt, relevant project rules, and commands using an empty/cold
context (`fork_turns: none` or equivalent). The reviewer checks production assembly and the real
object, not just tests.

## Expand one behavior at a time

Implement slices serially by default. During coding, run cheap targeted logic/API tests after
relevant edits. Implement the approved cases for each completed slice; discoveries that change an
oracle route back to testcase approval. Run the browser Core-Case once at each completed slice, the full gate
only at integration/final delivery, and the provider canary only after offline layers are stable.

The main executor implements by default. Use one implementer subagent only for a truly independent,
bounded task; give it a one-page task packet and `context_mode: none|summary`. `fork_turns: all` is
forbidden. Never run more than one implementer and one reviewer at the same time.

Tests may act through public UI/API/CLI, inspect scratch state read-only, use independent provider
fakes, and import source-hashed snapshots. Production code must not expose test controls that
directly create the Run/Event/Artifact/Receipt later asserted as success.

## Verification ladder

Run from cheap/stable to expensive:

1. logic/build;
2. local production service + scratch state;
3. approved testcase runner for UI/API E2E;
4. saved-provider-response replay;
5. one real provider canary;
6. human acceptance.

If a provider attempt exposes a harness, DOM, seed, or timing problem, repair and stabilize offline;
do not immediately call the provider again. `opc_increment.py` mechanically guards this sequence.

Run one final independent integration review. Repair and re-review until it passes or reaches a
genuine blocker that requires user input, external state, or redesign. There is no fixed review or
repair quota. A broad review object should be decomposed when that makes findings actionable.
Record increment gates with `flow: increment-v1`; `opc_ledger.py audit` enforces the review chain.

## Completion

Run `opc_increment.py check --require real-service-core-journey`. Report the exact highest level;
never call an increment complete when the check fails. A user correction that changes the target
object or journey invalidates the plan, tests, receipt, and downstream conclusions; rewrite the
result card before continuing.
