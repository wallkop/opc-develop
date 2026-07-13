# Rubric: implementation contracts

You are reviewing an explicitly requested coordination contract tree against
`formats/impl-contract-format.md`, the result card, mandatory PRD/testcase, and any technical
or mock artifacts that exist. End with one `**Status:**` line and `Reviewed-SHA:` lines per reviewed
contract/source file. This review is optional governance, not a new standard-increment gate.

## Blocking checks

1. **Buildability**: could a fresh implementer, given only one contract file plus the referenced
   sections, produce the work? Read each contract cold and flag anything that requires the
   creator's unstated intent.
2. **Boundary disjointness**: parallel-safe contracts share no allowed paths. Overlap ⇒ reject
   with the collision.
3. **In-scope partition**: every result-card constraint assigned to these workstreams is owned once;
   same for listed mock inventory entries. Do not force unrelated/future PRD ACs into this increment.
4. **Reference discipline**: contracts point to prd/technical sections; restated content ⇒ reject
   (it will drift). Redefined public APIs or re-decided SaaS choices ⇒ reject (wrong layer).
5. **TDD seed actionable**: each workstream names its highest-value boundary/regression test,
   assertion, runnable command shape, and level. Do not require all future TC skeletons upfront.
6. **Dependency order sound**: the index's dependency column is acyclic and the first runnable
   outcome is ordered before dependents.
7. **Packet sufficiency**: a cold owner can act without hidden conversation context; local notes
   stay minimal and do not duplicate the result card or technical decisions.
8. **Integration steps**: concrete, ordered, controller-runnable; not "integrate and test".
9. **No premature matrix**: reject packets that pre-author the full future test matrix instead of
   the current workstream's boundary seed and slice regression.
10. **Seam ownership**: every applicable technical public contract produced by one owner and consumed
    by another appears in the index's integration steps with an `api`-level boundary case.
    A seam covered only by the two sides' mocks of each other ⇒ reject.

## Non-blocking

Contract naming, index formatting, seed verbosity, absent future-slice skeletons.
