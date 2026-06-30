---
name: review-plan
description: "Use after create-plan to review boundary-only plan files in a fresh dedicated review subagent against approved demo, PRD, technical, spec, testcases, project AGENTS.md, and commands. Assesses artifact references, allowed/forbidden change boundaries, plan indirectness, branch and acceptance compliance, parallelization, serial constraints, buildability from referenced artifacts, and integration readiness."
license: MIT
---

# review-plan

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
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/prompts/reviewer-common.md`
- `../../shared/prompts/plan-reviewer.md`

## Inputs

Approved frontend prototype evidence and mock inventory when UI-facing, approved `prd.md`, approved `technical.md`, approved `spec.md`, black-box `testcases.md`, real black-box testcases, `plan/*.md`, project `AGENTS.md`, and project commands.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. Reviewer must not edit artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to TDD coding unless status is Approved.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, applicable project `AGENTS.md` rules and commands, `reviewer-common.md`, and `plan-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent checks spec coverage, approved prototype reference coverage for UI-facing plans, prototype mock retirement task coverage when required, black-box testcase alignment as acceptance context, File Map completeness, allowed/forbidden boundary clarity, branch and acceptance compliance, parallelization, serial constraints, buildability from referenced artifacts, and integration plan completeness.
4. The review subagent rejects plans that contain API schemas, error matrices, database design, component selection, algorithms, RED/GREEN commands, concrete test cases, or other technical details that belong in `technical.md` or `spec.md`.
5. The review subagent rejects frontend plans that do not reference enough prototype/spec context for implementer subagents to reproduce the approved layout/interactions/states and retire prototype mocks.
6. The review subagent rejects plans that use black-box E2E, acceptance, or regression suites as `tdd-coding` task gates instead of handing them off to `local-e2e-verify` or `release-verify`.
7. For re-review after `Issues Found`, default to targeted fresh review against previous blocking issues, changed plan sections, and affected workstream boundaries unless the revision changes the plan's main semantics.
8. Write review report from the review subagent result without weakening its status or blocking issues.

## Output Contract

Write `docs/features/<feature-slug>/reviews/plan-review.md`.

## Self-Check

Confirm the report was authored by a fresh review subagent and explicitly states whether artifact references, boundary clarity, plan indirectness, demo parity handoff, buildability, parallelization, and integration-plan readiness are approved.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
