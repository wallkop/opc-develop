---
name: lite
description: "Default route for one bounded change implemented through existing architecture, including localized behavior, state, billing, permission, provider, API, persistence, UI, bug, copy, style, docs, or config changes. Upgrade to build only for an explicit structural trigger such as a net-new complete capability, shared-core refactor, breaking/destructive evolution, broad regression surface, or coordinated rollout. Uses focused checks plus matching risk protection, with no mandatory feature documents or subagents. Works in bare repositories."
license: MIT
---

# lite

Finish one bounded result without workflow artifacts. Keep evidence honest and proportional.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- On matching risk or worktree questions: `packs/risk-readiness.md`, `packs/branch-worktree.md`
- On debugging: the failure-discipline section of `packs/tdd-implement.md`

## Process

1. Read applicable project rules and inspect the touched code/runtime. Default to Lite. Upgrade to
   `build` only when inspection proves one of the exact triggers in `core-contract.md`; name the
   trigger before rerouting. Behavior change, release intent, money, permissions, concurrency,
   providers, APIs, or database work alone do not qualify. If product intent is unclear, clarify it
   directly; use `brainstorm`/`demo` only when the human wants formal product definition, then
   reclassify. Do not use technical ceremony to guess product truth.
2. Choose the current branch by default or a lite worktree when isolation is genuinely useful.
   Do not create requirement, demo, PRD, technical, contract, ledger, or report artifacts.
3. Implement directly through existing project patterns. Write the narrowest useful regression;
   for a bug, observe the failure before the fix when practical. A clear user-requested behavior
   may define or update the focused regression without a separate testcase artifact. Run targeted
   tests during iteration, not the full suite after every edit.
4. Apply proportional verification. Pure copy, static style, docs, comments, formatting, and
   non-runtime configuration do not run testcase/E2E by default. Use relevant static, type,
   component, snapshot, or accessibility checks plus a lightweight real-entry visual/DOM check when
   UI is touched. Runtime behavior gets the smallest real-entry or black-box check that proves the
   result; use the project testcase runner when a matching case exists. Do not manufacture a full
   feature chain merely because behavior changed.
5. Add only the matching safety check: migration snapshot/rollback, permission denial path,
   money calculation/idempotency/rollback, concurrency/idempotency, or provider replay. A real
   provider call, if needed, happens once after offline checks are stable. These checks do not
   change the route.
6. When release is requested, run the project's complete deployment preflight/gate, then enter
   `ship`/`deploy` as applicable. Release intent does not upgrade Lite to Build. Preserve the
   project runbook, rollback, production-confirmation, and destructive-action rules.
7. Hand the human the diff, commands/exits, before/after evidence, and authenticity label. Say
   plainly when the result stops below a real-service check. Route only a discovered exact Build
   trigger to `build`.
8. Record a non-obvious resolved root cause in the project error ledger when one exists; clean a
   worktree when used.

## Boundaries

- Use no implementation/reviewer subagents; dispatch overhead is not justified for this tier.
- Preserve unrelated user changes. Destructive, production, permission/security, and irreversible
  schema/data actions still require explicit approval.
- Do not claim a behavior change complete for UI work when only an API or unit test was exercised.
- Non-semantic UI work needs proportional visual/DOM evidence, not an E2E journey.
- Do not silently broaden ambiguous product intent. Clarify the bounded result; use the
  product-definition skills only when the intent or experience genuinely needs definition.
- Adding a backward-compatible field, index, endpoint, optional shared-code path, or small isolated
  table may stay Lite. Breaking migration, shared default redefinition, or broad consumer
  regression is Build.

## Output

The scoped change, focused regression where valuable, matching risk checks, one proportional
real-entry check, and concise evidence.
