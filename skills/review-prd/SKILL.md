---
name: review-prd
description: "Use after create-prd to review prd.md in a fresh dedicated review subagent against requirement.md and the approved demo before technical design. Writes the PRD review with Approved or Issues Found. When the PRD review is Approved, automatically commit and push the current feature branch for PM-to-RD handoff."
license: MIT
---

# review-prd

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/prompts/reviewer-common.md`
- `../../shared/prompts/prd-reviewer.md`

## Inputs

`requirement.md`, demo files, `prd.md`, current feature branch state, and git remote/upstream state.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. The reviewer must not edit product artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to technical design unless status is Approved.

When the review status is `Approved`, this skill must create one git commit on the current feature branch and push it for handoff. Do not commit or push when status is `Issues Found`. Before committing, inspect branch, upstream/remote, and dirty state. Do not commit or push unrelated dirty work, secrets, production credentials, or files outside the approved PRD-stage handoff set. If the dirty set is unsafe or ambiguous, write the review report and stop with a blocker before committing.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, `reviewer-common.md`, and `prd-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent compares PRD to raw requirement and approved demo.
4. The review subagent checks that `prd.md` contains an explicit demo alignment contract or explains intentional non-binding demo elements.
5. The review subagent checks goals, non-goals, scope, user flow, states, rules, permissions, and acceptance criteria.
6. For re-review after `Issues Found`, default to targeted fresh review against previous blocking issues and changed PRD sections unless the revision changes the PRD's main semantics.
7. Write review report from the review subagent result without weakening its status or blocking issues.
8. Parse the review status. If status is `Issues Found`, do not commit or push; report the review path and route back to `create-prd`.
9. If status is `Approved`, run `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, and inspect upstream/remote with `git rev-parse --abbrev-ref --symbolic-full-name @{u}` or `git remote -v`.
10. Verify the current branch is the matching `feature/<numbered-slug>` or a project-approved feature branch equivalent. Do not switch branches.
11. Verify the dirty set is limited to PRD-stage handoff work: the feature's requirement, demo/prototype evidence and assets, PRD, demo/PRD reviews, progress/changelog, and frontend prototype files explicitly documented in `demo/prototype.md`. If other files are dirty, stop before commit and report the paths.
12. Resolve the push target before committing. If an upstream exists, plan to use `git push`. If no upstream exists but `origin` exists, plan to use `git push -u origin HEAD`. If no push target exists, stop and report a blocker before committing.
13. Stage only the verified handoff set. Commit with `docs: approve PRD for <feature-slug>`.
14. Push the current branch using the resolved push command.

## Output Contract

Write `docs/features/<feature-slug>/reviews/prd-review.md` with exactly one status line. When status is `Approved`, also leave the current feature branch committed and pushed, and report the commit SHA and push target.

## Self-Check

Confirm the report was authored by a fresh review subagent and blocking issues are precise enough for `create-prd` to revise. If status is `Approved`, confirm exactly one handoff commit was created on the current feature branch, no unrelated dirty files were included, the commit contains the PRD review, and push succeeded or was blocked before commit because no safe push target existed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
