# Changelog

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
