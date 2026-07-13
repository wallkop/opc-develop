# Prototype Mock Retirement

Demo prototypes may fake data; production may not. This pack closes that loop.

## Inventory

Every mock introduced during `demo` gets one entry in
`docs/features/<slug>/demo/mock-inventory.md`:

```
- id: M-1
  file: src/features/export/api.ts
  type: fixture | stubbed-endpoint | hardcoded-state | fake-timer | other
  scenario: what it fakes and why
  replacement: which real capability replaces it (API, query, service)
```

Mocks live inside the real frontend codebase on the feature branch — never a detached playground,
never a query-param-only alternate root app.

## Lifecycle

1. **demo** creates the inventory alongside the prototype.
2. **prd** carries the inventory forward; the PRD's ACs must cover the real behavior each mock fakes.
3. **feature plan** maps every `M-x` to the runnable slice that replaces it and the regression that
   proves the real capability. Unmapped mocks block the final review.
4. **build** replaces or removes each mock as its owning slice lands and records the real path.
5. **Final audit** (end of `build`): a fresh reviewer proves no prototype mock still affects
   production runtime — grep for inventory markers, inspect changed files, run focused tests.
   Ambiguous evidence = not retired.

## Hard Rule

No feature claims `DONE` while any inventory entry lacks retirement evidence. A mock deliberately
kept (e.g. dev-only fixture) is re-classified as a permanent harness fixture, moved out of the
inventory, and recorded in the ledger with the reason.
