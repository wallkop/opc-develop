# feature-plan.md Format

Path: `docs/features/<slug>/feature-plan.md`. A standard increment has exactly this one planning
artifact unless a lasting product decision or a changed public boundary independently justifies a
PRD or technical record. Keep it at 150 lines or fewer.

Keep the field names and enum values below unchanged for L0 parsing. Localize headings and field
values to the project language.

```md
# <feature>

Plan-Version: opc-increment-v1
Class: quick | standard | split
Budget-Minutes: <positive integer; standard <= 240>

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
Slice-1: 45 | <one user-visible result> | <independent black-box proof>
Slice-2: 60 | <one added user-visible result> | <independent black-box proof>

## Mock Retirement
<!-- Include only when demo/mock-inventory.md exists; one row per inventory id. -->
Mock-Retirement: M-1 | Slice-1 | <real replacement path> | <regression proving the mock is gone>

## Optional Constraints
<!-- Required only when optional prd.md or technical.md exists; list in-scope records. -->
Constraint: AC-1 | Slice-1 | <black-box proof>
Constraint: TD-1 | Slice-2 | <boundary/conformance proof>

## Acceptance
Build-Command: <cheap build/static command>
Core-Command: <real entry core-journey command>
Replay-Command: <offline provider replay, when applicable>
Provider-Command: <one final canary, when applicable>
```

Rules:

- Decide the class from elapsed-time budget, not feature nouns: ordinary <=60-minute work routes to
  `lite` without this artifact; `quick` is reserved for release-bound/oncall work that needs a
  receipt, standard is 61-240 minutes, and split is above 240 minutes. A split plan uses each Slice row as one proposed
  separately useful standard increment (each <=240 minutes), then stops; rewrite the chosen first
  increment as `Class: standard` before implementation.
- In quick/standard plans, `Slice-1` reaches the real assembled path within 45 minutes. Later slices
  are 30-90 minutes. Every slice adds one user-visible result; tables, services, and modules remain
  child tasks.
- For UI work, `When` names the browser action. API setup may prepare data but may not replace the
  action being accepted.
- If the user named an existing object, use a read-only snapshot or the real object as allowed and
  record its source hash. A hand-written lookalike is not equivalent.
- Run the core journey once before implementation and confirm it fails for the missing behavior.
- When a demo mock inventory exists, map every `M-x` exactly once. Missing, duplicate, unknown, or
  nonexistent-slice mappings block receipt initialization.
- When optional PRD/technical artifacts exist, map each in-scope `AC-n`/`TD-n` to a slice and proof.
  The final review checks that the selected scope is honest and the implementation conforms.
- Put durable product decisions in PRD only when they outlive this increment. Put a technical
  record only when a public boundary or one-way architectural decision changes.
