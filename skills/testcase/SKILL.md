---
name: testcase
description: "Use after both demo and PRD are Approved to turn product intent into a separately reviewed, human-approved black-box testcase catalog and deterministic executable manifest. Required before build and before any E2E regression; defines success/failure oracles, data/provider provenance, Playwright actions, three-corner observations, and atomic Computer Use fallback."
---

# testcase

Make the product oracle inspectable before implementation. Playwright is only a driver; correctness
comes from an approved demo, durable PRD truth, explicit human review of each case, deterministic
compilation, and runner-produced evidence.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/testcase-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`
- For the gate: `${CLAUDE_PLUGIN_ROOT}/shared/packs/gate-protocol.md` +
  `${CLAUDE_PLUGIN_ROOT}/shared/rubrics/testcase.md`

## Process

1. **Fail closed on prerequisites.** Require a running demo with fresh Approved
   `reviews/demo-review.md` and a PRD with fresh Approved `reviews/prd-review.md`. Both are
   mandatory; do not reconstruct either from implementation code and do not proceed from a PRD-only
   description.
2. Exercise the approved demo through its real app-shell entry. Read the PRD ACs and demo alignment.
   Resolve disagreements at their source: experience mismatch returns to `demo`; durable truth
   mismatch returns to `prd`. Do not write a testcase that papers over either.
3. Write `testcases.md` per the format. For every case make the product owner able to judge the exact
   object, starting state, user action, visible/durable result, success and failure signals, data
   provenance, provider mode, three observation corners, and safety invariants. UI uses Playwright
   as the deterministic primary driver. Computer Use is an `atomic-only` fallback, never the oracle.
4. Run `opc_testcase.py compile --feature-dir <dir>`. This validates bidirectional AC coverage and
   compiles deterministic `testcases.json`; it refuses stale or missing demo/PRD reviews.
5. Run a fresh independent review against `rubrics/testcase.md`. The reviewer inspects
   `testcases.md`, `testcases.json`, the live demo, PRD, named data availability, and proposed runner
   contract, then writes `reviews/testcase-review.md` with Reviewed-SHA lines for both testcase
   artifacts. Repair and re-review until approved or genuinely blocked; no fixed round quota applies.
6. **Mandatory product touchpoint.** Render `reports/testcases.md/.html` with a case-by-case approval
   table. Present it before implementation. The human may tune, revise, or park. Only after an
   explicit acceptance, run `opc_testcase.py approve --actor <human-role> --decision-note <note>`.
   Never approve on the human's behalf.
7. Run `opc_testcase.py check --require-approved`. Commit and push the testcase artifacts and review
   when another person or session will build them.

## Execution contract

- Downstream E2E invokes the project testcase runner, for example `npm run case -- TC-1`; raw
  Playwright commands are not acceptance entry points.
- The project runner consumes `testcases.json`, pre-arms both success and failure observers before
  the action, and emits `opc-case-evidence-v1` with step results and hashed artifacts.
- `opc_increment.py` derives authenticity from that evidence. CLI claims such as
  `--production-assembly`, `--data-hash`, or `--trace-id` cannot upgrade completion.
- A named real object requires a canonical isolated clone or explicitly permitted live/read-only
  source. A synthetic lookalike remains `seeded passed` even when its shape matches.

## Output

Fresh Approved demo + PRD prerequisites, `testcases.md`, compiled `testcases.json`,
`reviews/testcase-review.md`, human-facing testcase report, `testcase-approval.json`, and ledger
entries. Next: `architect` only for a public/one-way boundary; otherwise `build`.
