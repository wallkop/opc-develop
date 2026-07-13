# Decision Protocol

How decisions are made, and which ones reach the human.

## Door Classification

Classify every decision before deciding who makes it:

- **Two-way door** (reversible, local blast radius): the agent decides, records the decision and
  rationale in the ledger, and moves on. The human can veto retroactively via `retro` or any
  touchpoint. Do not interrupt the human for two-way doors.
- **One-way door** (irreversible, or cross-cutting blast radius: data schema, public API shape,
  SaaS/provider commitment, pricing-visible behavior, security posture): must be presented to the
  human and explicitly approved. Mark `[ONE-WAY]` wherever recorded.

## Presentation Obligation

A decision may be presented to the human only with the complete five-piece set:

1. Options (2-3 viable ones, honestly characterized)
2. Tradeoffs per option
3. Recommendation with the reason it wins
4. Reversibility tag (`[ONE-WAY]` / `[two-way]`)
5. Cost of deferring ("if you don't decide now, X happens")

If you cannot fill the set, you have not finished thinking — investigate further or run a
decision-spike. Never present a raw open question to the human.

## Questions From the Human

Answer with evidence: cite code, artifacts, demo behavior, or research. "I believe" is not an
answer. A question you cannot answer with evidence becomes either:

- a **decision-spike**: the smallest real experiment (prototype, benchmark, data query) that produces
  the missing evidence, then returns to the decision; or
- an **open question with a trigger**: proceed on the recommended path and record
  "revisit when <condition>" in the artifact and ledger.

Both keep the flow moving; neither hides the uncertainty.

## Decision Records

Technical decisions are recorded ADR-style inside `technical.md` (see
`formats/technical-format.md`): context, options considered, decision, consequences, reversibility.
Product decisions live in the PRD decision sheet. Ledger entries reference them by ID.
