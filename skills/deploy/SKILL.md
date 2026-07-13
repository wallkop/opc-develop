---
name: deploy
description: "Use when one or more increments have a fresh human-accepted acceptance receipt and are merged to trunk, to release them to production safely: fail-closed preflight, production environment changes with backups/rollback, deploy per runbook, prod-safe regression, and a watch window. Every destructive step requires explicit human confirmation."
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

Resume after the last `release` ledger entry with `result: ok`.

1. **preflight (fail-closed, all mandatory)**:
   - **define the release set first**: the features whose merge commits landed on the trunk
     since the last `deploy-prod: ok` ledger entry (or release tag), or an explicit
     human-declared list. Record the set — slugs + merge commits — in the ledger; everything
     below is checked per feature in the set;
   - all released code merged to the trunk (`develop` or per AGENTS.md) — verify the merge
     commits, not the claim;
   - after the release set is fixed and all merge commits are present, refresh every receipt once
     on that same combined trunk: run cheap checks, each increment's core journey, and focused
     regression, then obtain the human verdict again. This is the documented reconciliation for
     whole-tree fingerprints; a later merge intentionally stales earlier evidence. Use offline
     replay before at most one release-set provider canary when that provider path changed;
   - test acceptance recorded `ok` in the ledger for every increment, and
     `opc_increment.py check --require human-accepted` passes for each refreshed receipt; optional
     legacy artifact chains are checked only when those artifacts exist;
   - release manifests complete for every feature: every DDL item has a rollback entry, every
     env var is provisioned (names verified, values via human/secret manager), every third-party
     item has an owner;
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
4. **regression-prod**: run the approved `@prod-safe` testcase subset through the project runner — read-only
   evidence triangle (interface + correlation-ID logs + state queries). Untagged specs never run
   here. Record `external provider passed` / real-surface labels only for what actually ran.
5. **watch**: monitor the runbook's signals (error rates, key logs, business metrics) for its
   stated window. Anomaly ⇒ the decision is rollback-first: propose the rollback path
   immediately, fix-forward only with the human's explicit choice.
6. **close**: final ledger entries (stages, backups, evidence), residual gaps carried forward,
   suggest `retro`. Write the human handoff under `docs/opc/deploy/` as markdown truth plus a
   rendered/linted HTML companion using plain language and first-use term explanations.

## Rework

A defect found in production during or after deploy is `oncall`'s territory — diagnose there;
hotfixes flow back through `build` → `ship` → `deploy` on the expedited path `oncall` defines.

## Output

Released production feature with staged evidence, backups and rollback paths recorded, watch
window observed, plus the Markdown/HTML human handoff under `docs/opc/deploy/`.
