---
name: create-prd
description: "Use after review-demo is Approved to create or revise the feature PRD from requirement.md, demo, and demo-review.md. Defines product behavior, scope, flows, rules, states, acceptance criteria, and non-goals."
license: MIT
---

# create-prd

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prd-format.md`
- `../../shared/references/review-status-contract.md`

## Inputs

`requirement.md`, approved frontend prototype evidence in `demo/prototype.md`, preview assets when relevant, and `reviews/demo-review.md`.

## Hard Gates

`reviews/demo-review.md` must be Approved. Do not write technical design, spec, plan, testcase, code, feature branch, or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent before writing PRD artifacts. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

## Process

1. Read requirement, frontend prototype evidence, mock inventory, and demo review.
2. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
3. Preserve product intent and avoid unapproved scope.
4. Extract the approved frontend prototype's layout hierarchy, interaction model, visible states, important copy/control affordances, and user-facing mock scenarios into a `Demo Alignment Contract` section in `prd.md`.
5. Convert product ambiguities into blocking open questions.
6. Write `prd.md` using the PRD format.
7. Map acceptance criteria to user-visible or system-verifiable behavior, including demo-critical UI states and interactions when the feature is UI-facing.

## Output Contract

Write `docs/features/<feature-slug>/prd.md`.

## Self-Check

Confirm every requirement and approved frontend prototype decision is represented, the demo alignment contract is explicit, user-facing mock scenarios are captured without treating mocks as production design, intentional demo deviations are explained, and no TODO/TBD placeholders remain. If this run revised an already reviewed PRD, report that `review-prd` must be rerun before technical design can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
