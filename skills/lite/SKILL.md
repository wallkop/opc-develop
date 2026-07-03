---
name: lite
description: "Use for small or low-risk changes: bug fixes, copy/layout tweaks, config changes, minor behavior adjustments. Works on the current branch (or a lite worktree) with targeted tests and a quick before/after acceptance check — no demo, PRD, technical, or contract artifacts. Escalates to the full flow when risk categories or scope say so. Works in bare repositories."
license: MIT
---

# lite

The 80% path. Zero ceremony that doesn't pay for itself, same honesty rules.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- On escalation or worktree questions: `packs/risk-readiness.md`, `packs/branch-worktree.md`
- On debugging: the failure discipline section of `packs/tdd-implement.md`

## Process

1. **Classify (fast)**: read the request and the touched surface.
   - Escalation triggers → recommend the full flow (human decides): any risk category from
     `risk-readiness.md`, schema/public-API changes, permission changes, or
     "this keeps growing as I look at it".
   - **Middle tier — structured lite**: multi-module scope or a change that wants TDD subagents
     and a review gate but no demo/PRD ceremony → borrow exactly `build`'s phase B machinery
     (load `packs/tdd-implement.md` + `rubrics/implementation.md`): a minimal boundary note
     instead of a contract tree, implementer subagent(s) with RED/GREEN evidence, one merged
     review gate, targeted regression. No feature directory, no other artifacts.
   - Otherwise pick: direct edit on the current branch (default) or a lite worktree (when tests/
     services need isolation).
2. Read project AGENTS.md and applicable rules if present; proceed without them if absent
   (bare-repo compatible — missing harness docs are a note, not a blocker).
3. Implement with tests where the change has behavior: failing test first when fixing a bug
   (capture RED/GREEN per `packs/evidence.md` when you do), targeted test run after.
4. Verify by exercising the change for real — run the affected flow, capture before/after
   evidence (screenshot, output diff, log line) with an honest label.
5. Quick acceptance: show the human the evidence. Their feedback routes tune (iterate) /
   revise (widen scope → reclassify, possibly escalate) / park (discard cleanly).
6. If a debugging session resolved a non-obvious root cause, append it to
   `docs/opc/error-ledger.jsonl` via `opc_ledger.py` — lite work is where repeated small mistakes
   hide.
7. Worktree cleanup per `branch-worktree.md` when one was used.

## Fail-open

Everything here fails open except destructive actions. On the trunk with no branch rules: small
tested changes may proceed; anything touching data, schema, or permissions gets a branch first.

## Output

The change, its evidence, optional error-ledger records. No feature artifacts.
