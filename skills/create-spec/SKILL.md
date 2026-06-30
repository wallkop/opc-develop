---
name: create-spec
description: "Use after review-technical is Approved to create the feature spec only. Converts approved PRD and technical.md into executable micro implementation contracts for AI: internal modules, local components such as sqlite/local storage/cache, state machines, internal errors, UI/demo parity, Runtime evidence points, verification mapping, and TDD seed; does not redefine SaaS choices or public API I/O."
license: MIT
---

# create-spec

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/spec-format.md`
- `../../shared/references/review-status-contract.md`

## Inputs

`requirement.md`, approved frontend prototype evidence and `reviews/demo-review.md`, prototype mock inventory, approved `prd.md`, approved `technical.md`, project code and docs.

## Hard Gates

`reviews/demo-review.md`, `reviews/prd-review.md`, and `reviews/technical-review.md` must be Approved. The feature branch must already have been created or entered by `product-brainstorm` before `requirement.md` was written. Do not create or switch branches, write plan or code, or create a worktree by default. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

## Process

1. Read upstream artifacts, approved frontend prototype evidence, mock inventory, and applicable `AGENTS.md`.
2. Apply `branch-stage-contract.md`: inspect current branch and dirty state, derive the numbered feature slug from `docs/features/<numbered-slug>/`, and verify the current branch is the corresponding `feature/<numbered-slug>` or a project-approved equivalent. Do not create or switch branches here.
3. Verify `technical.md` already owns SaaS decisions and public API input/output contracts. If not, stop and route back to `create-technical`.
4. Convert product and technical decisions into executable internal implementation contracts without duplicating technical design rationale.
5. For UI-facing work, define the executable UI/demo parity contract: layout regions, component responsibilities, interactions, states, responsive constraints, accepted demo deviations, and production reuse boundaries for prototype frontend code.
6. If the approved prototype contains frontend mocks, write a mandatory `Prototype Mock Retirement Plan` section following `prototype-mock-retirement-contract.md`. For every mock, specify the real backend/API/storage replacement, frontend integration change, file/flag removal or test-only restriction, and verification evidence required to prove no production mock residual remains.
7. Make internal module placement, local components such as sqlite/local storage/cache, internal interfaces, data, states, errors, permissions, rollout, rollback, Runtime evidence, and verification mapping explicit.
8. Add a TDD seed list for unit/API/focused implementation-facing tests that `tdd-coding` can execute, including tests that prove real replacement behavior for retired prototype mocks. Do not rely on `plan.md` to define RED/GREEN details.
9. Record missing decisions as blockers.

## Output Contract

Write `docs/features/<feature-slug>/spec.md`.

## Self-Check

Confirm no TODO/TBD placeholders, no hidden implementation decisions, no high-overlap rewrite of `technical.md`, no redefinition of public API I/O or SaaS decisions, and enough executable internal detail for `create-plan` and `tdd-coding`, including UI/demo parity detail when relevant. When prototype mocks exist, confirm `Prototype Mock Retirement Plan` enumerates every mock and gives executable replacement/removal/verification steps with no allowed production mock residual. Confirm the current branch is the matching `feature/<numbered-slug>` or that project rules explicitly require another feature branch equivalent. If this run revised an already reviewed spec, report that `review-spec` must be rerun before testcase creation can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
