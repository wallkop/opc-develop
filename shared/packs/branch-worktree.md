# Branch & Worktree Rules

## Trunk Detection

Detect the project's trunk instead of assuming one: `git symbolic-ref refs/remotes/origin/HEAD`
(fallback: whichever of `main`/`master`/`develop` exists, in that order), unless AGENTS.md names
one. Project AGENTS.md always wins over this pack.

## Feature Branches

- Full-flow features live on `feature/<numbered-slug>` (e.g. `feature/7-export`), created by
  `brainstorm` when requirement.md is first written — not before, not later.
- **Slug collision (multi-person)**: `next_feature_slug.py` numbers from the local checkout, so
  two people starting features concurrently can draw the same number. Push the feature branch
  right after creating it to reserve the slug; on a collision at push time, the later branch
  renumbers (`git branch -m`, rename the feature dir, one commit) — artifact content never
  changes, only the slug.
- Never write feature artifacts directly on the trunk.
- Lite work may stay on the current branch when the change is small and low-risk; a lite worktree
  from the current branch is the isolation option when tests/services need separation.
- On a mismatched branch or detached HEAD: state what you found and ask, don't guess.

## Worktrees

- Parallel implementers ⇒ one worktree each, branched from the feature branch
  (`git worktree add ../<repo>-wt-<contract-id> <feature-branch>`). Serial dispatch needs none.
- Never nest worktrees. Never create a worktree from inside another worktree.
- Cleanup: merge or discard promptly after the contract completes; `git worktree remove` after
  merge; a worktree left behind is a recorded gap.

## Destructive Actions (fail closed)

Require explicit human confirmation, every time, regardless of prior approvals:
deleting branches/worktrees with unmerged work, `push --force`, history rewrites on shared
branches, dropping data, publishing/releasing to shared or external surfaces.
Everything else fails open with a recorded gap.

## Dirty State

Uncommitted changes unrelated to the current work: stop and ask. Related changes: proceed, but
commit scope stays limited to files the current work owns.
