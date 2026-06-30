---
name: loop-develop
description: "Use after product confirmation, approved demo, approved PRD, and review-technical are Approved to run the long-task development loop only. Runs create-spec, review-spec, create-testcases, review-testcases, create-plan, review-plan, tdd-coding, and local-e2e-verify with targeted re-review after fixes. Does not create PRD, demo, technical design, or release."
license: MIT
---

# loop-develop

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/development-input-contract.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/subagent-execution-contract.md`
- `../../shared/references/local-e2e-contract.md`
- `../../shared/references/evidence-before-claim.md`

## Inputs

Approved demo and `reviews/demo-review.md`, approved `prd.md`, approved `technical.md`, project code, project commands, Runtime entries, and applicable project `AGENTS.md`.

## Hard Gates

Do not run unless `reviews/demo-review.md`, `reviews/prd-review.md`, and `reviews/technical-review.md` are fresh Approved for the latest demo, PRD, and technical design. Do not create demo, PRD, technical design, or release artifacts. Do not create a feature branch in this orchestrator; the feature branch must already exist from `product-brainstorm` before `requirement.md` was written. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Every `review-*` gate in this loop must be executed in a fresh dedicated review subagent, never inline inside this orchestrator.

## Process

Run this sequence exactly:

1. `create-spec`; it verifies the current feature branch according to `branch-stage-contract.md` but must not create or switch branches.
2. `review-spec` in a fresh dedicated review subagent. If `Issues Found`, return to `create-spec`, treat the previous spec review as stale after the revision, and rerun targeted fresh `review-spec` focused on blocking issues and changed sections unless semantics changed.
3. `create-testcases`
4. `review-testcases` in a fresh dedicated review subagent. If `Issues Found`, return to `create-testcases`, treat the previous testcase review as stale after the revision, and rerun targeted fresh `review-testcases` focused on blocking issues and changed testcase areas unless semantics changed.
5. `create-plan`
6. `review-plan` in a fresh dedicated review subagent. If `Issues Found`, return to `create-plan`, treat the previous plan review as stale after the revision, and rerun targeted fresh `review-plan` focused on blocking issues, changed plan sections, and affected workstream boundaries unless semantics changed.
7. `tdd-coding`; this stage must dispatch implementer subagents, read the complete development input set, and block if subagent execution is unavailable.
8. `local-e2e-verify`

Every creator/reviewer pair must stop only on a fresh Approved review authored by an isolated review subagent for the latest artifact revision. Use targeted re-review after fixes per `review-trigger-policy.md`; do not run unnecessary full review loops. Do not proceed from `create-spec` to `create-testcases`, from `create-testcases` to `create-plan`, or from `create-plan` to `tdd-coding` using an Approved review that was written before the latest creator change.

## Output Contract

Produce approved spec, approved testcase coverage, approved plan tree, code/test changes, local E2E evidence, runtime demo parity evidence for UI-facing work, and updated `progress.md`. Every completion claim must be backed by fresh evidence. If human acceptance later fails, use `acceptance-rework` before re-entering this loop or a lower-level skill.

## Self-Check

Confirm the shortcut did not alter any atomic skill input/output contract, did not bypass review gates, used targeted re-review after fixes where appropriate, and each spec/testcase/plan review was authored by a fresh review subagent after the last matching creator revision.

## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
