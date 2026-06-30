---
name: finish-branch
description: "Use when implementation work is complete and the current Git branch, linked worktree, or Codex App detached HEAD needs a safe finish path: local merge, push or PR handoff, keep branch, discard changes, remove worktree, or report a detached-head handoff. Follows project AGENTS.md, git-flow runbook, worktree isolation, and evidence-before-claim rules."
license: MIT
---

# finish-branch

完成分支或 worktree 收尾：检查当前 Git 状态，按项目军规选择 local merge、push/PR、keep branch、discard、worktree 清理或 detached HEAD 交接。

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/runtime-evidence-contract.md`
- `../../shared/references/evidence-before-claim.md`
- `../../shared/references/worktree-isolation-contract.md`

Also read project `AGENTS.md` and git-flow/runbook documents before merging, pushing, deleting branches, or removing worktrees.

## Inputs

Current repository or worktree, project `AGENTS.md`, git-flow runbook, user-requested finish mode when provided, validation evidence, and current diff.

## Hard Gates

Do not merge, push, delete, discard, or remove a worktree without checking branch, HEAD state, dirty files, linked worktrees, project rules, and `branch-stage-contract.md`. Do not merge into `develop` or `main` unless project runbooks allow the specific path, the user requested/confirmed it, and required gates have fresh evidence. Do not discard uncommitted work without explicit user instruction.

## Finish Modes

- `local-merge`: merge the completed feature branch into the project-approved parent branch.
- `push-pr`: push branch and provide PR handoff when project rules allow remote PR flow.
- `keep-branch`: leave branch/worktree intact and report status.
- `discard`: discard work only after explicit user instruction.
- `detached-head-handoff`: preserve diff and report exact recovery commands when current state is detached HEAD.

## Process

1. Inspect `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git rev-parse --abbrev-ref HEAD`, and `git worktree list --porcelain`.
2. Detect detached HEAD, linked worktree, nested worktree risk, dirty unrelated files, untracked files, and upstream divergence.
3. Read project `AGENTS.md` and git-flow runbook to determine allowed finish modes and required gates.
4. Confirm validation evidence is fresh enough for the requested finish mode. If not, stop and report missing gates.
5. Execute only the requested or project-obvious finish mode:
   - local merge: commit current branch if needed, switch to allowed parent, merge, and record commit ids.
   - push/PR: push only when project rules allow; report branch, remote, and PR command/link.
   - keep branch: report branch, worktree, dirty state, and next command.
   - discard: require explicit instruction, then clean only the requested changes.
   - detached HEAD handoff: create a rescue branch or provide exact commands, according to user instruction and project rules.
6. Remove a linked worktree only after its branch is safely merged, pushed, kept intentionally, or discarded by explicit instruction.
7. Update `progress.md` when working inside a opc-develop feature directory.

## Output Contract

Return language-adaptive output with:

- detected repository/worktree state
- selected finish mode
- commands run and evidence
- resulting branch, commit, merge, push, or handoff state
- worktree cleanup status
- blockers or remaining user decision

## Self-Check

Confirm no destructive action was taken without explicit permission or project-rule authority, no stale validation was treated as passed, no linked worktree was removed before safe handoff, and detached HEAD was preserved or handed off safely.
