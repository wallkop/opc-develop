---
name: create-demo
description: "Use after product-brainstorm when requirement.md exists and a high-fidelity product demo is needed before PRD. Builds the demo directly in the real frontend codebase on the feature branch, uses frontend-only mocks for missing backend data, restarts local frontend/backend services, and returns a preview URL plus evidence."
license: MIT
---

# create-demo

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/prototype-mock-retirement-contract.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/demo-contract.md`

## Inputs

`requirement.md`, brainstorm decisions, project frontend code, project visual references or existing product UI, local-dev runbook, and project mock conventions when available.

## Hard Gates

Do not write PRD, technical design, spec, plan, or testcase artifacts. Do not create a feature branch or worktree. This is a feature-branch-only workflow: the current branch must be `feature/<numbered-slug>` or a project-approved equivalent before writing demo artifacts. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch.

Allowed code changes are frontend-only prototype changes. Strictly do not modify backend code, API handlers, database schemas, migrations, infrastructure, server jobs, or production storage logic. Any missing backend behavior must be simulated with frontend-only mocks.

Do not downgrade to a standalone static HTML demo when a real frontend exists. When the product already has a real frontend shell, route, page, header, sidebar, input area, or workspace surface for the requested user flow, the demo's primary path must be integrated into that shell. A query-param-only alternate root app, standalone demo route, isolated mock page, or detached playground is not sufficient as the primary demo surface.

`?demo=<feature>` and similar switches may seed frontend-only mocks, select scenarios, or unlock reviewer states, but they must not be the only way to see the feature entry or main state when a real shell exists. The normal product URL or route must visibly expose the intended production entry point or a reviewer-visible mock state.

Do not bypass the real shell to avoid frontend integration work. If integrating the shell path would require backend, database, Electron, infrastructure, or production storage changes, keep those missing capabilities mocked in frontend code. Stop only when the frontend/backend boundary is genuinely unclear.

Do not claim demo completion without restarting local services and giving the user a preview URL.

## Process

1. Read `requirement.md`, applicable `AGENTS.md`, local-dev runbook, and frontend architecture/design-system context.
2. Verify current branch is the corresponding feature branch according to `branch-stage-contract.md`; do not switch branches.
3. Identify frontend and backend ownership boundaries. If the boundary is unclear, stop before editing.
4. Inspect the existing frontend UI enough to match product visual language, layout density, component conventions, routes, state management, interaction style, and the real shell surfaces where the feature should enter, display status, switch views, and exit.
5. Implement the demo in real frontend code: routes, components, stores, styles, interactions, and state rendering. The primary demo path must use the intended production shell and entry/exit surfaces. Aim for at least 80% of the final frontend experience.
6. For unavailable backend behavior, add explicit frontend-only mocks using the narrowest viable mechanism: fixture, adapter/interceptor, store seed, route guard, mock provider, or component-local fake data. Do not touch backend code.
7. Record every mock in `docs/features/<feature-slug>/demo/prototype.md` with file path, mock type, scenarios, simulated backend behavior, enablement switch, and expected real replacement owner.
8. Cover happy path and requirement-relevant empty, loading, error, permission, confirmation, and success states in runtime through the real shell path whenever the product has one.
9. After every edit batch, restart local services according to the documented local-dev runbook, including backend and frontend services or the documented combined stack. Run status/health checks.
10. Capture or record preview evidence: URL, branch, commands, exit codes, screenshots or recordings when useful, changed frontend files, mock inventory, and residual gaps.
11. Give the user the preview URL and a concise acceptance checklist for product-sense review.

## Output Contract

Produce working frontend code plus `docs/features/<feature-slug>/demo/prototype.md` with preview URL, commands, evidence, changed frontend files, mock inventory, and remaining gaps. Optional screenshots or recordings may live under `docs/features/<feature-slug>/demo/assets/`.

## Self-Check

Confirm the runtime frontend prototype reaches at least 80% frontend fidelity, the primary path is visible in the real product shell when one exists, local services were restarted, preview URL works, no backend files changed, all new backend-dependent behavior is frontend-mocked, mock inventory is complete, and downstream demo alignment decisions are discoverable. If this run revised an already reviewed demo, report that `review-demo` must be rerun before PRD work can proceed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
