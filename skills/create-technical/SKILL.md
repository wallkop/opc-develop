---
name: create-technical
description: "Use after review-prd is Approved to create the feature technical design for human architecture review. Commits to one technical route, SaaS/infrastructure choices such as datastore/database, cache, queue, object/blob storage, and providers, public API input/output contracts, system boundaries, migration, security, Runtime evidence, and gate strategy; leaves internal implementation details to spec."
license: MIT
---

# create-technical

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/artifact-boundary-contract.md`
- `../../shared/references/technical-format.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/runtime-evidence-contract.md`

## Inputs

Approved `prd.md`, `requirement.md`, approved frontend prototype evidence, prototype mock inventory, project code, and `docs/technical/`.

## Hard Gates

`reviews/prd-review.md` must be Approved. Do not write spec, plan, testcase, code, feature branch, or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent before writing technical artifacts. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

## Process

1. Read project `AGENTS.md`, PRD, approved frontend prototype evidence, mock inventory, and global technical docs.
2. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
3. Inspect code paths enough to understand existing architecture.
4. Commit to exactly one technical route and one component selection. Do not leave multiple viable options for downstream AI to choose.
5. Put all SaaS / infrastructure decisions in `technical.md`, including datastore/database, cache, queue, object/blob storage, external APIs, model providers, auth services, and audit services. If a new or changed datastore/database is involved, follow the target project's existing architecture baseline or an explicit human-approved decision; if no baseline exists or existing facts conflict, block for a human architecture decision instead of choosing implicitly.
6. Define public API input/output contracts in `technical.md`: endpoint, method, request schema, response schema, status code, error code, auth/permission boundary, and external dependency failure semantics.
7. For UI-facing work, map the approved frontend prototype and PRD demo alignment contract to real frontend modules, routes, components, state owners, and design-system constraints.
8. Define the real backend/API/storage contracts needed to replace frontend prototype mocks. Technical owns public API input/output and SaaS/storage choices; do not leave mock replacement decisions to downstream AI.
9. Document architecture-level approach, module boundaries, public API contracts, SaaS/data/UI impacts, mock replacement architecture, compatibility, migration, security, performance, operations, Runtime evidence, gate classification, and risks.
10. Keep internal module placement, local components such as sqlite/local storage/cache, state machines, internal error mappings, mock retirement execution details, and TDD seed lists for `spec.md`.
11. Mark high-impact unknowns as blockers.

## Output Contract

Write `docs/features/<feature-slug>/technical.md`.

## Self-Check

Confirm technical design commits to one route, owns SaaS choices and public API I/O, explains module boundaries, maps approved frontend prototype to real implementation, defines real backend/API/storage replacement for prototype mocks, and states where Log, DB, and Trace evidence will come from without becoming a duplicate executable spec. If this run revised an already reviewed technical design, report that `review-technical` must be rerun before downstream development can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
