# Rubric: requirement.md

You are reviewing a requirement document against `formats/requirement-format.md`. Judge the
artifact, not the author. Cite line/section for every blocking finding. End with exactly one
`**Status:**` line and one `Reviewed-SHA:` line per reviewed file.

## Blocking checks

1. **Decision summary completeness**: what/for-whom/value, non-goals, tradeoffs, risk profile,
   acceptance signals all present and specific. "Improve UX" is not a value; "faster export" is.
2. **Scope unity**: the feature is one independently shippable thing. Multiple subsystems bundled
   together ⇒ reject with a split proposal.
3. **Tradeoffs are real**: each names what was given up. A tradeoff list with no losses is
   advocacy, not analysis.
4. **Open questions are safe**: none of them could change scope, core behavior, or risk
   classification. Each has a trigger condition or owning phase.
5. **Risk profile plausibility**: check the feature description against the eight categories in
   `packs/risk-readiness.md`; a feature calling external APIs classified `none identified` is wrong.
6. **Length**: over 150 lines ⇒ the summary has leaked detail; reject with what to move or cut.
7. **Acceptance signals are observable**: someone could check them without reading code.

## Non-blocking (note, don't block)

Domain language completeness, alternative depth, grilling-log tidiness.
