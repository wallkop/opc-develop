# OPC Core Contract

Load this contract for every opc-develop skill. Load other packs only when the current role needs
them. Enforce at the lowest useful layer: script/hook (L0) > structured artifact (L1) > prose (L2).

## Route by semantics and risk

- `vibe`: only when the human explicitly owns all acceptance and requests no tests/verification.
- `lite`: one localized result that does not create or change E2E product semantics; no feature
  artifacts or subagents. Do not use when the result must enter `ship`/`deploy` and therefore needs
  a revision-bound receipt.
- `build`: new or changed behavior, state, data, permissions, cross-module contracts, or
  release-bound work; one plan, one core journey, runnable slices.
- Independent outcomes may be decomposed for clarity. Never route, block, stop, or split work based
  on a predicted duration or implementation-cost estimate.

Risk adds a matching check; it does not automatically add architecture ceremony. Every `build`
flow has one mandatory product-definition chain: `demo -> prd -> testcase -> build`. `architect`
remains conditional on a public boundary or one-way technical decision. `vibe` and ordinary `lite`
stay outside this chain only while they make no E2E or release claim.

Pure copy, static styling, docs, comments, formatting, and configuration changes with no runtime
behavior change do not run E2E by default. Verify them with the matching static/component/a11y
check and, for UI, a lightweight real-entry visual/DOM before-and-after check. If the observed user
journey, state, data, permission, routing, or contract semantics change, reclassify and execute the
approved testcase through the project runner.

## Status tokens

