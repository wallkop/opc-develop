---
name: prd
description: "Use only when durable product decisions, a state machine/permission contract, or a PM-to-architecture handoff independently justifies a PRD. Produces numbered PD/AC records and structurally validated black-box testcases. It is optional and not a prerequisite for a normal build increment of up to four hours."
license: MIT
---

# prd

Record durable product truth. Owned by whoever holds product judgment — the PM in a duo, the
builder solo. Ends with a pushed branch when another person must pick it up.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/prd-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/testcase-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- For the sign-off rendering: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/prd.md`

## Process

1. Read the result card and whichever requirement/demo artifacts exist; verify freshness for every
   upstream review that is present. Missing optional layers are not gaps.
2. From those inputs and the human's durable product decisions, write `prd.md` per the
   format. Before writing ACs, check the owning domain's living spec (`docs/opc/specs/`, when it
   exists) for conflicts with existing system behavior — a new AC that contradicts a live one
   must declare the supersession explicitly. ACs are the spine — every contractual demo
   behavior, acceptance signal, and edge case maps to a numbered AC. The decision sheet stays ≤2 pages; contested decisions get numbered PD
   records with the five-piece set; product one-way doors are tagged.
3. From the ACs, write `testcases.md` per `testcase-format.md`: every AC gets ≥1 black-box case
   (Given/When/Then, declared `level`, named seed). Writing the cases is the cheapest audit the
   PRD will ever get — an AC you cannot phrase as a case is not testable; fix the AC now, not in
   build.
4. Gate the PRD + testcases together (fresh reviewer, `rubrics/prd.md`, L0 precheck via
   `validate_artifacts.py --prd <prd>`). Apply the shared two-repair stop-loss; unresolved blockers
   reduce scope or return to product judgment. Ledger each round.
5. **Product sign-off touchpoint**: write faithful plain-language `reports/prd.md` and
   `reports/testcases.md` summaries with source artifact SHAs, render/lint their `.html` companions
   per `report-style.md`, and present the decision sheet plus testcase coverage map to the product
   owner. Two-way doors were decided and logged; `[ONE-WAY]` PD records need an explicit yes.
   Feedback routes tune/revise/park.
6. **Handoff when needed**: commit and push. If architecture work is justified, print branch,
   entry point, AC/TC counts, open questions, risk profile, and gaps. Otherwise return to `build`.

## Fail-open

Product questions the available inputs cannot answer go back to the product owner as five-piece
decisions—never guessed. An optional demo being absent is not a gap; claiming interaction taste was
exercised when it was not is.

## Output

`prd.md` and `testcases.md` (gated together, PD/AC/TC numbered), HTML sign-off reports, pushed
feature branch, handoff summary, ledger entries.
Next: `build`, or `architect` only for a changed public boundary/one-way decision.
