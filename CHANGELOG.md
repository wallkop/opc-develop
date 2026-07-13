# Changelog

## 0.6.0 - 2026-07-13

- Remove all predicted-duration and implementation-effort gates. `lite`/`build` now route only by
  changed product semantics, risk, and release needs; plans no longer require `Class`,
  `Budget-Minutes`, or per-slice minute estimates. Reviews also have no fixed repair quota.
- Add an explicit E2E applicability rule: copy, static styling, docs, comments, formatting, and
  non-runtime configuration changes use proportional targeted/visual checks and do not run E2E by
  default; semantic behavior changes continue through the approved testcase runner.
- Split `testcase` out of PRD as a mandatory, separately invocable and reviewable phase after both
  an Approved demo and Approved PRD. Standard/releasable delivery now follows
  `demo -> prd -> testcase -> build`; architecture remains conditional.
- Add deterministic `testcases.json` compilation, a fresh independent testcase review, explicit
  product-owner `testcase-approval.json`, and automatic staleness when demo/PRD/case truth changes.
- Require every downstream E2E regression to enter through the project testcase runner. Raw
  Playwright commands cannot serve as acceptance commands; Playwright remains the primary UI
  driver and Computer Use is limited to a reasoned atomic fallback.
- Add `opc-case-evidence-v1`: runners report separate assembly, data, provider, driver,
  observation, and product-outcome axes, per-step results, correlations, and hashed artifacts.
  `opc_increment.py` derives labels and completion from this evidence instead of caller flags.
- Close the mtime/touch false-green: structured evidence must have new content, not merely a changed
  timestamp. Named real-object claims require canonical-clone/live-real provenance matching the
  plan hash; synthetic lookalikes remain seeded evidence.
- Require atomic positive/negative observation and the interface/log/state evidence triangle, cap
  human-facing screenshots at three per case, and bind gate-chain checks to the mandatory product
  definition and approval artifacts.

## 0.5.1 - 2026-07-13

- Restored the full system architecture map instead of replacing it with the v0.5 increment flow.
- Kept the budget-first diagram as a separate routing aid with a distinct asset path and caption.
- Rebuilt both READMEs around quick start, exact invocation, skill selection, scenario playbooks,
  best practices, new-project onboarding, and gradual existing-project adoption.
- Added a regression contract that fails when architecture/routing assets or core onboarding
  sections disappear from either README.

## 0.5.0 - 2026-07-13

Breaking default-flow change driven by a measured 38-hour false-green incident: standard work is
now budget-first and core-journey-first. The former full artifact/contract pipeline remains opt-in.

- Rebuild `build` around one 1-4 hour standard increment: 240-minute hard budget, one-page
  `feature-plan.md`, one real core journey, a <=45-minute first vertical slice, and 30-90 minute
  runnable follow-up slices. Larger work splits before implementation; ordinary <=60-minute work
  routes to `lite`, while release-bound/oncall quick work keeps the receipt chain.
- Add `opc_increment.py`, a generated revision-bound `acceptance.json` receipt with automatic
  command/time/exit/output/head/content-tree capture, runtime metadata, four completion levels, and
  automatic staleness after code/test/plan/seed/config changes, canonical exclusions, hash-chained
  command history, per-receipt interprocess locking, hashed output/evidence files, and
  latest-attempt-wins failure semantics.
- Make UI completion require a browser-driven key action through the production assembly. Add real
  `testcases.md` L0 validation for level, seed, Given/When/Then, bidirectional AC coverage, and
  `ui-e2e` browser action instead of returning “nothing checked.”
- Enforce cheap-to-expensive verification. External Provider canaries remain locked until local
  build, real core journey, and offline replay pass; allow one attempt per revision by default.
- Replace per-contract review loops with one reality review plus one final review. Ledger audit now
  enforces at most two repair rounds across the increment, rejects extra gates, and forbids
  full-conversation dispatch context. New records use `opc-ledger-v3`; v2 remains readable.
- Default to one main executor. Subagents are exceptional, bounded, cold-context tasks; heavy
  brainstorm/demo/PRD/architect skills are opt-in and disabled for implicit invocation.
- Update `ship`/`deploy` to gate on real-service/human-accepted receipts, keep optional decision
  artifacts optional, and invalidate downstream conclusions when the user rejects the tested object
  or journey. Multi-increment releases refresh all receipts once on the final combined trunk.
- Make applicable project `AGENTS.md` target language mandatory across artifacts, reviews, reports,
  conversation, and human-readable ledger values; parser-required tokens/identifiers stay stable.
- Replace the English/Chinese public workflow image and documentation around the new default.
  Helper tests increase from 32 to 60.

## 0.4.1 - 2026-07-12

