---
name: create-plan
description: "Use after review-testcases is Approved to create boundary-only feature plan workstream files and integration-plan.md. Builds a parallelizable plan tree with module/workstream split, development order, allowed/forbidden change boundaries, artifact references, branch rules, and local-e2e handoff; does not write API schemas, database design, RED/GREEN commands, or technical implementation details."
license: MIT
---

# create-plan

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
- `../../shared/references/plan-tree-format.md`
- `../../shared/references/tdd-contract.md`
- `../../shared/references/review-status-contract.md`

## Inputs

Approved frontend prototype evidence and mock inventory when UI-facing, approved `prd.md`, approved `technical.md`, approved `spec.md`, approved black-box testcase index, project code context, applicable project `AGENTS.md`, `docs/technical/runbooks/local-dev.md`, and `docs/technical/standards/testing.md`.

## Hard Gates

`reviews/demo-review.md`, `reviews/spec-review.md`, and `reviews/testcase-review.md` must be Approved. Required project `AGENTS.md` rules for development flow, branching, and acceptance must be read before writing plans. Do not create a feature branch or worktree. In Full flow, operate on the current feature branch created by `product-brainstorm` before `requirement.md` was written. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

## Process

1. Read root and scoped `AGENTS.md` files and extract development flow, branch strategy, branch creation, acceptance flow, and gates.
2. Inspect current branch according to `branch-stage-contract.md`; the plan records branch expectations but must not create branches.
3. Read approved frontend prototype evidence, mock inventory, PRD, spec, technical design, black-box testcases, local-dev runbook, and testing standard.
4. Build a File Map for each plan file with exact expected files or directories and their purpose.
5. For UI-facing plans, include prototype/PRD/spec references that implementer subagents must read; do not restate UI technical detail in the plan.
6. Split independent workstreams into separate `plan-XX-<workstream>.md` files.
7. Keep serially dependent tasks inside the same plan file with explicit task dependencies.
8. For each task, define referenced upstream artifacts, allowed change boundary, forbidden change boundary, development order notes, dependencies, and ready standard. When the spec has a `Prototype Mock Retirement Plan`, include explicit task boundaries for replacing and removing prototype mocks.
9. Do not write API schemas, error matrices, database design, component selection, algorithms, RED/GREEN commands, or concrete test cases in the plan.
10. Remove placeholders such as TODO, similar to, add proper error handling, handle edge cases, write tests later, or implement appropriately.
11. Use black-box testcases as acceptance context only, and hand off black-box E2E, acceptance, or regression execution to `local-e2e-verify` or `release-verify`.
12. Write `integration-plan.md` as the final merge and implementation-facing integration node, with explicit handoff to `local-e2e-verify` for black-box regression and runtime demo parity evidence.

## Output Contract

Write `docs/features/<feature-slug>/plan/plan-XX-<workstream>.md` files and `docs/features/<feature-slug>/plan/integration-plan.md`.

## Self-Check

Confirm every plan declares AGENTS.md rule source, current feature branch expectation from `branch-stage-contract.md`, acceptance entrypoint, acceptance pass criteria, File Map, artifact references, allowed/forbidden change boundaries, parallel-safe conditions, and ready standards. Confirm the plan is indirect and contains no technical detail that belongs in technical/spec. Confirm an implementer subagent can execute by reading referenced approved artifacts without extra design decisions and without running black-box regression. If this run revised an already reviewed plan, report that `review-plan` must be rerun before TDD coding can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
