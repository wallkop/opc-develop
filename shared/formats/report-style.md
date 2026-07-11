# Human Review Reports (HTML)

Artifacts that a human reads at a touchpoint get a rendered HTML companion. The markdown stays
the source of truth — gates hash and review the `.md`; the HTML is presentation only.

## When

Generate or refresh the companion at every touchpoint that presents an artifact:

| Artifact | Touchpoint |
|---|---|
| requirement.md | brainstorm decision-summary confirmation |
| prd.md + testcases.md | product sign-off |
| technical.md | architecture sign-off |
| acceptance.md + release-manifest.md | ship test-acceptance |

## Where

`docs/features/<slug>/reports/<artifact>.html` (e.g. `reports/prd.html`), committed with the
feature branch so a reviewer opens it from disk with no tooling.

## How

- One self-contained file per artifact: inline CSS, no external assets, no build step.
- Use the `frontend-design` skill when available to produce and keep one shared look across all
  report types; otherwise follow the tokens below by hand.
- Shared tokens: readable measure (~72ch), system font stack, generous whitespace; AC/TC/PD/TD
  IDs rendered as monospace badges; the decision sheet first; a table of contents for anything
  over two screens; color reserved for semantic states (one-way doors, blocking items, struck
  entries) — never decoration.
- Coverage maps render as tables; Given/When/Then render as labeled definition blocks, not code.

## Rules

- Read the applicable project `AGENTS.md` before rendering. All ordinary report headings,
  navigation, labels, summaries, and source-derived prose must use its declared target language;
  only normative machine tokens and identifiers may remain unchanged. A mixed-language report
  that violates the project rule is not ready for its human touchpoint.
- The HTML is never the review target: gate reviewers read the markdown, and `Reviewed-SHA`
  lines reference the markdown. Divergence between the two is presentation drift — regenerate
  from the md; never hand-edit the HTML.
- Regenerate whenever the source md changes after a gate (revise flows included).
- Nothing appears in the HTML that is absent from the md.