- Add `vibe`, an explicit fastest-path skill that writes code directly without plans, tests,
  automated verification, browser checks, or evidence artifacts; the human owns acceptance.
- Keep destructive, production, security/permission, and irreversible data/schema actions behind
  human approval even in vibe mode.
- Document the new path in English and Chinese and expose it in Codex plugin prompts.

## 0.4.0 - 2026-07-12

- Add executable OPC benchmark cases with multiple cost/realism profiles for one historical
  problem, mandatory GREEN → RED → GREEN proof, temporary-worktree mutation/historical replay,
  machine JSON and plain-language HTML reports.
- Add ledger v2 cost spans, automatic wall time, Codex session token deltas, normalized Claude
  usage imports, cost audits and phase summaries while keeping legacy JSONL readable.
- Close the retro loop with data-quality preflight, benchmark coverage for high-value incidents,
  explicit rule lifecycle states, post-crystallization measurement, and honest missing-data gaps.
- Require a self-contained HTML companion for every human report. Chinese reports lead with the
  conclusion and user impact, and explain specialist terms beside their first occurrence.
- Add project-agnostic compressed incident fixtures for child stderr deadlock, approval decline
  termination, and external-directory deletion safety. Helper tests increase from 23 to 32.

## 0.3.0 - 2026-07-08

ATDD restructuring driven by a live-project retro: acceptance now flows AC → TC → skeleton →
green, seams have owners, Tier-1 sheds its UI-centrism, and every human touchpoint gets a
rendered report.

- **Black-box test cases as a gated PRD artifact** (`formats/testcase-format.md`, new):
  `prd` now produces `testcases.md` alongside `prd.md` — numbered TCs in Given/When/Then, each
  tracing to its AC-IDs and naming its seed scenario, gated together with the PRD at product
  sign-off (`rubrics/prd.md` gains TC coverage/traceability checks). Test intent is now decided
  where product intent is decided, not improvised at verification time.
- **Build is now acceptance-first (ATDD)**: contracting (phase A) translates every non-struck TC
  into a committed, failing Tier-1 skeleton *before any implementer is dispatched*, capturing an
  acceptance-RED run. Skeletons are fixed once gated — implementation makes them pass; a wrong
  skeleton means a wrong TC and routes `revise` to `prd`. Local verify (phase C) runs the
  skeletons first as the primary acceptance signal, then hunts gaps beyond them and distills
  discoveries into `explored` specs. `rubrics/impl-contract.md` and `rubrics/e2e.md` enforce
  skeleton coverage, fidelity, provenance, and unweakened assertions end to end.
- **Cross-contract seams have an owner**: TDD seeds declare a level (`unit`/`api`/`e2e`);
  implementers may not downgrade an `api` seed to a unit test against their own mock. The
  contract index names an `api`-level boundary case for every technical.md contract produced by
  one contract and consumed by another, and the build controller — not any implementer — runs
  them at integration. A seam proven only by two sides' mocks of each other is rejected at the
  contract gate.
- **Tier-1 de-UI-centralized** (`harness-verbs.md`): Tier-1 is defined by the interface the
  feature exposes — HTTP/API suites, CLI invocations, or browser specs. Playwright is one
  driver, not the definition; API features proven only through a UI detour are called out as
  fragile coverage.
- **HTML reports at every human touchpoint** (`formats/report-style.md`, new): requirement,
  PRD + test cases, technical design, and ship acceptance each render a self-contained,
  uniformly styled HTML companion (`docs/features/<slug>/reports/`). Markdown stays the review
  target and the hash source; reports regenerate whenever the gated md changes.

## 0.2.3 - 2026-07-03

Hardening pass driven by an external structural review: chain of custody, gate-chain L0
verification, living spec, and honest-limitation fixes.

- **Review chain of custody closed**: the reviewer itself writes the review record (its one
  permitted write) and repeats the status token in its returned text; the controller
  cross-checks via `parse_review_status.py` and never transcribes a verdict. Degraded
  (no-isolation) mode must disclose that the separation is gone.
- **`check_gate_chain.py` (new L0)**: verifies a feature's full review chain — existence, single
  Approved token, content-SHA freshness — including per-contract implementation reviews;
  declared `--skip`s are printed, never silent. Wired into `ship` precheck and `deploy`
  preflight; `harness` now proposes hook/CI wiring as a default recommendation (a decline is a
  recorded gap).
- **Living spec** (`docs/opc/specs/`, new format): each shipped feature's ACs (feature-qualified
  ids), state machines, permission tables, and PD/TD references fold in at ship's merge stage;
  conflicts are `revise`, not overwrites. `prd` checks it before writing ACs (new blocking
  rubric check), `architect` intake and `oncall` read it first.
