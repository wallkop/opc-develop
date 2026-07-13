# Implementation Contract Format

Path: `docs/features/<slug>/contracts/` — one `C-XX-<name>.md` per independently implementable
workstream plus one `index.md`. This optional layer is a compact coordination packet for one owner;
the owner may be the main executor, a human, or the single exceptional implementer subagent.

## index.md

```
# Contracts: <feature>

| id | name | depends on | parallel-safe | ACs owned | mocks owned |
|----|------|-----------|---------------|-----------|-------------|
| C-01 | export-api | — | yes | AC-1..3 | M-1 |
...

First runnable outcome: C-01          (only when contracts are explicitly justified)
Integration steps:                    ordered controller-run steps after all contracts complete
```

## C-XX-<name>.md

```
# C-XX: <name>

## Boundary
Allowed paths:                        globs the implementer may change
Forbidden paths:                      globs it must not touch
ACs owned:                            AC-IDs this contract proves (reference, don't restate)
References:                           prd.md#section, technical.md#TD-n — pointers, not copies

## Local Notes
                                      only owner-specific detail not already clear from the result
                                      card/code; do not build a second design document

## TDD Seed
                                      one highest-value boundary/regression seed for this workstream;
                                      future slice tests are added when their behavior lands

## Mock Retirement
                                      inventory entries (M-x) this contract retires, and how

## Done Means
                                      per-task completion checklist: RED/GREEN evidence, tests
                                      green, boundary respected, mocks retired, report filed
```

## Rules

- Different contracts must be independently implementable; shared-file overlap between
  parallel-safe contracts is a gate-blocking defect.
- Contracts reference upstream artifacts by section pointer; a contract that restates PRD or
  technical content will drift and is rejected at the gate.
- No public API redefinition, no SaaS re-decisions — that is technical.md's territory.
- Every mock in the inventory appears in exactly one contract's Mock Retirement section.
- Contracts do not require subagents, per-contract review gates, or an upfront skeleton for every
  future test case. Reality/final integration reviews remain the standard gates.
