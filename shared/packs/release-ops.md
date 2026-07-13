# Release Ops

Manifest collection, environment-change safety, and regression rules shared by `ship` (test
environment), `deploy` (production), and standard increments with local environment changes.

## Release Manifest — `docs/features/<slug>/release-manifest.md`

```
# Release Manifest: <feature>            (commit range: <base>..<head>)

## Migrations / DDL
- M1: <file/path> — what it changes — rollback: <down path | backup-restore | [ONE-WAY] + human ack>
## Environment Variables
- NAME (new|changed) — purpose — secret: yes/no (names only, never values) — set in: test [ ] prod [ ]
## Config Changes
- <file/key> — old → new — reason (TD-n when one exists; otherwise result-card constraint)
## Services / Jobs
- <new or changed service, queue, cron> — start/stop/scale notes
## Third-party / Provider
- <dashboard settings, webhooks, API scopes> — who applies it (agent | human handoff)
## Data Backfills
- <script/command> — idempotent: yes/no — estimated scope
## Not Releasing
- <changes in the diff deliberately excluded, with reason>
```

## Collection Rules

- Source of truth is the **actual diff** (migrations dir, config files, env references, service
  definitions), cross-checked against `feature-plan.md` and any optional technical decision record.
- Diff outside the result-card scope is either removed/split or explicitly added before release.
- When technical.md exists, compare the diff to the `TD-n` records mapped into this increment's
  result card. Contradiction or an unmapped changed public boundary is drift; unrelated technical
  records are not mandatory implementation scope.
- Empty sections are written as `- none` — an absent section reads as "not checked".
- Self-check: every DDL item has a rollback entry; every secret is name-only; every third-party
  item has an owner.

## Environment-Change Safety

- Backup before any DDL touching existing data; record the backup path in the ledger.
- Prefer expand → migrate → contract over in-place destructive DDL; a destructive or lossy
  migration is `[ONE-WAY]` and needs explicit human confirmation even on the test environment
  when data is shared.
- Apply to test first, always; prod applies only what test proved, in the same order.
- Secrets are provisioned by the human or a secret manager — the agent handles names and wiring,
  never values in artifacts or logs.

## Online Regression

- The prod-safe subset is Tier-1 specs explicitly tagged `@prod-safe`: read-only flows, no data
  mutation, no test-account pollution beyond documented sandboxes. Untagged specs never run
  against production.
- Evidence triangle applies read-only: interface assertion + correlation-ID log lookup + state
  query. Watch the runbook's signals (error rates, key logs) for its stated window before
  declaring the stage ok.

## Stage Ledger

Each stage appends `{"type":"release","stage":"<stage>","result":"ok|failed|blocked",
...evidence fields}`. Stage vocabulary:

- `ship`: `manifest` → `env-test` → `deploy-test` → `regression-test` → `acceptance-test` → merge
- `deploy`: `preflight` → `env-prod` → `deploy-prod` → `regression-prod` → `watch`

Resume = skip stages whose latest entry is `ok` and whose inputs are unchanged since (manifest
re-collects when the diff moved; preflight always re-runs — it is a check, not work).
