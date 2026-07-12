---
name: ship
description: "Use after build's local verification passes to put the feature in front of the human on the test environment: collect and gate the release manifest (DDL, env vars, config, services) against technical.md, apply environment changes and deploy to test, run automated regression there, then run the test-acceptance touchpoint and route its verdict — code defects re-enter build, artifact defects revise upstream, approval merges the branch to the trunk. Production is deploy's job, not ship's."
license: MIT
---

# ship

Test environment only. Ship ends with a human verdict on a really-deployed feature and, on
approval, code merged to the project trunk — the precondition `deploy` will check.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/release-ops.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/feedback-routing.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Stages

Resume after the last `release` ledger entry with `result: ok`; `manifest` re-collects when the
diff moved.

1. **Precheck**: run
   `python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/check_gate_chain.py" docs/features/<slug>` —
   the whole chain from requirement to e2e must be intact (declared `--skip`s are surfaced to
   the human). Acceptance sheet exists, rework entries resolved (each open `RW-n` explicitly
   referenced by a resolving entry), project test-env runbooks read.
2. **manifest**: collect the release manifest per `release-ops.md` from the actual diff (build's
   phase-C ledger entries seed the DDL/config sections), cross-checked against technical.md.
   Drift routes `revise` before release. Write `release-manifest.md`; self-check; ledger.
3. **env-test + deploy-test**: apply manifest items to the test environment in order (backup
   before DDL per safety rules), deploy per runbook.
4. **regression-test**: run the Tier-1 suite against the test environment; evidence triangles
   with test-env labels; smoke the documented signals. Failures here are triaged before any
   human is summoned.
5. **acceptance-test (touchpoint)**: write `reports/acceptance.md` as a faithful plain-language
   acceptance-sheet + manifest summary with source SHAs, render/lint `reports/acceptance.html` per
   `formats/report-style.md`, then hand the human the test-environment
   entry point, the acceptance sheet, and the manifest. Route the verdict:
   - **Approved** → next stage.
   - **Code defect** → re-enter **`build`** (fix mode) with the rejection notes; after build
     refreshes its evidence, ship resumes at stage 3.
   - **Artifact defect** → `revise` at `prd`/`architect` + stale cascade; the flow replays
     forward and ship resumes at stage 2 (manifest re-collects).
   - **New need / taste change** → `change` entry → `brainstorm` for the next increment; the
     human decides whether this release proceeds without it or parks.
6. **merge**: merge the feature branch into the project trunk (`develop` or per AGENTS.md flow),
   push, clean worktrees per `branch-worktree.md`. Record the merge commit in the ledger —
   `deploy`'s preflight requires it. Then **fold the feature's deltas into the living spec**
   (`formats/living-spec-format.md`): ACs into the domain registry, state machines and
   permission tables rebuilt to current truth, PD/TD references indexed. An AC conflict at merge
   time is a `revise`, not an overwrite.

## Fail-open

Missing test environment: run the acceptance touchpoint on the best available surface with its
label cap stated, and say so on the sheet. Missing deploy runbook for test: record the gap,
deliver the manifest + checklist, stop at handoff. Shared-data DDL keeps its confirmation rule
even on test.

## Output

`release-manifest.md`, staged `release` ledger entries, human test-acceptance verdict, feature
merged to trunk on approval. Next: `deploy` when you choose to release to production.
