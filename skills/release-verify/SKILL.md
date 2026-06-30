---
name: release-verify
description: "Use after local verification is complete to execute release gates, build, CI/CD release, post-release automated acceptance, and rollback readiness strictly from deploy.md, rollback.md, testing.md, progress.md, and testcase reports. Human acceptance records are optional context, not a hard gate unless project runbooks explicitly require them."
license: MIT
---

# release-verify

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/demo-implementation-alignment.md`
- `../../shared/references/release-contract.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/evidence-before-claim.md`

## Inputs

Approved reviews, final `progress.md`, latest local reports including demo parity result for UI-facing work, `docs/technical/runbooks/deploy.md`, `docs/technical/runbooks/rollback.md`, `docs/technical/standards/testing.md`, testcase reports, and optional `human-acceptance.md` when it exists or when the project release runbook requires it.

## Hard Gates

Do not guess release, CI/CD, rollback, or release gate commands. Do not create feature branches or worktrees. Verify branch state according to project release rules and `branch-stage-contract.md` before release gates. For Full feature release, start on the corresponding feature branch and stop on `develop`, `main`, `master`, detached HEAD, or a mismatched branch unless the project release runbook explicitly defines a later integration/release branch step. Block if deploy, rollback, or testing standards are missing required release instructions. Do not block merely because `human-acceptance.md` is missing, Failed, or Blocked unless the project release runbook explicitly makes human acceptance a release gate.

## Process

1. Inspect current branch according to `branch-stage-contract.md` and the project release runbook; do not switch branches unless the release runbook explicitly requires it.
2. Read deploy, rollback, and testing documents.
3. Confirm all required review gates and local verification gates are passed, including runtime demo parity evidence for UI-facing work.
4. If `human-acceptance.md` exists, read it as optional risk context. If it is Failed or Blocked, report the risk and recommended `acceptance-rework` route, but do not treat it as a hard release blocker unless project runbooks require it.
5. Run release gate and build exactly as documented.
6. Execute CI/CD or release command exactly as documented.
7. Run documented post-release black-box smoke, automated acceptance, or regression checks.
8. Record release and rollback evidence with command, exit code, report path, commit, and artifact identifiers.

## Output Contract

Update `progress.md` and reports with verification summary, optional human acceptance risk context when present, version, commit, artifact path, checksum, CI/CD link, upload or release result, post-release acceptance result, and rollback entrypoint.

## Self-Check

Confirm every release claim has fresh evidence from command output, CI/CD status, report files, and required release runbook gates. Confirm human acceptance was not treated as a hard gate unless the project release runbook explicitly requires it.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
