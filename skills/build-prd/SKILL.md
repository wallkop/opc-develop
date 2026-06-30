---
name: build-prd
description: "Use after build-demo or review-demo is Approved when the user wants PRD creation and review handled as one loop. Runs create-prd, review-prd, and reruns create-prd when prd-review.md has Issues Found until the PRD review is Approved or blocked."
license: MIT
---

# build-prd

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/prd-format.md`

## Inputs

`requirement.md`, approved frontend prototype evidence in `demo/prototype.md`, demo assets when relevant, and `reviews/demo-review.md` with Approved status.

## Hard Gates

`reviews/demo-review.md` must be fresh Approved. Do not write technical design, spec, plan, testcase, code, feature branch, or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not bypass `review-prd`. `review-prd` must run in its own fresh review subagent; this build skill must not review the PRD inline. Do not proceed to technical design unless `reviews/prd-review.md` is fresh Approved for the current `prd.md` revision.

## Process

Run this sequence:

1. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
2. Run `create-prd`.
3. Run `review-prd` in a fresh dedicated review subagent with only necessary review inputs.
4. If `reviews/prd-review.md` is `Issues Found`, rerun `create-prd` using the review findings as required revision input.
5. Treat the previous PRD review as stale after every `create-prd` revision.
6. Rerun `review-prd` in a fresh dedicated review subagent after each PRD revision; default to targeted review of blocking issues and changed PRD sections unless the revision changes the PRD's main semantics.
7. Stop only when `reviews/prd-review.md` is fresh Approved for the latest PRD or a blocker is reached.

## Output Contract

Produce `docs/features/<feature-slug>/prd.md` and `docs/features/<feature-slug>/reviews/prd-review.md` with Approved status.

## Self-Check

Confirm the final PRD review has exactly one `**Status:** Approved` line, was rerun after the last `create-prd` change with targeted scope where appropriate, and that no technical, spec, plan, testcase, or code artifact was created by this skill.

## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, project `AGENTS.md` forbids the planned action, review findings require a changed demo or product decision, or continuing would require guessing product behavior.
