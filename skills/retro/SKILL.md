---
name: retro
description: "Use weekly, or after finishing features, to run the loop-engineering pass: mines feature ledgers, the error ledger, and session/usage data for token distribution, review round-trips, rework routing, recurring errors, and gate effectiveness; proposes rule crystallization at the lowest enforcement layer and process prunings — all gated by human approval."
license: MIT
---

# retro

The loop that improves the loop. Heavy process is what you run when you can't measure; this skill
is how measurements replace process.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/ledger-format.md`

## Process

1. **Collect** (whatever exists; each source is optional):
   - Feature ledgers: `opc_ledger.py summary` per active feature. Cost approximation comes from
     the ledgers themselves (`rounds`, optional `wall_secs`/`tokens_est` fields) — this is the
     always-available baseline.
   - Error ledger: `python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/recurrence_scan.py"
     docs/opc/error-ledger.jsonl --json` — **pre-grouping only** (exact string match). You must
     then semantically cluster across the pre-groups, at least within each tag: two records with
     the same root-cause meaning but different phrasing are one cluster. Label the report
     honestly: script-detected vs semantically-judged recurrences.
   - Session data when available: Claude Code OTel metrics or `/insights` output, transcript
     token usage. Absence is a note, not a blocker — but then say "estimated from ledger", not
     "measured".
2. **Compute the report** (one page, docs/opc/retro/<date>.md):
   - Token/effort distribution by phase; framework overhead trend.
   - Review round-trips per gate; gates with N consecutive zero-finding approvals flagged as
     downgrade candidates (blocking → sampled).
   - Rework routing distribution: which layer eats the reworks. Mostly `implementation` means
     upstream docs are working; upstream-heavy means taste capture is failing — name the layer.
   - `change` vs `rework` ratio (taste drift vs defects).
   - Recurring error clusters with counts and features.
   - Gap backlog status: open harness gaps and the label caps they cause.
3. **Propose crystallizations** for each recurring cluster, lowest layer first
   (`ledger-format.md` rules section): L0 lint/test/hook > gate-rubric line > AGENTS.md line.
   Each proposal names the layer, the exact artifact, and its provenance records.
4. **Propose retirements**: rules in `docs/opc/rules.md` unfired for 8 weeks; all rules after a
   model major-version change.
5. **Human touchpoint**: present report + proposals. Only human-approved rules are written to
   `docs/opc/rules.md` (and their L0 artifacts created); false crystallization is worse than slow
   crystallization. Record approvals in the rules file with provenance.
6. **Measure the rules**: for previously crystallized rules, report post-crystallization
   recurrence — zero means it works; recurrence means the layer was too weak, propose one layer
   down (prose → hook).

## Fail-open

An empty error ledger with weeks of activity is itself a finding: capture points are being
skipped — say so and check `build`/`lite` usage. Never fabricate metrics; report "no data" where
there is none.

## Output

`docs/opc/retro/<date>.md`, approved rule/retirement changes, updated `docs/opc/rules.md`.
