---
name: local-e2e-verify
description: "Use after tdd-coding integration succeeds to run local black-box end-to-end, acceptance, smoke, regression, and runtime demo parity verification strictly from local-dev runbook, testing standard, approved demo, product testcases, and Runtime Log, DB, and Trace evidence entries."
license: MIT
---

# local-e2e-verify

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/local-e2e-contract.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/evidence-before-claim.md`

## Inputs

Completed code after `tdd-coding`, approved demo when UI-facing, `prd.md`, `spec.md`, `docs/technical/runbooks/local-dev.md`, `docs/technical/standards/testing.md`, relevant black-box `docs/testcases/`, and Runtime evidence entries.

## Hard Gates

Do not guess local start, stop, status, log, test, or evidence commands. Do not create, switch, merge, or delete branches. In Full flow, verify on the current feature branch created by `product-brainstorm` or a project-approved equivalent. Stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch. Block if required runbook or testing instructions are missing. For UI-facing features, block if the approved demo or demo-review evidence is missing because runtime demo parity cannot be verified.

## Process

1. Inspect current branch according to `branch-stage-contract.md`; do not switch branches.
2. Read local-dev runbook and testing standard.
3. Start local services exactly as documented.
4. Run status and health checks.
5. Execute relevant black-box E2E, smoke, acceptance, or regression commands.
6. For UI-facing work, capture runtime screenshots, interaction recordings, Browser/Computer Use notes, or equivalent evidence and compare visible layout/interactions/states against the approved demo and testcase expectations.
7. Capture reports, screenshots, logs, DB evidence, and trace evidence.
8. If a check fails because of a pure implementation defect, route through `debug-failure`; if the failure reveals wrong upstream artifacts, route to the earliest affected skill using `demo-implementation-alignment.md`.
9. Stop or leave services according to project runbook.
10. Update `progress.md` only with evidence-backed status.

## Output Contract

Write reports under `docs/testcases/<product-module>/reports/` and update `progress.md` with evidence paths, demo parity result for UI-facing work, and residual risk.

## Self-Check

Confirm commands are fresh, exit codes are known, evidence paths exist, and runtime demo parity was checked for UI-facing work before claiming local verification passed.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
