# Rubric: prd.md

You are reviewing a PRD against `formats/prd-format.md`, requirement.md, the approved demo, and
the mock inventory. End with one `**Status:**` line and `Reviewed-SHA:` lines per reviewed file.

## Blocking checks

1. **Structure**: decision sheet (≤2 pages), numbered ACs, appendix — all present per the format.
2. **AC quality**: every AC is one sentence, black-box observable, and testable. Reject ACs that
   describe internals ("uses a queue") or bundle multiple assertions.
3. **AC coverage against the demo**: walk the approved demo's interactions; every contractual
   behavior maps to an AC or is explicitly marked placeholder in Demo alignment. Unmapped demo
   behavior is drift waiting to happen.
4. **AC coverage against requirement.md**: every acceptance signal traces to ≥1 AC.
5. **State machine soundness**: no orphan states, no undefined transitions, error states included.
6. **Permission model completeness**: every flow in the appendix names who may perform it; check
   for the classic gap — mutation endpoints reachable by roles the table forbids.
7. **Mock inventory linkage**: every inventory entry's real behavior is covered by an AC.
8. **Decision sheet honesty**: contested decisions carry the five-piece set
   (`packs/decision-protocol.md`); one-way doors are tagged.
9. **Edge cases mapped**: each edge case maps to an AC or an explicit out-of-scope note.
10. **Living-spec consistency**: when `docs/opc/specs/` exists, check the owning domain's AC
    registry — a new AC contradicting a live one without a declared supersession is blocking.

## Non-blocking

Prose quality, flow-diagram polish, appendix ordering.
