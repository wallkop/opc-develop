# Rubric: prd.md

Review the PRD against `formats/prd-format.md` and the mandatory approved demo. Testcases are not
part of this gate. End with one `**Status:**` line and a `Reviewed-SHA:` line for `prd.md`.

## Blocking checks

1. **Fresh demo prerequisite**: `demo/prototype.md`, `demo/mock-inventory.md`, and
   `reviews/demo-review.md` exist; the review is Approved and fresh. Exercise the demo yourself.
2. **Structure**: decision sheet (at most two pages), numbered ACs, and appendix are present.
3. **AC quality**: every AC is one black-box-observable, testable sentence. Reject internals or
   bundled assertions.
4. **Demo alignment**: every contractual demo behavior maps to an AC; every placeholder is named.
5. **Intent coverage**: every requirement/result-card acceptance signal traces to at least one AC.
6. **State/permission soundness**: no orphan states, undefined transitions, or mutation permissions
   that contradict the decision table.
7. **Mock linkage**: each inventoried mock's intended real behavior is covered by an AC.
8. **Decision honesty**: contested and one-way decisions follow the decision protocol.
9. **Edge cases**: each maps to an AC or explicit non-goal.
10. **Living-spec consistency**: contradictions declare supersession rather than silently forking
    durable product truth.

## Non-blocking

Prose polish, diagram style, appendix ordering.
