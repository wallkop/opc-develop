---
name: retro
description: "Run the measured loop-engineering pass: audit ledger/usage quality, evaluate executable incident cases and crystallized rules, mine recurrence and rework, then propose verified process changes for human approval."
license: MIT
---

# retro

The loop that improves the loop. A historical problem becomes a cheap repeatable experiment; a
rule becomes active only after that experiment proves it can kill the bad variant.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/ledger-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/benchmark-case-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Process

1. **Data-quality preflight**: audit every active feature/error ledger and generated acceptance
   receipt. Count eligible phase/gate/dispatch entries, cost coverage, unmapped sessions, invalid
   gaps, command/provider capture, and benchmark linkage. Missing cost data creates or updates one
   stable `observe` gap with its label cap; never duplicate it.
2. **Collect**: feature summaries, exact-match error pre-groups, semantic clusters, normalized
   Codex/Claude usage, benchmark reports, and crystallized rules. Label script findings separately
   from semantic judgment.
3. **Compute**: measured/no-data cost by phase, time to first runnable core path, command
   and repeated-test counts, subtask/context modes, review/repair rounds, provider calls/cost,
   rework routing, user corrections, post-completion fixes, recurring clusters, open gaps,
   benchmark coverage, and false-green gates. Do not call missing capture “zero recurrence” or
   “efficient.”
4. **Executable case check**: every P0/P1, irreversible-risk, false-green, or recurring incident
   links a project case, or a human-approved waiver. Profiles reproduce one problem at different
   cost. Prefer the cheapest stable profile and report when real calibration is stale.
5. **Crystallize**: propose the lowest enforcement layer. Approval records `approved`; building
   records `implemented`; only a linked GREEN → RED → GREEN report promotes `verified`, then
   `active-unmeasured` until later observations exist.
6. **Measure**: after approval, count linked recurrences and rule fires. Zero with healthy capture
   becomes `effective`; recurrence becomes `recurring` and proposes a lower layer; 8 weeks unfired
   or a model major-version change becomes a retirement candidate.
7. **Human report**: write `docs/opc/retro/<date>.json` and `.md`, then render/lint
   `docs/opc/retro/<date>.html`. Lead with conclusion, user impact, evidence, and decision. Only
   human-approved rule changes are written to `docs/opc/rules.md`.

## Fail-open

Missing telemetry or environments cap claims and create gaps; they never justify fabricated
metrics. Destructive benchmark profiles and real external environments require explicit approval.

## Output

Structured JSON and markdown truth, mandatory plain-language HTML, approved rule lifecycle
updates, and linked benchmark evidence.
