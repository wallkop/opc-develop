---
name: ship
description: "Use when a verified Lite or Build increment should deploy to test, be accepted, and merge. Build keeps its approved demo/PRD/testcase, receipt, and review gates. Lite instead uses focused regression evidence, matching risk checks, and the project's complete predeploy gate without manufacturing feature artifacts. Release intent alone never upgrades Lite to Build."
license: MIT
---

# ship

Deploy one verified increment to the test environment, obtain the human verdict, then merge.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/release-ops.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/feedback-routing.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Stages

When the project has a release ledger, resume after the latest fresh `release` entry with
`result: ok`. Refresh evidence and recollect any applicable manifest whenever the content tree
changes.

1. **Precheck and classify evidence**:
   - **Build**: run `opc_increment.py check --require real-service-core-journey`,
     `check_gate_chain.py docs/features/<slug>`, and
     `opc_ledger.py audit --require-increment-complete`. Require the plan, receipt, approved
     demo/PRD/testcase artifacts, reviews, resolved rework, and test-env runbook.
   - **Lite**: confirm no exact Build trigger applies; run focused regressions, matching risk
     checks, the smallest relevant real-entry check, and the project's complete predeploy/release
     gate. Record commit/diff, commands, exits, and evidence through the project's native mechanism.
     Do not create Build feature artifacts, approvals, reviews, or receipts solely for release.
   Both routes require the real test-env runbook. Release intent does not change the route.
2. **manifest**: inspect the actual diff per `release-ops.md`. Build writes its feature release
   manifest. Lite uses the project's native release artifact or a concise release ledger/handoff
   record only when operational changes exist; do not create a feature directory for an ordinary
   code-only Lite release. Every DDL item has rollback; secret values never enter artifacts;
   provider/dashboard changes have an owner.
3. **env-test + deploy-test**: apply manifest items to test in order, back up shared data before DDL,
   and deploy per runbook.
4. **regression-test**:
   - **Build**: execute the same approved Core-Case and regression suite through the project
     testcase runner against test and attach runner-generated evidence.
   - **Lite**: rerun the focused regression and matching real-entry check against test; use a
     matching project testcase when one exists, without requiring a new testcase catalog.
   In both routes attach honest build/origin/session/object/trace/state facts where available. Do
   not rerun a real provider to diagnose a harness failure.
5. **acceptance-test**: present the real test entry, scoped change or Build result card, applicable
   manifest, safety checks, and highest supported completion claim. Route the verdict:
   - approved: Build runs `opc_increment.py accept --actor <role>`; Lite records the human verdict
     through the project release evidence/ledger, then continue;
   - implementation defect: re-enter the originating Lite change or Build slice, invalidate stale
     evidence, fix, and resume at test deploy;
   - wrong journey/object/plan: reject the candidate, revise the result card or earliest explicit
     artifact, and invalidate downstream evidence;
   - taste change: create a new increment; the human decides whether this one still ships.
6. **merge**: merge to the project trunk, push, and clean worktrees. Fold into a living spec only
   when the project uses one and the increment changes durable behavior.

## Fail-open / fail-closed

Missing test environment caps acceptance at the best real local level and stops before merge unless
the human explicitly accepts that release policy. Missing runbooks create a handoff, not improvised
deployment. Shared-data DDL and destructive actions remain approval-gated.

## Output

Test deployment evidence, human verdict, applicable release record, and merged branch. Build also
returns its human-accepted fresh receipt. Next: `deploy` when the human chooses production release.
