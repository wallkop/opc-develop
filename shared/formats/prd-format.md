# prd.md Format

Path: `docs/features/<slug>/prd.md`. Two-part structure: a decision sheet the human reads, and an
appendix the agents read. AC-IDs are the spine of the whole downstream flow.

## Structure

```
# PRD: <feature>

## Decision Sheet                     ← the human-facing part, ≤2 pages
Key product decisions                 numbered PD-1, PD-2, ... — each with the five-piece set
                                      when contested (options/tradeoffs/recommendation/
                                      reversibility/defer-cost); ledger entries reference PD ids
State machine summary                 states + transitions, diagram or table
Permission model                      who can do what, one table

## Acceptance Criteria                ← the machine spine
AC-1: <one testable sentence>
AC-2: ...
                                      Every AC is externally observable (black-box), numbered,
                                      never renumbered — retired ACs are struck through, new ones
                                      appended.

## Appendix                           ← agent-facing detail
User flows                            per path: steps, states touched, ACs proven
Data flow & lifecycle                 what is created/updated/deleted, retention
Edge cases & error states             each mapped to an AC or explicitly out of scope
Demo alignment                        which demo interactions are contractual (layout, interaction,
                                      state visibility), which were placeholder
Non-goals                             inherited from requirement.md plus PRD-level exclusions
```

## Rules

- Every downstream artifact (technical, impl-contract, testcases, reviews, acceptance report)
  references ACs by ID and never restates their text.
- An AC that cannot be verified black-box is a spec detail, not an AC — move it to the appendix.
- Behavior visible in the approved demo but absent from ACs is a gap: add the AC or mark the demo
  behavior placeholder in Demo alignment.
- Changes to ACs after approval are a `revise` (stale cascade applies), never a silent edit.
