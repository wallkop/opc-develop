---
name: lite-develop
description: "Use for small or medium-low-risk product tweaks, bug fixes, UI copy/layout changes, and quick implementation iterations on the current branch. Classifies work as direct current-branch edit, isolated worktree from current branch, or Full flow; supports targeted checks, quick user acceptance, and optional merge/discard of the lite worktree back into the current branch without creating Full demo/PRD/technical/spec/plan/review/testcase artifacts."
license: MIT
---

# lite-develop

受控 vibe-coding：优先服务“当前分支上的快速开发”。简单需求直接在当前分支改；较复杂、需要隔离、需要多轮打磨或并行试验时，从当前分支 `HEAD` 拉 lite worktree；用户满意后可合回当前分支并清理 worktree，不满意可丢弃。

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/worktree-isolation-contract.md`

Also read from the target project before changing code:

- root `AGENTS.md`
- any scoped `AGENTS.md` that applies to changed paths
- `docs/technical/runbooks/git-flow.md`
- `docs/technical/runbooks/local-dev.md`
- `docs/technical/standards/testing.md`
- `docs/technical/harness/documentation-rules.md`

If a required project rule document is missing or incomplete, stop and report the gap instead of guessing.

## Inputs

Natural-language requirement, optional existing lite worktree path, optional quick acceptance feedback, current project repository, current branch, and applicable project commands.

## Hard Gates

Do not create demo, PRD, technical, spec, plan, review, testcase, release, feature branch, or Full closeout artifacts during this skill unless the project `AGENTS.md` explicitly requires a minimal artifact. Do not bypass project military rules: `AGENTS.md`, runbooks, testing standards, and documentation rules override Lite simplification.

Lite is a current-branch workflow. The default expected branch is `develop`. If the current branch is not `develop`, ask the user to confirm before writing code or docs. Do not auto-checkout `develop`, do not create `feature/*`, and do not use a worktree as the default response. If current branch is `main`, `master`, or protected by project rules, stop unless the user and project rules explicitly allow the requested change on that branch.

Do not stash, commit, discard, copy, or merge dirty changes without explicit user instruction or project-rule authority. Do not push or release.

Stop and recommend Full opc-develop flow when the request needs product brainstorm, high-fidelity demo alignment, full PRD, architecture design, data migration, security, permissions, payment, privacy, cross-service work, cross-team work, multiple formal workstreams, formal spec/plan/review, or when project rules forbid simplification.

## Classification

Choose one mode before editing and report it in the first status update.

### Direct current-branch mode

Use when all are true:

- Change is small, low risk, and easy to validate with targeted checks.
- Expected diff is narrow and does not need isolation.
- Current branch is the right product context.
- Dirty worktree state is either clean or clearly part of the same requested change.
- No parallel experimentation is needed.

Typical examples: copy changes, style/layout tweaks, single-component bugfixes, small test stabilization, local-only behavior fixes.

### Isolated lite worktree mode

Use when any are true:

- Change needs several rounds of UI/product polish.
- The user may want to discard the whole attempt.
- Current branch should stay runnable while experimenting.
- Diff may touch multiple modules but is still Lite, not Full.
- Service startup, screenshot verification, or parallel option testing makes isolation useful.
- Current branch has unrelated dirty changes that must not be mixed into the Lite attempt.

Create the lite worktree from the current branch `HEAD`, not from `develop`.

Default path:

```text
../<repo-name>-worktrees/lite-<slug>
```

Default branch:

```text
lite/<slug>
```

Default command:

```bash
git worktree add -b lite/<slug> ../<repo-name>-worktrees/lite-<slug> HEAD
```

If current uncommitted changes are required context, do not create a worktree unless the user explicitly confirms how to carry them over. Prefer direct mode for dirty-context edits.

### Full flow escalation

Escalate to Full when Lite classification is false or project rules require formal artifacts/gates.

## Process

1. Resolve the project root with `git rev-parse --show-toplevel`.
2. Inspect `git branch --show-current`, `git status --short`, `git rev-parse --abbrev-ref HEAD`, and `git worktree list --porcelain`.
3. Read the required shared and project references.
4. Apply `branch-stage-contract.md`: default to direct current-branch edits on `develop`; require confirmation before writing on any non-`develop` branch.
5. Classify the request as `direct`, `isolated-worktree`, or `full`.
6. For direct mode, implement on the current branch. Keep the change narrow and avoid unrelated cleanup.
7. For isolated mode:
   - create or locate the existing `lite/<slug>` worktree from the current branch `HEAD`
   - record parent branch and parent commit
   - implement only inside the lite worktree
   - keep changes independent from unrelated dirty state in the parent checkout
8. Run targeted checks based on the actual diff and project rules:
   - UI path changes: run documented local start/status commands, capture screenshots or Computer Use evidence when required.
   - API endpoint changes: add or update required API tests, scenario mapping, and strict audit inputs required by the project.
   - Backend logic changes: run focused unit or integration tests plus any required aggregate checks.
   - Copy/style-only changes: run the lightest documented build, type, or smoke check that can catch regressions.
9. If a documented service start command was run, follow the project runbook for stopping or preserving services.
10. Present changed behavior, files changed summary, commands run, evidence paths, residual risks, and exact items needing user quick acceptance.

## Iteration Rules

When the user asks for more polish after quick acceptance, keep the same mode and workspace unless classification changes.

- Direct mode: continue on the current branch.
- Isolated mode: continue in the same lite worktree and branch.

Treat feedback as authoritative product input, make the smallest effective adjustment, rerun targeted checks, and present a new acceptance summary.

If feedback changes product scope or exposes missing architecture decisions, stop and recommend Full flow instead of expanding Lite silently.

## Settle Rules

When the user confirms the Lite result is satisfactory:

### Direct mode settle

Do not auto-commit, merge, or create docs. Report:

- current branch
- changed files
- targeted checks and evidence
- remaining dirty state
- whether project rules require a later commit, PR, or Full closeout

### Isolated worktree settle

Ask for explicit user confirmation before merge or discard.

If user chooses merge:

1. Confirm parent branch and parent checkout are still the intended target.
2. Confirm no unrelated dirty changes would be overwritten.
3. Run required targeted checks in the lite worktree.
4. Commit or keep uncommitted according to project runbook and user instruction.
5. Merge or cherry-pick the lite worktree changes back into the original current branch, following project git-flow rules.
6. Stop on conflicts, stale parent branch, or unrelated dirty changes.
7. Remove the lite worktree only after successful merge/cherry-pick and user-approved cleanup.

If user chooses discard:

1. Confirm explicit discard intent.
2. Remove the lite worktree and delete the `lite/<slug>` branch only when safe.
3. Report discarded branch, worktree path, and any preserved evidence.

Never delete a worktree with unmerged useful work unless the user explicitly chose discard.

## Output Contract

Return language-adaptive output with:

- selected mode: `direct`, `isolated-worktree`, or `full`
- current branch and, when applicable, lite branch/worktree path
- implemented behavior
- files changed summary
- targeted checks and evidence
- blockers or residual risk
- next user action: quick acceptance, more feedback, merge lite worktree, discard lite worktree, or escalate to Full

## Self-Check

Confirm the selected Lite mode matches risk, project military rules were read, `branch-stage-contract.md` was followed, no `feature/*` branch or Full artifacts were created, targeted checks match the diff, no branch/worktree action happened without authority, no dirty unrelated work was hidden, and the user has enough evidence to accept, iterate, merge, discard, or escalate.
