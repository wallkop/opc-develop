---
name: tdd-coding
description: "Use after review-plan is fresh Approved to implement an approved Full plan tree with TDD through mandatory implementer subagents. Requires approved demo, PRD, technical, spec, plan, and black-box testcases as input; writes/runs implementation-facing unit and API tests; uses targeted review and risk-triggered code quality review; never runs black-box E2E, acceptance, or regression suites."
license: MIT
---

# tdd-coding

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/development-input-contract.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/tdd-contract.md`
- `../../shared/references/subagent-execution-contract.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/evidence-before-claim.md`
- `../../shared/references/worktree-isolation-contract.md`
- `../../shared/prompts/implementer-subagent.md`
- `../../shared/prompts/implementation-reviewer.md`

## Inputs

Approved frontend prototype evidence, demo review, and prototype mock inventory when UI-facing, approved `prd.md`, approved `technical.md`, approved `spec.md`, approved `plan/*.md`, approved black-box `testcases.md` and real testcase files as acceptance context, project code, project commands, and applicable project `AGENTS.md`.

## Hard Gates

All upstream reviews through `reviews/plan-review.md` must be fresh Approved. Full-flow development must have the complete input set required by `development-input-contract.md`; missing inputs block. If the approved frontend prototype contains mocks, `spec.md` must contain a `Prototype Mock Retirement Plan` and `plan/*.md` must include explicit replacement/removal boundaries before any implementer subagent starts.

Implementer subagents are mandatory for plan task execution. If no subagent execution is available, stop and report a blocker; do not downgrade to controller-inline implementation. The controller must not directly implement `plan-XX-*.md` tasks.

Follow project `AGENTS.md` branch strategy and acceptance rules. Do not create a feature branch; Full branch creation must already have happened in `product-brainstorm` before `requirement.md` was written. Worktrees are optional tools only for conflict, test, service, parallelism, or project-rule isolation. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not use black-box E2E, acceptance, or regression execution as this skill's completion gate. Do not claim `DONE` while any prototype mock still affects production runtime.

## Process

1. Read the full approved input set: frontend prototype evidence, demo review, prototype mock inventory, PRD, technical, spec, plan tree, black-box testcase index/files, project rules, and commands.
2. Inspect current branch according to `branch-stage-contract.md`; require the feature branch created by `product-brainstorm` or a project-approved equivalent before dispatch.
3. Verify artifact boundaries before dispatch: technical owns SaaS/API public contracts, spec owns internal implementation/TDD seed and prototype mock retirement details, plan only owns boundaries/references. If this is false, stop and route to the earliest broken artifact.
4. If prototype mocks exist, enumerate the inventory and confirm every entry is covered by the `Prototype Mock Retirement Plan`, a plan boundary, and a focused unit/API/implementation-facing test seed. Missing coverage blocks dispatch.
5. Decide whether each parallel plan needs a worktree based on conflict risk, tests, and AGENTS.md, following `worktree-isolation-contract.md`; do not create worktrees by default.
6. Dispatch implementer subagents by independent plan file. Give each subagent only its assigned plan boundaries plus relevant frontend prototype evidence, mock inventory, mock retirement plan excerpts, PRD, technical, spec, testcase, project-rule, command, and work directory/worktree context required by `development-input-contract.md`.
7. Require TDD for every task using unit tests, API tests, or focused implementation-facing tests derived from spec TDD seed, prototype mock retirement requirements, and black-box testcase context. Require implementer subagents to report files changed, UT/API tests added or changed, commands run, evidence, demo parity notes, mock retirement notes, residual audit evidence, concerns, and one exact status token.
8. Handle `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, and `BLOCKED` statuses. Do not ignore concerns; provide missing context, split work, route back to plan/spec/technical review, or stop on blockers. Treat unresolved production mock residuals as blocking, not as concerns.
9. For UI-facing plans, require implementer subagents to state how the implementation preserves the approved prototype's layout, interaction, and state expectations, or to return `NEEDS_CONTEXT` when the demo/spec references do not define enough parity detail.
10. For each completed plan, inspect actual diff, changed files, test output, report paths, and mock residual evidence before making any status claim.
11. For each completed plan, run a fresh spec compliance implementation review subagent using actual code and tests, not only the implementer report. Provide approved prototype context and mock inventory for UI-facing or prototype-derived work.
12. Run code quality review only when `review-trigger-policy.md` risk triggers apply. Record the trigger or why code quality review was not run.
13. Send blocking review issues back to the original implementer subagent or a dedicated fix subagent. After fixes, repeat targeted fresh review focused on previous blocking issues, changed diff, affected contracts, and mock residual evidence. Do not full-review every small repair unless semantics or risk scope changed.
14. Stop after the same blocking issue fails to converge for 2 repair rounds; write the unresolved issue to `progress.md` and route to technical/spec/plan or human decision.
15. When implementation-facing tests fail for a pure implementation defect, use `debug-failure` discipline before retrying fixes.
16. When all plans are ready, execute `integration-plan.md` as the controller, limited to integration and white/gray-box checks. Do not run black-box regression; hand off to `local-e2e-verify` for runtime demo parity and black-box evidence.
17. After integration, run a final mock residual review/audit for the whole feature when any prototype mock existed. Use a fresh implementation review subagent focused on the prototype mock inventory plus fresh grep/static checks, changed-file inspection, focused tests, or project-specific commands to prove prototype mocks no longer affect production runtime. Do not claim completion when evidence is missing or ambiguous.
18. Update `progress.md` with subagent assignments, commands, exit codes, report paths, demo parity notes for UI-facing work, mock retirement actions, final mock residual review/audit evidence, review scope type, risk triggers, review outcomes, blockers, and residual risk.

## Output Contract

Produce code, unit/API test changes, optional focused implementation-facing test changes, plus updated `docs/features/<feature-slug>/progress.md` containing plan/subagent/task status, spec compliance review results, mock retirement and residual audit results when applicable, risk-triggered or skipped code quality review rationale, targeted re-review outcomes, and integration evidence. Do not claim black-box E2E, acceptance, or regression passed.

## Self-Check

Do not claim completion without the full input set, implementer subagent reports, controller-checked diff/test/report evidence, fresh spec compliance review evidence, mock residual review/audit evidence when prototype mocks existed, risk-triggered code quality review evidence when required, UT/API task test evidence, integration check evidence, and demo parity notes for UI-facing work. Confirm the controller did not directly implement plan tasks, did not leave prototype mocks in production runtime, and did not treat black-box tests as a `tdd-coding` gate.

## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not fresh Approved, subagent execution is unavailable, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
