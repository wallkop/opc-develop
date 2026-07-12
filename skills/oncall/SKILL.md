---
name: oncall
description: "Use when something is wrong in production (or on the test environment): triages severity, investigates through the observe verbs (correlation-ID logs, read-only DB queries, traces, recent releases), produces a diagnostic report with root cause and blast radius, executes the chosen path — rollback, expedited hotfix through build/ship/deploy, or mitigation — and always leaves an error-ledger record plus a long-term fix proposal."
license: MIT
---

# oncall

Production diagnosis with the same evidence discipline as development: no cause claimed without
the log chain and state that prove it, no fix without a covering test.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/harness-verbs.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`
- On hotfix: `${CLAUDE_PLUGIN_ROOT}/shared/packs/release-ops.md`

## Process

1. **Triage**: capture the symptom (alert, user report, anomaly), when it started, who is
   affected. Classify severity: data loss / money / security ⇒ propose rollback or kill-switch
   FIRST, investigate second; degraded-but-safe ⇒ investigate first.
2. **Investigate through observe**: first establish expected behavior from the living spec
   (`docs/opc/specs/`, when it exists) — regression vs works-as-specified is the first fork.
   Reconstruct the failing action's causal chain by correlation ID; query state read-only; check
   traces; diff behavior against the last known-good release — recent `release` ledger entries,
   merge commits, and release manifests are the change candidates. Reproduce on local/test with the matching seed when possible.
3. **Diagnostic report** — `docs/opc/incidents/<date>-<slug>.md`: timeline, blast radius, root
   cause with the evidence chain (log lines, queries, commits), contributing factors, and the
   options considered. No root cause ⇒ say so explicitly and record the leading hypotheses with
   what would confirm each.
   Render and lint the same-basename `.html`. Lead with conclusion, user impact, evidence and next
   action; explain specialist terms beside their first occurrence.
4. **Decide the path** (five-piece set to the human when contested):
   - **rollback** — hand to `deploy`'s rollback path; fastest when the trigger is a recent release;
   - **hotfix (expedited path)** — minimal fix on a hotfix branch per project flow, RED/GREEN
     evidence for the defect, targeted regression only, then `ship` (test env, compressed) →
     `deploy` with the incident referenced. Expedited ≠ unverified: the RED test and prod-safe
     regression are not skippable;
   - **mitigation** — config/flag/scale change with its own evidence and a revert note.
5. **Always, after stabilization**:
   - append the root cause to `docs/opc/error-ledger.jsonl` (tag it — incidents feed `retro`'s
     recurrence detection like any other failure);
   - for P0/P1, irreversible-risk, false-green, or recurring incidents, link a project benchmark
     case proving GREEN → RED → GREEN, or record a human-approved waiver;
   - write the long-term fix proposal: what structural change prevents the class, sized as a
     `lite` task or routed to `brainstorm`/`architect` as a feature; link it in the report;
   - record any harness gap the investigation exposed (missing correlation ID, missing dump,
     missing prod-safe spec) — these become `harness` backlog.

## Fail-open / fail-closed

Investigation is read-only and fails open (missing observability = recorded gap + stated
confidence caps). Interventions follow `deploy`'s rules: production mutations, restarts, and
rollbacks all require explicit human confirmation.

## Output

Diagnostic report, stabilized system via the chosen path, error-ledger record, long-term
proposal, harness gaps.
