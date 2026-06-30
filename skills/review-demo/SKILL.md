---
name: review-demo
description: "Use after create-demo to review the running frontend prototype in a fresh dedicated review subagent against requirement.md, project visual expectations, frontend-only mock rules, preview evidence, and 80% fidelity before PRD creation. Writes the demo review with Approved or Issues Found."
license: MIT
---

# review-demo

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/demo-contract.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/review-trigger-policy.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/prompts/reviewer-common.md`
- `../../shared/prompts/demo-reviewer.md`

## Inputs

`requirement.md`, frontend prototype changed files or diff summary, `demo/prototype.md`, runtime preview URL/evidence, mock inventory, screenshots or recordings when available, and visual references when available.

## Hard Gates

This skill must run in a fresh dedicated review subagent. The main controller must not review inline. If no subagent execution is available, stop and report a blocker. The reviewer must not edit demo or product artifacts. Do not create, switch, merge, or delete branches; write the review only on the corresponding feature branch according to `branch-stage-contract.md`. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not proceed to PRD unless status is Approved.

When a real frontend shell exists, reject demos whose primary path bypasses that shell. A query-param-only alternate root app, standalone demo route, isolated mock page, or detached playground may be reviewed only as secondary evidence, not as the primary demo surface.

## Process

1. The main controller starts a fresh review subagent for this review only.
2. Provide only the required inputs, applicable project visual references, `reviewer-common.md`, and `demo-reviewer.md`; do not include creator chat history, suspected issues, desired outcome, or unrelated context.
3. The review subagent reviews requirement coverage, runtime preview evidence, 80% frontend fidelity, project visual alignment, key states, interaction completeness, frontend-only mock discipline, absence of backend code changes, and whether the primary demo path uses the intended real product shell.
4. The review subagent rejects static-only demos when a real frontend exists, query-param-only alternate root demos when the normal shell should carry the feature, missing preview URL/service restart evidence, backend modifications, unrecorded mocks, or product-sense gaps that prevent PRD alignment.
5. The review subagent rejects as `Issues Found` when the intended production entry point is documented but not visible in the running UI, or when existing navigation/header/sidebar/input/workspace surfaces are not touched even though the requirement depends on them.
6. For re-review after `Issues Found`, default to targeted fresh review against previous blocking issues and changed demo regions unless the revision changes the demo's main semantics.
7. Write the review report from the review subagent result without weakening its status or blocking issues.

## Output Contract

Write `docs/features/<feature-slug>/reviews/demo-review.md` with exactly one status line and explicit notes on frontend fidelity, real shell integration, backend-change absence, mock inventory completeness, and preview evidence.

## Self-Check

Confirm the report was authored by a fresh review subagent, status line matches the review status contract, and blocking issues are actionable.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