- **Demo replay semantics defined**: after mock retirement the demo layer's replay degrades to
  PRD Demo-alignment cross-check + demo parity on the real implementation; demo-gate freshness
  is documented as document-level only.
- **Retro honesty**: `recurrence_scan.py` repositioned as exact-match pre-grouping — semantic
  clustering across pre-groups is the retro agent's job, and reports must label script-detected
  vs judged recurrences; ledger entries gain optional `wall_secs`/`tokens_est` cost fields as
  the telemetry-independent baseline.
- **Rework resolution id'd**: `rework` entries carry `RW-n`; only an entry with
  `"resolves":["RW-n"]` closes one — unrelated same-layer approvals no longer count.
- **Deploy release set defined**: preflight names the set (trunk merges since last
  `deploy-prod: ok`, or a human-declared list) and records it before checking anything.
- **Structured-lite middle tier**: multi-module changes can borrow build's phase-B machinery
  (implementer subagents + merged review gate) without demo/PRD ceremony.
- Also: shared dev infra declared a serialized resource across concurrent features; slug
  collision handling documented for duo mode; `validate_artifacts.py` AC parsing scoped to the
  Acceptance Criteria section with retired-id reuse detection; `check_freshness.py` redundant
  comparison removed; README gains a "Start Small (day one)" adoption path (lite + harness
  first). Script tests: 16 → 21.

## 0.2.2 - 2026-07-03

Pipeline realigned to the local → test → production boundary; production and incident response
become their own skills.

- **`contract` and `verify` are no longer user-facing skills** — they are internal phases of
  `build` (new packs `contracting.md` and `verification.md`; gates and rubrics unchanged).
- **`build` completes everything local in one run**: contract partitioning → TDD implementers →
  local deploy including this feature's migrations/config applied to the local/shared dev
  environment under release-ops safety rules → full black-box regression → gated acceptance
  sheet. No human touchpoint. Also the explicit re-entry point ("fix mode") for code defects
  rejected at test acceptance.
- **`ship` is test-environment only**: manifest → env-test → deploy-test → regression-test →
  acceptance-test (touchpoint ⑤) → merge to trunk on approval. Verdict routing is now explicit:
  code defect → `build` fix mode (ship resumes at deploy), artifact defect → `revise`, new need
  → `brainstorm`.
- **New `deploy` skill** — fail-closed production release: preflight (test acceptance recorded,
  code merged to trunk, manifests complete, rollback proven) → env-prod with backups and
  per-item confirmation → deploy per runbook → `@prod-safe` online regression → watch window.
- **New `oncall` skill** — production diagnosis through the observe verbs, diagnostic report
  with root cause and blast radius, then rollback / expedited hotfix (through build → ship →
  deploy, RED evidence not skippable) / mitigation; always leaves an error-ledger record and a
  long-term fix proposal.
- Release stage vocabulary extended (`regression-test`, `preflight`); diagram and READMEs
  updated to the 7-phase pipeline.

## 0.2.1 - 2026-07-03

Collaboration split, build auto-chaining, and a staged release pipeline.

- **`design` split into `prd` + `architect`** for PM/architect collaboration: `prd` ends with a
  product sign-off and a pushed feature branch (handoff summary included); `architect` starts
  with an intake pass (understand before designing; questions route back as `revise`, never
  self-answered). Solo builders run both back-to-back; intake auto-skips. Touchpoints go 4 → 5.
- **`build` auto-runs `contract`** when contracts are missing or stale against the current
  PRD/technical revisions — one invocation covers both phases; `contract` remains directly
  invocable for preparing or revising contracts without building.
- **`ship` rebuilt as a staged release pipeline** with ledger-based resume: release manifest
  (migrations/DDL with per-item rollback, env vars name-only, config, services, third-party,
  backfills — collected from the diff and gated against technical.md; drift routes `revise`) →
  test env changes + deploy (backup before DDL) → test-environment human acceptance (same
  tune/revise/park + three-way triage) → production with rollback readiness and explicit
  confirmation → online regression (`@prod-safe` Tier-1 subset, read-only evidence triangle) →
  branch cleanup. New `packs/release-ops.md`; new `release` ledger entry type with stage
  vocabulary; optional `actor` field on ledger entries for multi-person attribution.

## 0.2.0 - 2026-07-03

Complete architectural rework: from prose-feedforward harness loop to measured feedback loops
("loop engineering"). Breaking — the 27 v0.1 skills are replaced by 10.

- **Skills consolidated 27 → 10**: `brainstorm`, `demo`, `design` (PRD + technical), `contract`
  (spec + plan merged), `build`, `verify`, `ship`, `lite`, `retro` (new), `harness`
  (init + eval merged, execution-oriented). Migration map in the README.
