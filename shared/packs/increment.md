# Standard Increment

Use this pack for `build`: one 1-4 hour user outcome, one plan, one core journey, runnable slices,
and two code-review moments at most. The core journey leads acceptance; cheap lower-level tests
localize failures.

## Budget gate

Within 20 minutes, classify from the credible elapsed-time estimate:

- <=60 minutes and one small result: route to `lite`, except a release-bound/oncall change uses a
  quick build increment so `ship`/`deploy` receive a receipt and review chain.
- 1-4 hours: continue as a standard increment.
- >4 hours or multiple independently useful outcomes: write a split plan, propose the first
  standard increment, and stop. Never promise the whole engineering program in one run.

Risk adds only its matching protection. A migration adds snapshot/rollback checks; permission work
adds authn/authz checks; an external provider adds replay + one canary. A risk word does not load
Demo, PRD, technical design, contracts, and a full test matrix automatically.

## Result card and core journey

Write `feature-plan.md` per `formats/feature-plan-format.md`, validate it, and initialize
`acceptance.json` per `formats/acceptance-receipt-format.md`. Resolve at most three questions that
would change the route; inspect code/runtime/data for everything discoverable.

Run the core journey once before implementation. It must fail for the missing behavior, not for a
broken harness. For UI, the browser performs the accepted action. API/DB setup may prepare state but
may not manufacture the result. If historical data matters, use a source-hashed read-only snapshot.

## First vertical slice

Within 45 minutes, pass through the real assembly boundary:

`real entry -> real session/auth -> production router -> production service -> scratch state -> result`

Implement only the smallest visible result. Do not combine authentication, compiler, scheduler,
provider, persistence, migration, audit, and UI breadth into one slice. If the entry cannot run or
be observed within 45 minutes, pause feature breadth and route the missing run/reset/observe/drive
capability to `harness`.

After the slice works, run one independent reality review with `rubrics/increment.md`. Give the
reviewer only the plan, diff, receipt, relevant project rules, and commands using an empty/cold
context (`fork_turns: none` or equivalent). The reviewer checks production assembly and the real
object, not just tests.

## Expand one behavior at a time

Implement slices serially by default. During coding, run cheap targeted logic/API tests after
relevant edits. Add the most valuable regression for each completed slice; do not pre-author the
entire future test matrix. Run the browser core journey once at each completed slice, the full gate
only at integration/final delivery, and the provider canary only after offline layers are stable.

The main executor implements by default. Use one implementer subagent only for a truly independent,
bounded task; give it a one-page task packet and `context_mode: none|summary`. `fork_turns: all` is
forbidden. Never run more than one implementer and one reviewer at the same time.

Tests may act through public UI/API/CLI, inspect scratch state read-only, use independent provider
fakes, and import source-hashed snapshots. Production code must not expose test controls that
directly create the Run/Event/Artifact/Receipt later asserted as success.

## Verification ladder and stop-loss

Run from cheap/stable to expensive:

1. logic/build;
2. local production service + scratch state;
3. browser core journey for UI;
4. saved-provider-response replay;
5. one real provider canary;
6. human acceptance.

If a provider attempt exposes a harness, DOM, seed, or timing problem, repair and stabilize offline;
do not immediately call the provider again. `opc_increment.py` mechanically guards this sequence.

Run one final independent integration review. Across reality + final reviews, allow at most two
repair rounds total. If blockers remain, stop patching and reduce scope or redesign. A broad review
object is itself blocking. Record increment gates with `flow: increment-v1`; `opc_ledger.py audit`
enforces the repair budget.

## Completion

Run `opc_increment.py check --require real-service-core-journey`. Report the exact highest level;
never call an increment complete when the check fails. A user correction that changes the target
object or journey invalidates the plan, tests, receipt, and downstream conclusions; rewrite the
result card and re-evaluate scope before continuing.
