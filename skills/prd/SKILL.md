---
name: prd
description: "Use after the demo gate is Approved to produce and gate the PRD: decision sheet with numbered PD records, AC-IDs, state machine, permissions, and appendix — plus the black-box test cases (testcases.md) that state how every AC will be proven. Ends at the product sign-off touchpoint (typically the PM), then commits and pushes the feature branch as the product-to-architecture handoff."
license: MIT
---

# prd

Convert the experienced prototype into the product taste document. Owned by whoever holds product
judgment — the PM in a duo, the builder solo. Ends with a pushed branch another person can pick up.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/prd-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/testcase-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- For the sign-off rendering: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/prd.md`

## Process

1. Precheck upstream freshness (`check_freshness.py` on the demo review). Stale ⇒ route per
   `feedback-routing.md`.
2. From requirement.md, the exercised demo, and the mock inventory, write `prd.md` per the
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
   `validate_artifacts.py`). Fix-and-re-gate until Approved. Ledger each round.
5. **Product sign-off touchpoint**: write faithful plain-language `reports/prd.md` and
   `reports/testcases.md` summaries with source artifact SHAs, render/lint their `.html` companions
   per `report-style.md`, and present the decision sheet plus testcase coverage map to the product
   owner. Two-way doors were decided and logged; `[ONE-WAY]` PD records need an explicit yes.
   Feedback routes tune/revise/park.
6. **Handoff**: commit the feature artifacts and push the feature branch. Print a handoff
   summary for the architect: branch name, demo entry point, AC and TC counts, open questions
   with triggers, risk profile, and any recorded gaps.

## Fail-open

Product questions the demo/requirement can't answer go back to the product owner as five-piece
decisions — never guessed. If the demo gate is missing entirely (legacy or imported feature),
record the gap, note the fidelity caps it implies, and continue with the human's ack.

## Output

`prd.md` and `testcases.md` (gated together, PD/AC/TC numbered), HTML sign-off reports, pushed
feature branch, handoff summary, ledger entries.
Next: `architect` — same person or a different one.
