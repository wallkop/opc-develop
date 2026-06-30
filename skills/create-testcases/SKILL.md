---
name: create-testcases
description: "Use after review-spec is Approved to create or update black-box product testcase files only: E2E, acceptance, and regression cases under docs/testcases product-module folders plus the feature testcase index. Do not create unit tests, API tests, white-box fixtures, TDD commands, or implementation test plans."
license: MIT
---

# create-testcases

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/testcase-format.md`
- `../../shared/references/review-status-contract.md`

## Inputs

Approved demo when UI-facing, approved `prd.md`, approved `technical.md`, approved `spec.md`, existing `docs/testcases/` modules.

## Hard Gates

`reviews/spec-review.md` must be Approved. Do not write plan, code, unit tests, API tests, mocks, white-box fixtures, implementation test commands, feature branch, or worktree. In Full flow, operate on the current feature branch created by `product-brainstorm` before `requirement.md` was written; do not create a feature branch or any other branch. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

## Process

1. Inspect current branch according to `branch-stage-contract.md`; for Full flow, require the feature branch created by `product-brainstorm` or a project-approved equivalent.
2. Identify product module for each acceptance criterion.
3. For UI-facing work, include demo-critical layout, state, and interaction paths as black-box E2E or acceptance cases.
4. Create or update black-box testcase files under `docs/testcases/<product-module>/`.
5. Include E2E, acceptance, and regression coverage as needed from the product/system boundary.
6. Write feature-local `testcases.md` as an index to real black-box testcase paths.
7. Include black-box automation entrypoints or manual verification paths plus failure diagnostics, including screenshot or interaction evidence expectations when demo parity matters.
8. Leave unit/API test design to `tdd-coding`; mention only acceptance behaviors that those tests may need to cover.

## Output Contract

Write only black-box testcase files under `docs/testcases/<product-module>/` and write `docs/features/<feature-slug>/testcases.md` as an index only.

## Self-Check

Confirm every PRD acceptance criterion maps to at least one real black-box testcase path, demo-critical UI behavior is covered when relevant, and no UT/API/TDD implementation test design was written. If this run revised already reviewed testcases, report that `review-testcases` must be rerun before plan creation can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
