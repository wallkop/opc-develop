# Contracting (build phase A)

Partition the approved PRD + technical design into implementation contracts. Internal to `build`
— not a user-facing phase. Formats: `formats/impl-contract-format.md`; gate rubric:
`rubrics/impl-contract.md`.

## Partition Rules

- Every PRD AC owned by exactly one contract; every mock inventory entry owned by exactly one.
- Parallel-safe contracts share no allowed paths — overlap is a gate-blocking defect; merge or
  serialize instead of shipping a known collision.
- Thin slice first when risk categories exist; everything risky depends on it.
- Prefer fewer, fuller contracts over many thin ones — dispatch overhead is real.

## Content Rules

- Each `C-XX-<name>.md`: boundary globs, AC references (never restated text), internal design
  (module split, state handling, local component decisions — the detail technical.md deliberately
  excludes), TDD seeds concrete enough to start RED, mock retirement assignments, done-means
  checklist.
- `index.md`: dependency table (acyclic), parallel-safety column, thin slice, ordered integration
  steps the controller will run.
- Contracts point to prd/technical sections; restated content drifts and is rejected. No public
  API redefinition, no SaaS re-decisions — wrong layer.

## Gate

L0 precheck every file (`validate_artifacts.py <contract-file> --prd <prd-path>`), then one fresh
reviewer on `rubrics/impl-contract.md` reading the contracts cold — buildability by a stranger is
the bar. Fix and re-gate until Approved; ledger rounds. Questions the artifacts can't answer
route `revise` upstream; never paper over gaps with invented design that contradicts technical.md.

## Staleness

Contracts are stale when the PRD or technical.md revisions moved past the contract gate's
`Reviewed-SHA`. `build` re-runs this phase automatically on staleness; unaffected contracts are
confirmed by targeted re-review, not rewritten.
