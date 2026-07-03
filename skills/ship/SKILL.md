---
name: ship
description: "Use after verify's acceptance touchpoint passes to release and close out: runs the project's release gates and build, executes deploy per project runbooks, performs post-release smoke checks with evidence, confirms rollback readiness, then finishes the branch safely (merge, PR handoff, or keep) and cleans up worktrees."
license: MIT
---

# ship

Release with evidence, leave the workspace clean.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`

## Process

1. Precheck: verify's gate fresh, acceptance verdict recorded, no unresolved `rework` entries in
   the ledger (resolution rule per `formats/ledger-format.md` conventions). Read the project's release runbooks (deploy/rollback docs, CI config) — these
   define the gates; this skill does not invent a release process.
2. Run release gates: full test suite, build, lint/type checks, any project CI gates runnable
   locally. Record commands, exit codes, and labels.
3. **Rollback readiness before deploy**: confirm the documented rollback path exists and its
   preconditions hold (previous version identifiable, down-migrations or compatibility noted).
   No rollback path is a `[ONE-WAY]` situation — surface it to the human before deploying.
4. Deploy per the project runbook. Deployment to shared/production surfaces is a destructive-class
   action: confirm with the human unless AGENTS.md grants standing approval for this target.
5. Post-release: run the documented smoke checks against the released surface; record evidence
   with `external provider passed` / real-surface labels only when actually exercised there.
6. Finish the branch per `branch-worktree.md`: merge or PR per project flow, remove worktrees,
   delete merged branches when project rules say so. Detached-HEAD or app-managed checkouts get a
   handoff note instead of guessed cleanup.
7. Final ledger entries: release evidence, residual gaps carried forward. Suggest `retro` if one
   hasn't run recently.

## Fail-open

Missing deploy/rollback runbooks: do not improvise a production deploy. Record the gap, hand the
human a concrete release checklist of what was verified locally, and stop at the handoff — this
is the one phase where the destructive-action rule dominates fail-open.

## Output

Released feature (or a clean handoff), release evidence in the ledger, tidy branch state.
