---
name: loop-design
description: "Use after product-brainstorm when requirement.md exists and the user wants the pre-development design loop completed end-to-end. Runs build-demo, build-prd, and build-technical in order until demo, PRD, and technical reviews are Approved or blocked. Does not create spec, testcases, plan, code, local verification, acceptance, or release artifacts."
license: MIT
---

# loop-design

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
- `../../shared/references/demo-contract.md`
- `../../shared/references/prd-format.md`
- `../../shared/references/technical-format.md`
- `../../shared/references/runtime-evidence-contract.md`

## Inputs

`requirement.md`, brainstorm decisions, project visual references, project code context, `docs/technical/`, and applicable project `AGENTS.md`.

## Hard Gates

Do not run without `requirement.md`. Do not create spec, testcase, plan, code, local verification, human acceptance, release artifacts, feature branch, or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not bypass any review gate. Every review gate must be executed by its matching `review-*` skill in a fresh dedicated review subagent, never inline inside this orchestrator. Do not enter `loop-develop` unless `reviews/prd-review.md` and `reviews/technical-review.md` are fresh Approved for the latest artifacts.

## Process

Run this sequence exactly:

1. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
2. `build-demo`; if blocked, stop and report the blocker.
3. `build-prd`; if blocked, stop and report the blocker.
4. `build-technical`; if blocked, stop and report the blocker.

Each build skill owns its creator/reviewer revision loop and must end with a fresh Approved review authored by an isolated review subagent after the last creator revision before the next build skill starts. After `Issues Found`, use targeted fresh re-review focused on blocking issues and changed regions unless the revision changes the artifact's main semantics.

## Output Contract

Produce approved demo, approved PRD, approved technical design, and updated review files:

- `docs/features/<feature-slug>/demo/prototype.md`
- `docs/features/<feature-slug>/reviews/demo-review.md`
- `docs/features/<feature-slug>/prd.md`
- `docs/features/<feature-slug>/reviews/prd-review.md`
- `docs/features/<feature-slug>/technical.md`
- `docs/features/<feature-slug>/reviews/technical-review.md`

## Self-Check

Confirm demo, PRD, and technical reviews each have exactly one `**Status:** Approved` line, each review was authored by a fresh review subagent, and each review was rerun after the last matching creator revision with targeted scope where appropriate. Confirm the shortcut did not alter any atomic skill input/output contract or bypass review gates.

## Blockers

Stop and report a blocker when required inputs are missing, a build stage cannot reach Approved, project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
