# feature-plan.md Format

Path: `docs/features/<slug>/feature-plan.md`. Write it only after the mandatory demo -> PRD ->
testcase chain is fresh and approved. Keep it at 150 lines or fewer.

Keep the field names and enum values below unchanged for L0 parsing. Localize headings and field
values to the project language.

```md
# <feature>

Plan-Version: opc-increment-v1

## Outcome
User-Action: <the single action the user must complete>
Entry-Point: <real page, CLI, API, or job trigger>
Success-Signal: <what the user observes>
Non-Goals: <what this increment explicitly excludes>

## Core Journey
Journey-Type: ui | api | cli | job
Given: <traceable data and starting state>
When: <external user action>
Then: <observable result and durable state>
Production-Assembly: <entry -> session/auth -> router -> service -> scratch state -> result>
Data-Kind: synthetic | snapshot | real
Data-Source: <source name/object>
Data-Hash: <required for snapshot/real data>
Safety-1: <first invariant that must not break>
Safety-2: <second invariant that must not break>

## Slices
Slice-1: <one user-visible result> | <independent black-box proof>
Slice-2: <one added user-visible result> | <independent black-box proof>

## Mock Retirement
<!-- Include only when demo/mock-inventory.md exists; one row per inventory id. -->
Mock-Retirement: M-1 | Slice-1 | <real replacement path> | <regression proving the mock is gone>

## Optional Constraints
<!-- PRD constraints are mandatory; technical records remain conditional. -->
Constraint: AC-1 | Slice-1 | <black-box proof>
Constraint: TD-1 | Slice-2 | <boundary/conformance proof>

## Acceptance
Build-Command: <cheap build/static command>
Core-Case: TC-1
Core-Command: <project testcase runner command that names Core-Case>
Regression-Command: <project testcase runner suite command>
Replay-Command: <offline provider replay, when applicable>
Provider-Command: <one final canary, when applicable>
```

Rules:

- Route by semantics and risk, never elapsed-time or implementation-cost estimates. Do not add
  budget, duration, or effort fields to this plan. Localized non-semantic work uses `lite`; new or
  changed product behavior uses the approved `demo -> prd -> testcase -> build` chain.
- `Slice-1` reaches the real assembled path. Every slice adds one independently runnable,
  user-visible result; tables, services, and modules remain child tasks. Decompose unrelated
  outcomes for clarity, not because of a predicted duration.
- For UI work, `When` names the browser action. API setup may prepare data but may not replace the
  action being accepted.
- If the user named an existing object, use a read-only snapshot or the real object as allowed and
  record its source hash. A hand-written lookalike is not equivalent.
- Run the core journey once before implementation and confirm it fails for the missing behavior.
- When a demo mock inventory exists, map every `M-x` exactly once. Missing, duplicate, unknown, or
  nonexistent-slice mappings block receipt initialization.
- Map each in-scope PRD `AC-n` and any applicable technical `TD-n` to a slice and proof.
  The final review checks that the selected scope is honest and the implementation conforms.
- Put durable product decisions in PRD only when they outlive this increment. Put a technical
  record only when a public boundary or one-way architectural decision changes.
- `Core-Command` and `Regression-Command` must invoke the project testcase runner. Direct
  Playwright/E2E commands bypass product-approved semantics and block receipt initialization.
