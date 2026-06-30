# Subagent Execution Contract

`tdd-coding` is the controller. It reads the approved plan tree and dispatches implementer subagents by independent plan file.

## Controller Boundary

Implementer subagents are mandatory. If the current environment cannot start subagents, `tdd-coding` must stop and report a blocker instead of implementing plan tasks inline.

When the environment provides named implementation agents, use the OPC plan implementer role for assigned plan files. If no named role exists, use the environment's native isolated subagent mechanism with the implementer prompt.

The controller may read plans, decide worktree strategy, prepare context, dispatch subagents, answer `NEEDS_CONTEXT`, route blockers, run integration steps, and record progress. The controller must not directly implement tasks from `plan-XX-*.md`. The only implementation work the controller may perform is the explicit integration work described by `integration-plan.md` after all plan subagents and review gates are ready.

Each implementer subagent receives only the context needed for its assigned plan: that plan file, relevant spec/testcase excerpts, required `AGENTS.md` rules, allowed commands, work directory or worktree, and language/output contracts. Do not provide unrelated conversation history, other plan internals unless required for dependencies, creator reasoning, or desired conclusions.

Full-flow implementers must receive the complete development input set required by `development-input-contract.md`, scoped to the assigned plan: frontend prototype evidence, prototype mock inventory when relevant, PRD, technical, spec, plan, and black-box testcases as acceptance context. The plan file supplies boundaries and references; implementation detail must come from the approved artifacts, not from new plan prose.

## Status Protocol

Each implementer subagent must report one status:

- `DONE`
- `DONE_WITH_CONCERNS`
- `NEEDS_CONTEXT`
- `BLOCKED`

The controller must not ignore concerns or blockers. It must provide context, split tasks, choose a stronger model, or return to plan review when the plan is wrong.

## Review Gates

After each subagent completes:

1. Run one fresh spec compliance implementation review subagent using the actual code and tests, not only the implementer report.
2. Run code quality review only when `review-trigger-policy.md` risk triggers apply.
3. If spec compliance has blocking issues, the review status is `Issues Found`; skip code quality except for obvious severe safety, data-loss, secret-leak, or destructive-operation risks worth reporting.
4. Provide reviewers only necessary inputs: assigned plan, relevant frontend prototype evidence and mock retirement excerpts when relevant, relevant spec/testcase excerpts, applicable project rules, implementer report, diff, changed files, and test evidence.
5. Do not provide implementer private reasoning, controller conclusions, desired approval outcome, or unrelated conversation context.
6. Send issues back to the implementer or a fix subagent.
7. Repeat with targeted fresh review after fixes. Do not full-review every small repair unless the fix changes the main semantics or risk trigger scope.

When any assigned plan touches approved prototype mocks, the spec compliance implementation review must include mock retirement and residual checks. After all plans and integration work are complete, the controller must run a fresh final feature-level mock residual review/audit before claiming `tdd-coding` complete.

If isolated review subagents are unavailable, stop and report a blocker. Do not let the implementer self-approve and do not let the controller perform inline implementation review.

## Worktree Decision

The controller decides whether to create worktrees based on conflict risk, service isolation, test isolation, branch rules, and project `AGENTS.md`. Worktrees are optional tools, not a default plan execution mode. The user must not be asked to choose worktree strategy unless a merge/discard/destructive cleanup decision is required. Follow `branch-stage-contract.md` first, then `worktree-isolation-contract.md` for detection, nested-worktree avoidance, branch parent rules, cleanup, and detached HEAD handoff.
