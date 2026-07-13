---
name: ship
description: "Use after a build increment reaches a fresh real-service core journey to deploy it to the test environment, run the same core journey and targeted regression there, obtain human acceptance, and merge the branch. Supports standard and release-bound quick increments; requires the generated receipt and two-review chain. Optional PRD/technical artifacts are checked only when present. Production remains deploy's job."
license: MIT
---

# ship

Deploy one accepted increment to the test environment, obtain the human verdict, then merge.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/release-ops.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/feedback-routing.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Stages

Resume after the latest fresh `release` entry with `result: ok`; recollect the manifest whenever the
content tree changes.

1. **Precheck**: run `opc_increment.py check --require real-service-core-journey`,
   `check_gate_chain.py docs/features/<slug>`, and
   `opc_ledger.py audit --require-increment-complete`. Require the build plan,
   generated receipt, reality/final reviews, resolved rework, and test-env runbook. When explicit
   PRD/technical artifacts exist, verify their approvals/freshness separately; do not require absent
   layers.
2. **manifest**: collect `release-manifest.md` from the actual diff per `release-ops.md`. Cross-check
   optional technical records when present. Every DDL item has rollback; secret values never enter
   artifacts; provider/dashboard changes have an owner.
3. **env-test + deploy-test**: apply manifest items to test in order, back up shared data before DDL,
   and deploy per runbook.
4. **regression-test**: run the same core journey against test plus the focused regressions for this
   increment. For UI, the browser performs the key action. Record test build ID, origin/session,
   object IDs, trace, state assertion, and honest label. Do not rerun a real provider to diagnose a
   harness failure.
5. **acceptance-test**: present the real test entry, result-card scope, manifest, safety checks, and
   highest completion level. Route the verdict:
   - approved: run `opc_increment.py accept --actor <role>` and continue;
   - implementation defect: re-enter the affected `build` slice, invalidate stale receipt commands,
     fix, and resume at test deploy;
   - wrong journey/object/plan: reject the candidate, revise the result card or earliest explicit
     artifact, invalidate downstream evidence, and re-evaluate budget;
   - taste change: create a new increment; the human decides whether this one still ships.
6. **merge**: merge to the project trunk, push, and clean worktrees. Fold into a living spec only
   when the project uses one and the increment changes durable behavior; PRD is not mandatory.

## Fail-open / fail-closed

Missing test environment caps acceptance at the best real local level and stops before merge unless
the human explicitly accepts that release policy. Missing runbooks create a handoff, not improvised
deployment. Shared-data DDL and destructive actions remain approval-gated.

## Output

Test deployment evidence, human-accepted fresh receipt, release manifest, and merged branch. Next:
`deploy` when the human chooses production release.
