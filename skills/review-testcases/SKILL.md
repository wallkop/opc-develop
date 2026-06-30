---
name: review-testcases
description: "Use after create-testcases to review black-box feature testcases.md and real docs/testcases E2E, acceptance, and regression files in a fresh dedicated review subagent against approved demo, PRD, and spec before plan creation. Reject testcase artifacts that contain unit-test, API-test, white-box, mock, or TDD implementation design."
license: MIT
---

# review-testcases

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
- `../../shared/prompts/testcase-reviewer.md`

## Inputs

Approved demo when UI-facing, approved `prd.md`, approved `spec.md`, feature `testcases.md`, real black-box testcase files under `docs/testcases/`.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. Reviewer must not edit artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to plan creation unless status is Approved.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, `reviewer-common.md`, and `testcase-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent checks acceptance criteria mapping, approved demo-critical layout/interactions/states for UI-facing work, black-box E2E/acceptance/regression coverage, executable steps, expected results, automation entrypoints, and failure diagnostics.
4. The review subagent confirms index paths point to real files.
5. The review subagent rejects unit-test, API-test, white-box fixture, mock, or TDD command content in testcase artifacts.
6. For re-review after `Issues Found`, default to targeted fresh review against previous blocking issues and changed testcase/index files unless the revision changes testcase semantics broadly.
7. Write review report from the review subagent result without weakening its status or blocking issues.

## Output Contract

Write `docs/features/<feature-slug>/reviews/testcase-review.md`.

## Self-Check

Confirm the report was authored by a fresh review subagent and issues identify missing criteria, missing paths, non-executable steps, or black-box/white-box boundary violations.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
