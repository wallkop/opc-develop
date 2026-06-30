---
name: review-spec
description: "Use after create-spec to review spec.md in a fresh dedicated review subagent before testcase creation. Checks executable internal implementation contracts, local component decisions, UI/demo parity, TDD seed readiness, no technical.md duplication, no SaaS decision leakage, and no public API I/O redefinition."
license: MIT
---

# review-spec

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/prompts/reviewer-common.md`
- `../../shared/prompts/spec-reviewer.md`

## Inputs

`requirement.md`, approved frontend prototype evidence and demo review, prototype mock inventory, approved `prd.md`, approved `technical.md`, `spec.md`.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. Reviewer must not edit artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to testcase creation unless status is Approved.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, `reviewer-common.md`, and `spec-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent checks requirement, approved demo, PRD, and technical alignment.
4. The review subagent checks executable internal completeness, demo parity contract completeness for UI-facing work, prototype mock retirement completeness when mocks exist, technical/spec boundary, no public API I/O redefinition, no SaaS decision leakage into spec, excessive semantic duplication with `technical.md`, TDD seed readiness, and hidden decision risks.
5. For re-review after `Issues Found`, default to targeted fresh review against previous blocking issues, changed `spec.md` sections, and directly affected boundary contracts unless the revision changes the spec's main semantics.
6. Write review report from the review subagent result without weakening its status or blocking issues.

## Output Contract

Write `docs/features/<feature-slug>/reviews/spec-review.md`.

## Self-Check

Confirm the report was authored by a fresh review subagent and blocking issues identify exact missing, duplicated, non-executable, demo-divergent, or contradictory spec content.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
