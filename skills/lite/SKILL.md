---
name: lite
description: "Use for a single small change credibly finishable within 60 minutes: bug fixes, copy/layout tweaks, config changes, and minor behavior adjustments. Works on the current branch (or a lite worktree) with targeted tests and one real-entry before/after check, no feature documents or subagents. Risk adds only the matching safety check; scope that needs multiple runnable slices routes to build, and work above 4 hours must be split. Works in bare repositories."
license: MIT
---

# lite

Finish one small result without workflow artifacts. Keep evidence honest and proportional.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- On matching risk or worktree questions: `packs/risk-readiness.md`, `packs/branch-worktree.md`
- On debugging: the failure-discipline section of `packs/tdd-implement.md`

## Process

1. Read applicable project rules and inspect the touched code/runtime. Confirm one result and a
   credible <=60-minute budget. Multiple user-visible slices or >60 minutes routes to `build`;
   >240 minutes routes to a split. Do not escalate merely because a risk category exists.
2. Choose the current branch by default or a lite worktree when isolation is genuinely useful.
   Do not create requirement, demo, PRD, technical, contract, ledger, or report artifacts.
3. Implement directly. For behavior, write the narrowest useful regression; for a bug, observe the
   failure before the fix when practical. Run targeted tests, not the full suite after every edit.
4. Exercise the real entry once after targeted checks. For UI, the browser performs the changed
   action; for API/CLI, use the real external interface. A fixture may prepare state but may not
   manufacture the success being asserted.
5. Add only the matching safety check: migration snapshot/rollback, permission denial path,
   concurrency/idempotency, or provider replay. A real provider call, if needed, happens once after
   offline checks are stable.
6. Hand the human the diff, commands/exits, before/after evidence, and authenticity label. Say
   plainly when the result stops below a real-service check. Route widened intent to `build`.
7. Record a non-obvious resolved root cause in the project error ledger when one exists; clean a
   worktree when used.

## Boundaries

- Use no implementation/reviewer subagents; dispatch overhead is not justified for this tier.
- Preserve unrelated user changes. Destructive, production, permission/security, and irreversible
  schema/data actions still require explicit approval.
- Do not claim complete for UI work when only an API or unit test was exercised.

## Output

The scoped change, focused regression where valuable, one real-entry check, and concise evidence.
