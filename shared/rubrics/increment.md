# Rubric: standard increment reality/final review

Review the current diff, `feature-plan.md`, `acceptance.json`, and relevant project rules. The
reality review runs after Slice-1; the final review runs after all in-scope slices. End with one
`**Status:**` line. Both records hash the plan and write `Reviewed-Revision: <content-tree>` from the
receipt. Later slices may supersede the reality revision. The final revision must match the current
content tree; appending test/human evidence to the excluded receipt does not invalidate it.

## Blocking checks

1. **Budget and outcome**: the plan is <=4 hours, has one user-visible outcome, and its slices are
   independently runnable. Multiple unrelated journeys or a >2-hour slice means scope is too large.
2. **Real target**: the data/object is the one requested, or a source-hashed allowed snapshot. A
   hand-written lookalike cannot prove compatibility with existing user data.
3. **Production assembly**: inspect the actual mount/startup path: router, session/origin/auth,
   service construction, datastore, scheduler/dispatcher when relevant. Tests against an alternate
   assembly do not count.
4. **Core journey honesty**: the receipt is fresh and the accepted action originates at the real
   interface. UI means the browser performs the key click/type/upload; API-created success is a
   bypass.
5. **Safety**: verify both plan invariants and any matching data, permission, concurrency, money,
   rollback, or idempotency risk in the diff.
6. **Test independence**: no production test control writes the success objects later asserted by
   the test. Fixtures may prepare only preconditions; state assertions are read-only.
7. **Cost ladder**: cheap checks precede browser/replay/provider evidence. A provider rerun after a
   harness/DOM/seed failure without offline stabilization is blocking.
8. **Fresh completion**: build and core-journey commands match the current revision. Code, tests,
   plan, snapshot, or tracked config changes invalidate older results.
9. **Regression**: each completed slice has its highest-value targeted regression and the previous
   core journey remains green. Do not require all future tests before their slices exist.
10. **Prototype retirement**: when `demo/mock-inventory.md` exists, every `M-x` maps to a landed
    slice, a real replacement path, and a passing regression; no inventoried mock affects the
    production runtime. Missing or ambiguous retirement evidence is blocking.
11. **Optional-record conformance**: when PRD/technical records exist, the plan maps every in-scope
    `AC-n`/`TD-n` to a slice and proof. Compare the diff and runtime behavior to those records;
    omitted applicable constraints, contradictory behavior, or unreviewed boundary drift blocks.

## Conduct

Return the complete severity-ordered finding list on the first pass; do not drip-feed one new layer
per repair. Cite file/line, receipt command ID, and the concrete failure scenario. Do not edit code.
If the review object mixes several subsystems without one independently demonstrable outcome, lead
with “slice too large” instead of attempting unlimited review rounds.