- **Enforcement stack**: one always-loaded core contract (~1k tokens) + on-demand packs replace
  per-skill mandatory reading of up to 18 reference files (15-26k tokens per invocation → ≤5k).
- **Mechanical gates**: content-SHA review freshness (`check_freshness.py`, replaces mtime),
  structural artifact validation (`validate_artifacts.py`) as L0 gate prechecks, machine-validated
  ledger writes (`opc_ledger.py`), status parsing with `Reviewed-SHA` extraction.
- **AC-ID spine**: PRD acceptance criteria are numbered and referenced (never restated) by
  technical design, contracts, specs, reviews, and the acceptance sheet.
- **Ledger system**: per-feature `ledger.jsonl` (gates, rework routing, evidence labels, gaps,
  decisions) + project-wide `error-ledger.jsonl` (root causes at resolution time) +
  `docs/opc/rules.md` (crystallized rules with provenance and retirement review).
- **`retro` skill (new)**: mines ledgers and session data for token distribution, review
  round-trips, rework routing, and recurring errors (`recurrence_scan.py`); proposes rule
  crystallization at the lowest enforcement layer, gated by human approval.
- **Feedback model**: unified tune/revise/park taxonomy at every touchpoint; acceptance triage
  separates implementation defects, artifact defects, and taste changes; revise triggers
  SHA-verified stale cascades.
- **Decision protocol**: five-piece presentation obligation, one-way/two-way door classification,
  decision-spikes, triggered open questions.
- **Harness redefined as four executable verbs** (run/reset/observe/drive) with agent-legible
  runtime standards (structured logs + correlation IDs + fixed paths + recipes, dev side-channels,
  state dumps, read-only DB recipes) and named seed scenarios; scored by executing, not reading.
- **Two-tier E2E**: agentic exploration distilled into committed Tier-1 specs on named seeds;
  evidence triangle (UI + log chain + state) required for real-service claims; computer-use is
  advisory, never a blocking gate.
- **TDD evidence**: RED/GREEN captured as distinct report fields; missing RED is flagged as
  test-after by the merged implementation review.
- **Fail-open philosophy**: missing runbooks/services/subagents degrade honestly with recorded
  gaps and evidence-label caps; only destructive actions fail closed. Bare repositories work,
  including `lite`.
- **Fixed from v0.1 review**: non-UI features get a runnable-skeleton demo variant; reviewers now
  receive the full rubric they enforce; reviewer agent is tool-restricted read-only; parallel
  dispatch requires worktrees (no per-case judgment); single 2-round stop-loss; trunk detection
  replaces hardcoded `develop`; `${CLAUDE_PLUGIN_ROOT}` paths throughout; all normative text and
  script messages in English; dead scripts removed or wired in.

## 0.1.5 - 2026-07-01

- Adds a project-agnostic risk and readiness contract covering feature risk profiles, risk spikes, thin-slice gates, environment capability readiness, flow tiers, and evidence authenticity labels.
- Threads high-risk readiness through brainstorm, technical review, spec, testcases, plan, TDD, local E2E, release verification, Lite, and Batch Acceptance flows.
- Strengthens Harness initialization/evaluation around thin-slice smoke paths, mock/storage readiness, capability checks, and preventing mock or seeded evidence from being reported as real-provider or long-run validation.

## 0.1.4 - 2026-06-30

- Adds the native Codex repository marketplace manifest.
- Adds public security, contribution, publishing checklist, and submission copy documents.
- Documents Codex marketplace installation from the GitHub repository.
- Adds skill-level MIT license metadata for GitHub Agent Skills publishing.

## 0.1.3 - 2026-06-30

- Removes the fixed datastore default.
- Replaces fixed database defaults with a project architecture baseline rule for datastore/database decisions.
- Replaces provider-specific object storage wording with generic object/blob storage terminology.

## 0.1.2 - 2026-06-30

- Changes README default language to English and adds `README.zh-CN.md`.
- Replaces fixed-language behavior with language-adaptive output based on user request and project rules.
- Updates Codex and Claude plugin descriptions, prompts, and metadata to avoid fixed-language assumptions.
- Converts Codex skill entry descriptions and default prompts to English for public distribution.

## 0.1.1 - 2026-06-30

- Adds Claude Code plugin metadata and OPC reviewer/implementer agent definitions while keeping the root `skills/` library shared.
- Adds Claude Code usage documentation and marketplace-source metadata.

## 0.1.0 - 2026-06-30

- Initial public release of the opc-develop Codex plugin suite.
- Includes Lite, Full, Harness initialization/evaluation, release verification, and branch finishing flows.
- Includes shared artifact contracts, review status contracts, demo parity rules, mock retirement rules, and Harness documentation standards.
