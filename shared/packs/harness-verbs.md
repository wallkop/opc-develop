# Harness Verbs

A project's harness is measured by four verbs, not by documents. The standard: for any behavior
change, the agent can close the loop without a human — run the system, reset it to a known state,
drive it from the outside, and observe what actually happened inside. Capabilities are executable
(scripts, seeds, endpoints); documents only index them.

## E2E applicability

Harness capability is not a requirement to run E2E on every change.

- **No E2E by default:** copy, static styling, docs, comments, formatting, and configuration that
  does not change runtime behavior. Use targeted static/type/component/snapshot/accessibility
  checks as relevant; UI changes also get one lightweight real-entry visual/DOM before-and-after
  check that does not execute a complete journey.
- **Approved testcase E2E required:** changes to a user action or result, state transition,
  persistence, permissions, routing, provider behavior, concurrency, or a cross-module/runtime
  contract.
- If a supposedly non-semantic change alters behavior during verification, reclassify it before
  claiming completion. Do not author a new testcase merely to validate copy or static appearance.

## L1 — run

- One command starts the full local stack (`make dev` or equivalent); one command stops it.
- Fixed ports; a health endpoint or command that proves "up".
- Dev server output tees to a fixed log file path — stdout alone is invisible to agents.
- Double-start fails loudly (pidfile), never silently forks a second stack.

## L2 — reset (the precondition for determinism)

- One command returns the stack to a clean known state.
- **Named seed scenarios**: a catalog of business-meaningful fixtures invocable by name —
  `seed:empty`, `seed:small-team`, `seed:edge-heavy`, `seed:<feature-specific>` — each documented
  with one line about what world it creates. E2E cases declare which seed they stand on.
- Reset + seed is idempotent: run twice, same world.
- When a case names existing user data, expose a non-destructive canonical-clone command that uses
  datastore-native snapshot/backup semantics, emits a source hash + manifest, and starts the stack
  against the isolated copy. Never silently point E2E at the canonical writable store.

## L3 — observe (agent-legible runtime)

- **Structured logs, four elements**: JSON lines; a correlation/request ID on every entry (one user
  action's full causal chain must be reconstructable with one grep); written to a fixed file path;
  AGENTS.md documents the path and the tail/jq recipes.
- **Dev side-channels**: invisible events (emails, SMS, payment callbacks, magic links) are logged
  in dev mode so the agent can complete flows unattended.
- **State dump**: a CLI or dev endpoint answering "what state is entity X in right now"
  (`appctl dump <entity>` beats inferring from log fragments).
- **DB access**: a documented read-only query recipe (psql/sqlite3 command + generated schema doc).
  Prefer recipes over DB MCP servers — the reference MCP servers were archived with unpatched
  SQL injection, and recipes cost zero maintenance and zero context.
- Browser runtime: console/network/trace via the project's browser tooling (e.g. Chrome DevTools
  MCP or Playwright) when the feature has a UI.
- Correlations form one inspectable chain:
  `caseId -> stepId -> interactionId -> requestId/traceId -> commandId/runId/nodeId` as applicable.

## L4 — drive (black-box E2E, two tiers)

- **Tier 1 — approved testcase runner (the regression backbone):** one project entry such as
  `npm run case -- TC-1` consumes `testcases.json` and drives the interface the feature exposes —
  HTTP/API for services, CLI for tools, Playwright for UI. Raw test-framework commands stay behind
  this adapter. It emits `opc-case-evidence-v1` with per-step results, manifest hash, correlations,
  and hashed artifacts. Deterministic gates run approved cases on every semantically relevant change.
- **Tier 2 — agentic exploration:** the agent may investigate gaps and demo parity, but it cannot
  silently change product expectations. An important discovery routes back to the testcase phase
  for human review, then compiles into Tier 1.
- UI runners pre-arm positive and negative observers before one atomic Playwright action; no model
  round-trip or arbitrary sleep sits between action and decisive capture. Human-facing evidence is
  capped at three screenshots (before, signal, final); traces/video/logs may be richer.
- Computer Use is advisory and may replace only one reasoned atomic driver action. It never owns
  waits, assertions, loops, or blocking release gates.
- Evidence follows the interface/log/state triangle and reports independent assembly, data,
  provider, driver, observation, and product-outcome axes (`evidence.md`).

## Gap Accounting

Every missing verb capability found during any flow is recorded as a `gap` ledger entry with the
verb it blocks and the label cap it causes. The `harness` skill consumes gap entries as its backlog.
