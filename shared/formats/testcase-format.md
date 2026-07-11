# testcases.md Format (black-box acceptance cases)

Path: `docs/features/<slug>/testcases.md`. Authored by `prd` together with prd.md and reviewed by
the human at the product sign-off. This is the readable statement of how the feature will be
proven — every case is black-box: no internals, no implementation vocabulary.

## Structure

```
# Test Cases: <feature>

## Coverage Map                       one row per AC. An AC with no case is a PRD defect —
| AC   | Cases        |              an untestable AC, not a formatting gap.
| AC-1 | TC-1, TC-4   |

## Cases
### TC-1: <one-line title>  [level: api|ui-e2e]  [seed: seed:<name>]  [AC-1, AC-7]
Given  <the world, stated in seed terms>
When   <the external action — a request, a click, an upload>
Then   <the observable outcome: the response or UI, and the state that must hold afterwards>
```

## Rules

- Localize headings, labels, Given/When/Then keywords, and all ordinary prose to the target
  language resolved from project `AGENTS.md`. Keep TC/AC IDs, `level`, named seeds, commands, and
  parser-required tokens unchanged.
- TC-IDs are never renumbered — retired cases are struck through, new ones appended (same rule
  as ACs). Downstream artifacts reference TC-IDs and never restate case text.
- Every non-struck AC has ≥1 TC; every TC references ≥1 existing AC.
- `level` declares the outermost interface that drives the case: `api` (real HTTP/CLI against the
  running service) or `ui-e2e` (browser). Prefer `api` when both would prove the AC — cheaper and
  less brittle; use `ui-e2e` when the AC's observable *is* the UI.
- Every TC declares a named seed scenario (harness L2). A case that cannot name its world is not
  executable and will not survive build phase A.
- Given/When/Then stay in domain language the product owner can read — this file is part of the
  product sign-off, written to be read. `Then` includes the state that must hold, not only what
  the screen shows.
- Downstream: build phase A translates every TC into a committed **failing** Tier-1 skeleton
  (`packs/contracting.md`). The TC text is the source of truth for skeleton assertions; weakening
  a skeleton so it passes is an artifact defect routed `revise` — never an edit.
- Changes after approval are a `revise` (stale cascade applies), never a silent edit.
