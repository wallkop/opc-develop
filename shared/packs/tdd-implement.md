# TDD Implementation Pack

For the `build` controller and its implementer subagents.

## Controller Duties

The controller reads the approved impl-contract tree, dispatches implementer subagents, answers
`NEEDS_CONTEXT`, routes blockers, runs integration, and records progress. The controller does not
implement contract tasks itself. If subagent execution is unavailable, record the gap, implement
inline **one contract at a time with the full TDD evidence discipline**, and mark every such task
`self-implemented (no isolation)` in the ledger — the label alerts the human that controller and
implementer were not separated.

## Isolation Rule

Parallel dispatch ⇒ one worktree per implementer (see `branch-worktree.md`). No worktrees ⇒ serial
dispatch. There is no third option; do not weigh "conflict risk" per case.

Wrap every dispatch in a ledger cost span. Close it after controller verification and attach child
session ids/usage when the host exposes them. Missing child usage is an `observe` gap, not a token
estimate invented from prose length.

## Dispatch Context

Each implementer receives: its impl-contract file path, the AC-IDs it owns, the declared level of
each TDD seed (`unit`/`api`/`e2e` — the implementer honors the level, it does not downgrade an
`api` seed to a unit test against its own mock), paths (not full text) to PRD/technical sections
it needs, relevant mock-retirement entries, project rules (AGENTS.md), allowed commands, and its
work directory. Point to artifacts by path + section; do not paste full documents into the prompt.

## Implementer Protocol

Per task: write the failing test first, capture `RED:` evidence, implement, capture `GREEN:`
evidence (fields per `evidence.md`), refactor. Report: files changed, tests added/changed, RED/GREEN
fields, commands + exit codes, mock-retirement actions taken, concerns, and exactly one status token
(`DONE` / `DONE_WITH_CONCERNS` / `NEEDS_CONTEXT` / `BLOCKED`).

## Per-Task Gate

After each implementer completes, one fresh reviewer subagent runs the merged review (contract
compliance + code quality in a single pass) using `rubrics/implementation.md`, the actual diff, and
test evidence — never only the implementer's report. Risk-triggered concerns (security, data loss,
migration, concurrency) get explicit attention within the same review, not a second reviewer.
Blocking issues → back to the implementer → targeted re-review. Stop-loss per `gate-protocol.md`.

## Failure Discipline

A failing test with an unclear cause gets debugging discipline before retry: reproduce first,
form a hypothesis, read the runtime evidence (logs by correlation ID, DB state), identify root
cause, then fix with a covering test. When resolved, append the root-cause record to the
error-ledger (see `formats/ledger-format.md`) — resolution time is capture time.

## Integration

When all contracts are done, the controller performs the integration steps from the impl-contract
index — **including every `api`-level boundary case the index names for cross-contract seams**.
Seam cases are the controller's to run, not any single implementer's: a seam that both sides only
ever exercised through mocks of each other is unverified until its boundary case passes against
the real interfaces. Then run implementation-facing checks and the final mock-residual audit when
any prototype mock existed (fresh reviewer + grep/static evidence per `mock-retirement.md`).
Black-box E2E, acceptance, and regression belong to `build`'s local-verification phase
(`verification.md`), not here.
