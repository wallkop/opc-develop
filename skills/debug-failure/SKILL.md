---
name: debug-failure
description: "Use when unit tests, API tests, E2E, local verification, or human acceptance fail and the failure appears to be a pure implementation defect rather than a product, technical design, spec, testcase, or plan defect. Reproduces first, identifies root cause, adds a failing test or minimal reproduction before fixing, verifies with fresh evidence, and stops after three unsuccessful repair attempts."
license: MIT
---

# debug-failure

用于测试、API、E2E、本地验证或人工验收中的纯实现缺陷失败。先复现和根因，再补失败测试或最小复现，最后修复；三次修复失败后停止并路由回更早层级。

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/review-status-contract.md`
- `../../shared/references/tdd-contract.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/evidence-before-claim.md`

## Inputs

Failure report, command output, logs, screenshots, Runtime evidence, approved demo when UI-facing, latest `progress.md`, relevant approved artifacts, current code, project commands, and applicable project `AGENTS.md`.

## Hard Gates

Do not start by editing production code. Do not create a feature branch or worktree by default. Bugfix debugging is a current-branch workflow: default expected branch is `develop` for standalone bugfixes, while Full-flow debugging must stay on the current feature branch created by `product-brainstorm` before `requirement.md` was written. If branch context is ambiguous, stop for user confirmation. Do not treat unclear product behavior, architecture gaps, spec omissions, testcase gaps, or plan gaps as pure implementation defects. Do not claim fixed without fresh evidence. Stop after three unsuccessful repair attempts for the same issue.

## Process

1. Read the failure evidence, approved artifacts needed to classify the issue, project `AGENTS.md`, and relevant runbooks.
2. Inspect current branch and dirty state according to `branch-stage-contract.md`; do not switch branches.
3. Reproduce the failure with the smallest documented command or manual path available.
4. Classify the failure:
   - product intent changed or unclear -> route to `product-brainstorm` or `create-prd`
   - technical approach wrong -> route to `create-technical`
   - executable contract missing or contradictory -> route to `create-spec`
   - testcase missing or wrong -> route to `create-testcases`
   - plan decomposition or command wrong -> route to `create-plan`
   - approved demo mismatch caused by missing downstream contract -> route to `create-spec` or `create-plan`
   - pure implementation defect -> continue
5. Identify the root cause from code, logs, DB, trace, or reproduced behavior.
6. Add a failing test, API case, E2E assertion, or minimal reproduction that demonstrates the defect before changing production code. If automation is impossible, record the reason and the smallest manual reproduction.
7. Apply the smallest fix that addresses the root cause.
8. Run the failing check again and the relevant regression checks.
9. Record attempt number, root cause, changed files, commands, exit codes, evidence paths, and residual risk in `progress.md`.
10. If the same issue is not fixed after three attempts, stop and route to the earliest affected artifact layer or request human decision.

## Output Contract

Return language-adaptive output with:

- failure reproduction command/path and result
- root cause
- failing test or minimal reproduction added
- fix summary
- verification commands and evidence
- attempt count
- next route if unresolved

## Self-Check

Confirm the failure was reproduced before fixing, root cause is stated, a failing test or minimal reproduction exists before production changes, the fix has fresh evidence, and unresolved repeated failures are routed instead of patched blindly.
