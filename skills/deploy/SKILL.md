---
name: deploy
description: "Use when one or more human-accepted Lite or Build increments are merged to trunk and should release to production safely. Build uses fresh acceptance receipts; Lite uses test acceptance, focused evidence, matching risk checks, and the project's complete release gate. Performs fail-closed preflight, backups/rollback, runbook deployment, prod-safe regression, and a watch window. Every destructive step requires explicit human confirmation."
license: MIT
---

# deploy

Production release as its own flow. Where every other skill fails open, this one fails closed:
no verified precondition, no deploy.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/release-ops.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Stages

When the project has a release ledger, resume after the last `release` entry with `result: ok`.

1. **preflight (fail-closed, all mandatory)**:
   - **define the release set first**: the increments whose merge commits landed on the trunk
     since the last `deploy-prod: ok` ledger entry (or release tag), or an explicit
     human-declared list. Record the set — increment/slug when one exists + merge commits — through
     the project release mechanism; everything below is checked per increment in the set;
   - all released code merged to the trunk (`develop` or per AGENTS.md) — verify the merge
     commits, not the claim;
   - after the release set is fixed and all merge commits are present, refresh evidence once on the
     same combined trunk. For Build, refresh every receipt, core journey, and focused regression.
     For Lite, rerun its focused regressions, matching risk checks, relevant real-entry checks, and
     the project's complete release/predeploy gate. Use offline replay before at most one
     release-set provider canary when that provider path changed;
   - test acceptance recorded `ok` for every increment. Build additionally requires
     `opc_increment.py check --require human-accepted` for each refreshed receipt. Lite requires
     commit-bound command/exit/evidence records through the project's native release mechanism;
     optional artifact chains are checked only when those artifacts exist;
   - applicable release records are complete for every increment: every DDL item has a rollback
     entry, every env var is provisioned (names verified, values via human/secret manager), and
     every third-party item has an owner;
   - rollback readiness proven: previous version identifiable and redeployable, down path for
     every DDL item or explicit human ack of `[ONE-WAY]` migrations;
   - production runbook (deploy + rollback) exists and was read. Any miss ⇒ stop and report;
     do not improvise production mechanics.
2. **env-prod**: apply environment changes in manifest order — backup before every DDL touching
   existing data (record backup paths in the ledger), data backfills (idempotent, scoped, dry-run
   first when the runbook allows), config and server changes. Each destructive item gets its own
   human confirmation; batch approval is not a thing here.
3. **deploy-prod**: release per the project runbook (canary/staged rollout when the runbook
   defines one), with explicit human confirmation to start.
4. **regression-prod**: for Build, run the approved `@prod-safe` testcase subset through the project
   runner. For Lite, run the project's prod-safe focused checks for the touched path and reuse a
   matching tagged testcase when one exists. Keep production checks read-only unless the runbook
   and human explicitly authorize mutation. Record real-surface labels only for what actually ran.
5. **watch**: monitor the runbook's signals (error rates, key logs, business metrics) for its
   stated window. Anomaly ⇒ the decision is rollback-first: propose the rollback path
   immediately, fix-forward only with the human's explicit choice.
6. **close**: final ledger entries (stages, backups, evidence), residual gaps carried forward,
   suggest `retro`. Write the human handoff under `docs/opc/deploy/` as markdown truth plus a
   rendered/linted HTML companion using plain language and first-use term explanations.

## Rework

A defect found in production during or after deploy is `oncall`'s territory. Classify the fix by
the same Lite/Build triggers, then return through `ship` → `deploy`.

## Output

Released production increment with staged evidence, backups and rollback paths recorded, watch
window observed, plus the project-native human handoff.
