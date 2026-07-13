# testcases.md Format

Use `docs/features/<slug>/testcases.md` only when an explicit PRD needs a durable black-box case
catalog. A standard increment normally keeps one core journey in `feature-plan.md` and adds focused
regressions slice by slice.

Keep machine fields/IDs unchanged; localize headings and Given/When/Then prose as project rules
require.

```md
# Test Cases: <feature>

## Coverage Map
| AC | Cases |
| --- | --- |
| AC-1 | TC-1, TC-4 |

## Cases
### TC-1: <title> [level: api|ui-e2e] [seed: seed:<name>] [AC-1, AC-7]
Given <traceable starting world>
When <external user action>
Driver-Action: browser | <the click/type/upload>   # required for ui-e2e
Then <observable result and durable state>
```

Rules:

- Every active AC maps to >=1 case and every case maps back to existing ACs. TC IDs are never
  renumbered; retire by strike-through and append new IDs.
- Every case declares `level`, named seed, and Given/When/Then. Run
  `validate_artifacts.py testcases.md --prd prd.md`; “nothing checked” is never a valid gate.
- `ui-e2e` means the browser performs the key user action and therefore requires
  `Driver-Action: browser | ...`. API setup may prepare Given state but cannot create the accepted
  result. API-only behavior should use `level: api` against the real running interface.
- If existing user data is material, the named seed resolves to a source-hashed snapshot. A
  hand-written shape-alike proves only synthetic logic.
- Cases state product truth. Executable regressions are added with their owning slice; do not
  commit the whole future skeleton matrix before implementation.
- Any approved case change invalidates downstream evidence tied to the old content.
