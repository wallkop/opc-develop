# Targeted TDD and Debugging

Use lower-level tests to localize a core-journey failure, not to replace the journey.

## Main-executor default

The main executor implements standard and lite work by default. Write a failing regression first for
a reproduced bug or high-risk boundary; capture RED, implement, then rerun the same command for
GREEN. For straightforward new behavior, use the cheapest test that protects the slice and do not
manufacture a ceremonial RED after the code already exists.

Never pre-author the entire future test matrix. Add the highest-value regression as each runnable
slice lands. Run targeted tests frequently; run the approved testcase runner at slice boundaries and the full
gate only at integration/final.

## Exceptional implementer dispatch

Dispatch only a truly independent, bounded task that can proceed without another slice's unfinished
work. At most one implementer runs at once. Give it a <=1-page packet: outcome, allowed paths, plan
section, relevant project rules, current command, RED/GREEN expectation, and acceptance command.
Use `fork_turns: none` and ledger `context_mode: none|summary`; full conversation context is
forbidden.

Parallel work requires separate worktrees, but concurrency remains limited to one implementer and
one reviewer. No worktree means serial execution. The controller inspects the actual diff and test
output; an implementer report is not evidence.

## Test honesty

- Exercise the declared layer. An API seed cannot be downgraded to a unit test against the same
  module's mock.
- Use public actions and read-only assertions. Do not add production controls that directly create
  the success state being tested.
- Preserve previous journey behavior. Weakening an assertion to get GREEN is a test defect.
- For snapshot/real data, verify source hash before the run.

## Failure discipline

Before retrying an unclear failure: reproduce, form one hypothesis, inspect correlation-ID logs and
scratch state, identify the root cause, then fix with the cheapest covering regression. If a browser,
seed, DOM, or timing failure occurs during a real-provider attempt, return to offline replay and keep
the provider locked until stable.

Append resolved non-obvious causes to the error ledger. High-value/recurring false-green failures
also link a benchmark case or human-approved waiver.
