# Rubric: prd.md + testcases.md

You are reviewing an explicitly requested PRD and its black-box test cases against
`formats/prd-format.md`, `formats/testcase-format.md`, and whichever approved requirement/demo/mock
artifacts actually exist. End with
one `**Status:**` line and `Reviewed-SHA:` lines per reviewed file (prd.md and testcases.md).

## Blocking checks

1. **Structure**: decision sheet (≤2 pages), numbered ACs, appendix — all present per the format.
2. **AC quality**: every AC is one sentence, black-box observable, and testable. Reject ACs that
   describe internals ("uses a queue") or bundle multiple assertions.
3. **AC coverage against the demo, when present**: walk the approved demo's interactions; every
   contractual behavior maps to an AC or is explicitly marked placeholder in Demo alignment.
4. **AC coverage against requirement.md, when present**: every acceptance signal traces to ≥1 AC.
5. **State machine soundness**: no orphan states, no undefined transitions, error states included.
6. **Permission model completeness**: every flow in the appendix names who may perform it; check
   for the classic gap — mutation endpoints reachable by roles the table forbids.
7. **Mock inventory linkage, when present**: every inventory entry's real behavior is covered by
   an AC.
8. **Decision sheet honesty**: contested decisions carry the five-piece set
   (`packs/decision-protocol.md`); one-way doors are tagged.
9. **Edge cases mapped**: each edge case maps to an AC or an explicit out-of-scope note.
10. **Living-spec consistency**: when `docs/opc/specs/` exists, check the owning domain's AC
    registry — a new AC contradicting a live one without a declared supersession is blocking.
11. **TC coverage, both directions**: every non-struck AC has ≥1 TC in the coverage map; every TC
    references ≥1 existing AC. Verify against the Cases section, not the map alone.
12. **TC quality**: each case is black-box (no internals, no implementation vocabulary), has a
    concrete Given/When/Then whose `Then` includes the resulting state (not only the screen),
    declares its `level` (`api`/`ui-e2e`), and names a seed scenario. A case that cannot name its
    world ⇒ reject.
13. **Level fitness and action origin**: `ui-e2e` is used where the accepted behavior includes a UI
    action and declares `Driver-Action: browser | ...`; API-created success followed by browser
    inspection is a bypass and blocks. API-only observables use the real running API.
14. **Mechanical validation**: `validate_artifacts.py testcases.md --prd prd.md` reports actual
    structure and bidirectional coverage success; a `nothing checked` note is blocking.

## Non-blocking

Prose quality, flow-diagram polish, appendix ordering.
