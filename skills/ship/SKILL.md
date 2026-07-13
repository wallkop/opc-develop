---
name: ship
description: "Use after a build increment reaches a fresh approved-testcase real-service core journey to deploy it to test, rerun the same approved cases, obtain human acceptance, and merge. Requires the mandatory demo/PRD/testcase chain, receipt, and two-review chain."
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
   generated receipt, approved demo/PRD/testcase artifacts, reality/final reviews, resolved rework,
   and test-env runbook. Technical artifacts remain conditional.
2. **manifest**: collect `release-manifest.md` from the actual diff per `release-ops.md`. Cross-check
   optional technical records when present. Every DDL item has rollback; secret values never enter
   artifacts; provider/dashboard changes have an owner.
3. **env-test + deploy-test**: apply manifest items to test in order, back up shared data before DDL,
   and deploy per runbook.
4. **regression-test**: execute the same approved Core-Case and regression suite through the project
   testcase runner against test. Attach runner-generated evidence with build/origin/session/object/
   trace/state facts. Raw Playwright or caller-authored labels are invalid. Do not rerun a real
   provider to diagnose a harness failure.
5. **acceptance-test**: present the real test entry, result-card scope, manifest, safety checks, and
   highest completion level. Route the verdict:
   - approved: run `opc_increment.py accept --actor <role>` and continue;
   - implementation defect: re-enter the affected `build` slice, invalidate stale receipt commands,
     fix, and resume at test deploy;
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

Test deployment evidence, human-accepted fresh receipt, release manifest, and merged branch. Next:
`deploy` when the human chooses production release.
