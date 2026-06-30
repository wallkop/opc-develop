---
name: build-technical
description: "Use after build-prd or review-prd is Approved when the user wants technical design creation and review handled as one loop. Runs create-technical, review-technical, and reruns create-technical when technical-review.md has Issues Found until the technical review is Approved or blocked."
license: MIT
---

# build-technical

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/technical-format.md`
- `../../shared/references/runtime-evidence-contract.md`

## Inputs

Approved `prd.md`, `reviews/prd-review.md`, `requirement.md`, approved demo, project code, and `docs/technical/`.

## Hard Gates

`reviews/prd-review.md` must be fresh Approved. Do not write spec, plan, testcase, code, feature branch, or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not bypass `review-technical`. `review-technical` must run in its own fresh review subagent; this build skill must not review the technical design inline. Do not proceed to `loop-develop` unless `reviews/technical-review.md` is fresh Approved for the current `technical.md` revision.

## Process

Run this sequence:

1. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
2. Run `create-technical`.
3. Run `review-technical` in a fresh dedicated review subagent with only necessary review inputs.
4. If `reviews/technical-review.md` is `Issues Found`, rerun `create-technical` using the review findings as required revision input.
5. Treat the previous technical review as stale after every `create-technical` revision.
6. Rerun `review-technical` in a fresh dedicated review subagent after each technical design revision; default to targeted review of blocking issues and changed technical sections unless the revision changes the design's main semantics.
7. Stop only when `reviews/technical-review.md` is fresh Approved for the latest technical design or a blocker is reached.

## Output Contract

Produce `docs/features/<feature-slug>/technical.md` and `docs/features/<feature-slug>/reviews/technical-review.md` with Approved status.

## Self-Check

Confirm the final technical review has exactly one `**Status:** Approved` line, was rerun after the last `create-technical` change with targeted scope where appropriate, and that no spec, plan, testcase, or code artifact was created by this skill.

## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, project `AGENTS.md` forbids the planned action, review findings require PRD/demo changes, or continuing would require guessing architecture or technical decisions.
