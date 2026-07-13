---
name: lite
description: "Use for one localized change that does not create or alter product E2E semantics: bug fixes covered by an existing oracle, copy/static-style tweaks, docs, comments, formatting, and non-runtime config changes. Routes by semantics and risk, never duration. Uses proportional targeted checks and a lightweight real-entry check when relevant, with no feature documents or subagents. Works in bare repositories."
license: MIT
---

# lite

Finish one small result without workflow artifacts. Keep evidence honest and proportional.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- On matching risk or worktree questions: `packs/risk-readiness.md`, `packs/branch-worktree.md`
- On debugging: the failure-discipline section of `packs/tdd-implement.md`

## Process

1. Read applicable project rules and inspect the touched code/runtime. Classify the change by
   semantics, never by predicted duration. A change that creates or changes E2E product semantics
   routes to `demo -> prd -> testcase -> build`; lite may only reuse an already approved oracle
   unchanged.
2. Choose the current branch by default or a lite worktree when isolation is genuinely useful.
   Do not create requirement, demo, PRD, technical, contract, ledger, or report artifacts.
3. Implement directly. For behavior covered by an existing oracle, write the narrowest useful
   regression; for a bug, observe the failure before the fix when practical. Run targeted tests,
   not the full suite after every edit.
4. Apply the E2E applicability gate. Pure copy, static style, docs, comments, formatting, and
   configuration with no runtime behavior change do not run testcase/E2E by default. Use the
   relevant static, type, component, snapshot, or accessibility check plus a lightweight real-entry
   visual/DOM before-and-after check when UI is touched. This check must not execute a full journey.
   If runtime behavior changes under inspection, reclassify the work and use the approved testcase
   runner; never invoke raw Playwright as an acceptance command.
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
- Do not claim a behavior change complete for UI work when only an API or unit test was exercised.
- Non-semantic UI work needs proportional visual/DOM evidence, not an E2E journey.
- Lite cannot author or silently alter a product oracle. Missing approved E2E semantics routes to
  the mandatory product-definition chain.

## Output

The scoped change, focused regression where valuable, one real-entry check, and concise evidence.
