---
name: brainstorm
description: "Use when starting an opc-develop feature from a raw idea, or when acceptance triage classifies feedback as a taste change needing a fast increment. Grills the user one question at a time with recommended answers until product intent, domain language, tradeoffs, non-goals, and risk profile are sharp, then assigns the numbered feature slug, creates the feature branch, and writes the capped decision-first requirement.md."
license: MIT
---

# brainstorm

Capture the human's taste as a decision-dense requirement. Nothing downstream can recover
judgment that is missing here.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/requirement-format.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/decision-protocol.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/risk-readiness.md`
- On branch questions: `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- For the touchpoint: `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Process

1. Read project AGENTS.md and enough code/docs to understand the product surface. Inspect before
   asking — never ask the human something the codebase answers.
2. Scope gate: if the request spans independently shippable subsystems, propose a split and let
   the human pick the first slice.
3. Grill: one question at a time, hardest-uncertainty first, every question carrying a
   recommended answer with its reason. Walk value, users, non-goals, key paths, tradeoffs,
   alternatives (2-3 when real choice exists), domain terms, constraints. Stop grilling when new
   questions stop changing the shape — shared understanding, not exhaustion.
4. Classify the risk profile (`risk-readiness.md` categories, or `none identified`). Unknowns
   become open questions owned by `prd` or `architect`.
5. Classify remaining open questions: any that could change scope, core behavior, or risk class
   must be resolved now; the rest get trigger conditions.
6. When ready to commit: run
   `python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/next_feature_slug.py" "<name>" --features-dir <root>/docs/features`,
   create/enter `feature/<slug>` per `branch-worktree.md`, then write
   `docs/features/<slug>/requirement.md` per the format (≤150 lines, decision summary first).
7. Initialize `docs/features/<slug>/ledger.jsonl` with a risk-profile decision entry —
   `{"type":"decision","id":"RISK-PROFILE","door":"two-way","note":"<categories or none identified>"}` —
   and a `gap` entry for any harness verb already known missing.
8. Gate the requirement per `${CLAUDE_PLUGIN_ROOT}/shared/packs/gate-protocol.md` with
   `${CLAUDE_PLUGIN_ROOT}/shared/rubrics/requirement.md`.
9. Human touchpoint: write the faithful plain-language summary `reports/requirement.md`, including
   the requirement artifact SHA, then render/lint `reports/requirement.html` per `report-style.md`;
   then
   present the decision summary (≤1 page) for confirmation. Their feedback routes as tune (fix
   wording/decisions here) or park; on tune, regenerate the report from the updated md.

## Fail-open

Too-early ideas end without a branch or file — a good conversation is a valid output; say so and
stop. Never write requirement.md on the trunk. Never invent answers to taste questions: if the
human defers, record the recommended answer as provisional with a trigger.

## Output

`requirement.md` (gated), feature branch, initialized ledger. Next: `demo`.
