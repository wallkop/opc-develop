# requirement.md Format

Path: `docs/features/<numbered-slug>/requirement.md`. Hard cap: 150 lines. Decision density over
completeness — this is what the human reads to confirm "this is the thing I want".

## Structure

```
# <Feature name>            (slug: <n>-<name>, branch: feature/<n>-<name>)

## Decision Summary          ← ≤1 page; the only part the human must read
What / For whom / Value      one tight paragraph
Non-goals                    explicit exclusions, bulleted
Key tradeoffs                the 2-3 choices that shaped scope, each one line with the pick
Risk profile                 categories from risk-readiness.md, or `none identified`
Acceptance signals           observable outcomes that mean "it worked"

## Alternatives Considered   2-3 approaches, tradeoffs, why the recommendation wins

## Domain Language           canonical terms this feature commits to

## Open Questions            each with a trigger condition or owning phase, never free-floating

## Grilling Log              appended Q&A that produced the above; append-only, never rewritten
```

## Rules

- Localize every ordinary heading and prose block to the target language resolved from project
  `AGENTS.md`; keep only identifiers and parser-required tokens unchanged. Template headings are
  semantic section names, not mandatory English display text.

- Original wording is preserved; clarifications append, history is not rewritten.
- Scope gate: if the request spans independently shippable subsystems, split into separate
  features before writing this file.
- An open question that could change scope, core behavior, or risk classification blocks the file
  from being written — resolve it in grilling first.
- Every tradeoff line names what was given up, not only what was chosen.
