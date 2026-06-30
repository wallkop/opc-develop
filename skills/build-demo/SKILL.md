---
name: build-demo
description: "Use after product-brainstorm when requirement.md exists and the user wants frontend prototype creation and review handled as one loop. Runs create-demo, review-demo, and reruns create-demo when demo-review.md has Issues Found until the running frontend prototype review is Approved or blocked."
license: MIT
---

# build-demo

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/demo-contract.md`

## Inputs

`requirement.md`, brainstorm decisions, project frontend code, local-dev runbook, visual references, and existing product UI when available.

## Hard Gates

Do not write PRD, technical design, spec, plan, testcase, backend code, feature branch, or worktree. Frontend prototype code changes are allowed only through `create-demo`. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not bypass `review-demo`. `review-demo` must run in its own fresh review subagent; this build skill must not review the demo inline. Do not proceed to PRD unless `reviews/demo-review.md` is fresh Approved for the current frontend prototype revision.

## Process

Run this sequence:

1. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
2. Run `create-demo`.
3. Run `review-demo` in a fresh dedicated review subagent with only necessary review inputs.
4. If `reviews/demo-review.md` is `Issues Found`, rerun `create-demo` using the review findings as required revision input.
5. Treat the previous demo review as stale after every `create-demo` revision.
6. Rerun `review-demo` in a fresh dedicated review subagent after each demo revision; default to targeted review of blocking issues and changed demo regions unless the revision changes the demo's main semantics.
7. Stop only when `reviews/demo-review.md` is fresh Approved for the latest demo or a blocker is reached.

## Output Contract

Produce running frontend prototype code, `docs/features/<feature-slug>/demo/prototype.md`, optional preview assets, and `docs/features/<feature-slug>/reviews/demo-review.md` with Approved status.

## Self-Check

Confirm the final demo review has exactly one `**Status:** Approved` line, was rerun after the last `create-demo` change with targeted scope where appropriate, and that no downstream PRD, technical, spec, plan, testcase, or backend artifact was created by this skill.

## Blockers

Stop and report a blocker when required inputs are missing, the project `AGENTS.md` forbids the planned action, review findings require an unapproved product decision, or repeated review failures reveal unclear requirements that must return to `product-brainstorm`.
