---
name: review-technical
description: "Use after create-technical to review technical.md in a fresh dedicated review subagent before spec creation. Checks one committed route, SaaS/infrastructure choices, project datastore/database baseline compliance, public API input/output contracts, system boundaries, demo alignment, Runtime evidence strategy, and that micro implementation details are left to spec."
---

# review-technical

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
- `../../shared/prompts/reviewer-common.md`
- `../../shared/prompts/technical-reviewer.md`

## Inputs

`requirement.md`, approved demo, approved `prd.md`, `technical.md`, relevant code and docs.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. Reviewer must not edit artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to spec unless status is Approved.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, applicable project technical docs, `reviewer-common.md`, and `technical-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent checks PRD and approved demo alignment, one committed technical route, component selection, SaaS decisions, project datastore/database baseline compliance, public API input/output contracts, module boundaries, data/API/UI impact, demo-to-implementation module mapping for UI-facing work, compatibility, migration, security, performance, operations, Runtime evidence, risks, and the boundary with `spec.md`.
4. For re-review after `Issues Found`, default to targeted fresh review against the previous blocking issues, changed `technical.md` sections, and directly affected boundary contracts unless the revision changes the design's main semantics.
5. Write review report from the review subagent result without weakening its status or blocking issues.

## Output Contract

Write `docs/features/<feature-slug>/reviews/technical-review.md`.

## Self-Check

Confirm the report was authored by a fresh review subagent, status line exists, and issues distinguish blockers from advisory notes.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