Reviews end with exactly one line: `**Status:** Approved` or `**Status:** Issues Found`.
Implementers report exactly one of: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`.
Tokens are machine-parsed (`shared/scripts/parse_review_status.py`). Never translate or duplicate
them.

## Core journey and evidence before claim

Define and approve external journeys in the testcase phase before implementation: traceable
starting data, real entry, user action, production assembly, positive and negative signals, visible
result, durable state, and safety invariants. UI acceptance requires the project testcase runner to
perform the Playwright action; API/DB preparation may not manufacture the accepted result. If the
user named existing data, a synthetic lookalike is not equivalent—use a permitted source-hashed
canonical clone or real object.

Never claim passed, fixed, verified, done, or releasable without fresh evidence from the current
content tree: command, exit code, output path, branch/commit, and authenticity label. A report alone
is a claim to inspect. Every verification uses one label:
`mock passed` | `seeded passed` | `local real service passed` | `external provider passed` |
`human accepted` | `long-run passed` | `not run` | `pending` | `blocked`.

Report the highest achieved completion level exactly:

1. `code-build`
2. `automated-core-journey`
3. `real-service-core-journey`
4. `human-accepted`

`opc_increment.py` binds standard-increment receipts to code, the approved testcase manifest,
tests, plan, seed, and tracked config;
any change invalidates old command conclusions. Missing environment capability caps the level and
creates a visible gap. It never upgrades a claim.

## Verification cost order

Use logic/build -> local service + scratch state -> browser core journey -> saved-provider replay ->
one real-provider canary -> human acceptance. Cheap targeted tests may run after relevant edits;
browser journeys run at slice boundaries; full gates run at integration/final; provider canaries
never serve as the ordinary debug loop.

E2E regressions execute an approved testcase through the project case runner and emit
runner-generated evidence. Caller flags cannot assert production assembly, data provenance, driver
action, or trace completeness. Tests may use public interfaces, independent provider fakes,
source-hashed snapshots, and read-only state assertions. Production code must not expose a test
control that directly creates the
Run/Event/Artifact/Receipt the test later calls success.

## Reviews

A standard increment has one reality review after the first vertical slice and one final integration
review. The first pass returns a complete severity-ordered finding list. Repair and re-review until
the work passes or a genuine blocker requires user input, external state, or redesign. Do not impose
a fixed review or repair quota.

Start reviewers cold with the rubric, plan/artifact, diff, receipt/evidence, and project rules only.
Use `fork_turns: none` or the host equivalent. Never copy the full conversation. If isolation is
unavailable, self-review after a deliberate cold reread and disclose `self-reviewed (no isolation)`.

## Subtasks and context

The main executor implements by default. Dispatch only truly independent bounded work, with one
implementer and one reviewer at most concurrently. Every task receives a one-page packet with paths,
scope, commands, and acceptance—not creator reasoning or unrelated history. `fork_turns: all` and
`context_mode: all` are forbidden. End long stages with a <=1-page handoff: goal, current code,
unresolved issue, and next command.

## Feedback taxonomy

Classify human feedback as exactly one of:

- `tune` — same intent, different execution; iterate in the current slice.
- `revise` — plan/upstream truth was wrong; fix the earliest broken layer, invalidate downstream
  evidence, and replay forward.
- `park` — stop this line of work and close it cleanly.

Acceptance failures additionally separate implementation defect, artifact/plan defect, and taste
change. If the human says the tested object or journey is not theirs, mark the candidate rejected,
invalidate tests/receipts, and rewrite the result card before coding again.

## Freshness

Reviews record `Reviewed-SHA` per artifact using `git hash-object`; `check_freshness.py` verifies.
Standard command receipts use a content-tree fingerprint so an unchanged commit does not invalidate
them while content changes do. Never trust mtimes or manually copied SHAs.

## Failure philosophy

Fail open with a recorded cap for missing runbooks, services, observability, or isolation. Fail
closed for destructive/irreversible actions, production mutations, external publication, and human
product/technical decisions that cannot safely be inferred.

## Ledger and measurement

Append gate, phase, dispatch, rework, evidence, release, and gap records through
`shared/scripts/opc_ledger.py`. Wrap measurable phases/gates/dispatches in `span-start`/`span-end`;
wall time is automatic and token usage is recorded when exposed. Never invent missing usage.

Dispatch records require `context_mode: none|summary`. Standard gates use `flow: increment-v1` and
`gate: reality|final`; `opc_ledger.py audit` verifies their order and approval. Command and
provider counts live in the generated acceptance receipt. Missing telemetry prevents efficiency
claims but does not block implementation.

Resolved high-value failures (P0/P1, false-green, irreversible-risk, recurrence) link a project
benchmark case or a human-approved waiver. A rule becomes verified only after GREEN -> RED -> GREEN.

## Language and human reports

Read applicable project `AGENTS.md` files from repository root to artifact scope. Target-language
rules govern conversation, artifacts, review findings, reports, and human-readable ledger values.
Only parser-required tokens, IDs, commands, paths, code identifiers, evidence labels, and fixed
format keys retain normative spelling.

Markdown/JSON is machine truth. When a workflow calls for a human report, provide the self-contained
HTML companion per `formats/report-style.md`, lead with conclusion/user impact, and explain specialist
terms at first use.

## Pack index

- `packs/increment.md` — semantics-routed increment after mandatory product definition.
- `packs/gate-protocol.md` — isolated review mechanics, freshness, and convergence.
- `packs/evidence.md` — receipt fields, labels, RED/GREEN, runtime evidence.
- `packs/risk-readiness.md` — matching risk checks and first-slice spikes.
- `packs/tdd-implement.md` — targeted TDD/debugging and exceptional bounded dispatch.
- `packs/decision-protocol.md` — human decisions and reversible/one-way doors.
- `packs/feedback-routing.md` — tune/revise/park, invalidation, acceptance triage.
- `packs/branch-worktree.md` — branch/worktree rules and destructive-operation confirmation.
- `packs/harness-verbs.md` — run/reset/observe/drive standards and named seeds.
- `packs/release-ops.md` — test/production release safety.
- `packs/mock-retirement.md` — prototype mock inventory and slice-based retirement.
- `packs/contracting.md` — optional coordination contracts only when explicitly justified.
