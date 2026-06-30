---
name: harness-init
description: "Use when a user wants to initialize, assess, or improve a project Harness by producing a guided planning document only. Triggers include harness initialization, AGENTS.md rules planning, documentation standards, local development runbooks, API mock and storage mock planning, automated verification gates, runtime evidence, Log/DB/Trace planning, release verification planning, or comparing a project's Harness maturity without directly editing the project."
license: MIT
---

# harness-init

Use this skill to guide a user through Harness initialization planning for any software project. The output is a detailed plan, not project changes. Within `opc-develop`, the plan must use `harness-doc.md` as the binding documentation convention unless the target project's `AGENTS.md` defines a stricter rule.

## Hard Boundary

- Do not create, edit, move, or delete files in the target project.
- Do not run migrations, install dependencies, start services, commit, push, or publish.
- Do inspect project files when available to make the plan concrete.
- Do ask guided questions before finalizing decisions that cannot be inferred safely.
- Do produce a planning document the user can approve before implementation.
- Do keep the plan generic to the target project and avoid hardcoding business-specific names, environments, credentials, or organization-private assumptions.

## Required References

Read before producing the plan:

- `references/planning-framework.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/mock-system-contract.md`

`planning-framework.md` contains the question flow, maturity model, required Harness dimensions, and output template. `harness-doc.md` defines the required documentation layout and artifact boundaries for feature docs, global testcases, global technical docs, reviews, progress, and changelog records. `branch-stage-contract.md` defines the default branch lifecycle baseline: early brainstorming can remain on the current branch, `product-brainstorm` creates or enters the feature branch before writing `requirement.md`, and `create-demo` plus later Full feature skills must run on that feature branch. `mock-system-contract.md` defines the API mock, storage mock, fixture isolation, and mock evidence baseline that every Harness initialization plan must address.

## Workflow

1. Identify the target project path. If absent, ask for it.
2. Inspect available project context without modifying it:
   - `AGENTS.md` or equivalent AI rules
   - README and package/build configuration
   - docs structure
   - test scripts and CI/release scripts
   - local run scripts
   - API mock, storage mock, fixture, scenario, and reset entry points
   - runtime evidence entry points such as logs, database, traces, and reports
3. Classify current Harness maturity across:
   - development process
   - documentation standards
   - local service lifecycle
   - automated verification
   - mock system and fixture isolation
   - runtime evidence
   - release and rollback verification
4. Ask guided questions in small batches. Prefer 3-7 questions per batch. Ask only for decisions not safely inferable from files.
5. Produce a detailed Harness initialization plan with phases, statuses, deliverables, dependencies, unresolved decisions, and acceptance criteria.
6. Ensure the proposed documentation structure follows `harness-doc.md`, including `docs/features/`, `docs/testcases/`, `docs/technical/`, review records, testcase index boundaries, progress records, and changelog rules.
7. Ensure the proposed development flow follows `branch-stage-contract.md` unless the target project deliberately defines a stricter rule.
8. Stop after the plan. If the user asks to implement, treat that as a separate follow-up outside this skill's scope.

## Output Contract

Return a Markdown planning document with these sections:

- `# Harness Initialization Plan`
- `## Current-State Inventory`
- `## Open Decisions`
- `## Target Harness Model`
- `## Phase Plan`
- `## Required Project Facts`
- `## Documentation Plan`
- `## Development Flow Plan`
- `## Local Runtime Plan`
- `## Mock System Plan`
- `## Automated Verification Plan`
- `## Runtime Evidence Plan`
- `## Release Verification Plan`
- `## Risks and Blockers`
- `## Acceptance Checklist`

Each phase must include `Status`, `Goal`, `Inputs`, `Actions`, `Deliverables`, `Dependencies`, `Owner/Decision Needed`, and `Acceptance Criteria`.

## Blockers

Stop and ask the user when:

- The target project path is unknown.
- Branch strategy, release authority, or production safety rules cannot be inferred.
- The project contains multiple apps or services and the harness scope is unclear.
- Verification requires credentials or protected environments not described in project docs.
- The user asks for direct implementation while still expecting planning-only behavior.
