---
name: acceptance-rework
description: "Use after local-e2e-verify when human acceptance feedback fails, is blocked, or requests changes. Records optional human acceptance feedback, classifies the earliest affected artifact layer, updates human-acceptance.md and progress.md, and routes rework back to the correct upstream skill instead of blindly rerunning loop-develop."
license: MIT
---

# acceptance-rework

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/human-acceptance-contract.md`
- `../../shared/references/review-status-contract.md`

## Inputs

Human acceptance feedback, screenshots or recordings when available, latest `progress.md`, latest local verification report, `requirement.md`, approved demo and demo review, `prd.md`, `technical.md`, `spec.md`, `testcases.md`, `plan/*.md`, and relevant project `AGENTS.md`.

## Hard Gates

Do not edit demo, PRD, technical design, spec, testcase, plan, or code artifacts in this skill. Do not create, switch, merge, or delete branches. For Full feature rework, operate only on the corresponding feature branch and stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Do not run release verification. Do not treat failed human acceptance as a coding task until the earliest affected artifact layer is identified.

## Process

1. Read the human feedback and evidence exactly as provided.
2. Inspect current branch according to `branch-stage-contract.md`; do not switch branches.
3. Read upstream artifacts only enough to determine whether the feedback conflicts with requirement, approved demo, PRD, technical design, spec, testcase coverage, plan, or implementation.
4. Classify the earliest affected layer:
   - `product-brainstorm` when product intent, scope, user path, or core decision changed.
   - `create-demo` when the accepted product experience needs a revised frontend prototype before PRD changes.
   - `create-prd` when product behavior, rules, permissions, states, fields, or acceptance criteria are wrong or incomplete.
   - `create-technical` when architecture, module boundaries, contracts, data, migration, security, performance, operations, or Runtime evidence strategy is wrong.
   - `create-spec` when executable behavior, interfaces, data models, state, errors, rollout, rollback, security, or verification points are incomplete or contradictory.
   - `create-testcases` when acceptance criteria are correct but coverage, expected results, automation entrypoints, or diagnostics are missing.
   - `create-plan` when the plan decomposition, branch strategy, dependencies, or TDD commands are wrong.
   - `debug-failure` when approved demo, PRD, technical design, spec, testcases, and plan already cover the feedback and the failure is a pure implementation defect with reproducible evidence.
   - `tdd-coding` when the approved plan remains correct but additional planned implementation work or subagent execution is required.
5. Write or update `human-acceptance.md` with status, evidence, classification, earliest affected artifact, rework entrypoint, required review gates, and release impact/risk context.
6. Update `progress.md` with the acceptance result, selected rework path, blockers, and residual risk.
7. Stop after routing unless the user explicitly asks to continue into the selected next skill.

## Output Contract

Write `docs/features/<feature-slug>/human-acceptance.md` following the human acceptance contract. Update `docs/features/<feature-slug>/progress.md`.

## Self-Check

Confirm the selected next skill is the earliest layer that can fix the acceptance failure. Confirm human acceptance is recorded as optional release context and is not a `release-verify` hard gate unless the project release runbook explicitly requires it.

## Blockers

Stop and report a blocker when feedback is too vague to classify, evidence is missing for a disputed failure, required artifacts are missing, an upstream review is not Approved, project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
