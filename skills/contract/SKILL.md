---
name: contract
description: "Use after design sign-off to decompose the approved PRD and technical design into implementation contracts: self-sufficient per-workstream work orders (boundaries, internal design, TDD seeds, mock retirement, AC ownership) plus an index with dependencies, thin slice, and integration steps. Gates the contract tree before build."
license: MIT
---

# contract

One contract = one implementer's complete work order. This layer merges the old spec + plan:
internal design detail and boundary discipline live together so a fresh subagent needs nothing else.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/impl-contract-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/risk-readiness.md`
- For the gate: `packs/gate-protocol.md` + `rubrics/impl-contract.md`

## Process

1. Precheck freshness of PRD and technical reviews (`check_freshness.py`). Stale ⇒ stop and route.
2. Partition the work into independently implementable contracts. Partition rules:
   - every PRD AC owned by exactly one contract; every mock inventory entry owned by exactly one;
   - parallel-safe contracts share no allowed paths;
   - thin slice first when risk categories exist, everything risky depending on it;
   - prefer fewer, fuller contracts over many thin ones — dispatch overhead is real.
3. Write each `C-XX-<name>.md` per the format: boundary globs, AC references (never restated
   text), internal design (module split, state handling, local component decisions — the detail
   technical.md deliberately excludes), TDD seeds concrete enough to start RED, mock retirement
   assignments, done-means checklist.
4. Write `index.md`: dependency table, parallel-safety column, thin slice, ordered integration
   steps the controller will run.
5. L0 precheck every file (`validate_artifacts.py <contract-file> --prd docs/features/<slug>/prd.md`), then gate
   the tree with a fresh reviewer on `rubrics/impl-contract.md`. The reviewer reads contracts
   cold — buildability by a stranger is the bar. Fix and re-gate until Approved; ledger rounds.

## Fail-open

A partition that cannot avoid shared paths means the contracts are wrong-shaped — merge them or
serialize them in the index rather than shipping a known collision. Questions the artifacts can't
answer route `revise` upstream; do not paper over gaps with invented internal design that
contradicts technical.md.

## Output

`docs/features/<slug>/contracts/` tree, gate Approved, ledger entries. Next: `build`.
