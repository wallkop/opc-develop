---
name: product-brainstorm
description: "Use when starting a opc-develop feature from raw requirement input before demo, PRD, technical design, spec, plan, or coding. Runs an opc-adapted grilling gate to clarify product intent, domain language, tradeoffs, goals, non-goals, user paths, constraints, alternatives, blockers, then assigns the next numbered feature slug in {x}-{feature} format and writes the requirement document."
license: MIT
---

# product-brainstorm

## Required References

Read before acting:

- `../../shared/references/harness-artifact-contract.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/requirement-format.md`
- `../../shared/references/grilling-domain-contract.md`

## Required Scripts

Use when assigning a new feature slug:

- `../../shared/scripts/next_feature_slug.py`

## Inputs

Raw user requirement, project context, existing docs, attachments, and any prior decisions.

## Hard Gates

Do not create demo, PRD, technical design, spec, plan, testcase, code, or worktree in this skill. Early brainstorming may stay on the current branch and may end without a branch. Once this skill is ready to write or update `requirement.md`, it must create or enter the corresponding `feature/<numbered-slug>` branch first. Do not write `requirement.md` on `develop`, `main`, or `master`.

## Process

1. Resolve project root and read applicable `AGENTS.md`.
2. Inspect current branch and dirty state according to `branch-stage-contract.md`.
3. Inspect enough project context to understand product surface and constraints.
4. Run the scope decomposition gate from `requirement-format.md`; split or stop when the request spans independently shippable subsystems.
5. Run the opc-adapted grilling gate from `grilling-domain-contract.md`: walk the product decision tree branch by branch, inspect code/docs before asking when possible, ask one question at a time, include a recommended answer for every human question, and keep resolving dependencies until shared understanding is reached or a blocker is clear.
6. During grilling, apply the domain modeling rules from `grilling-domain-contract.md`: challenge conflicting terminology, propose canonical terms, keep pending glossary/ADR notes before the feature branch exists, and only promote stable project-wide terms or ADRs after branch rules allow artifact writes.
7. Explore 2-3 viable product approaches when there is meaningful choice; record tradeoffs and one recommendation. Do not hide unresolved scope, UX, or product semantics inside a single recommended path.
8. Stop without creating a branch when the requirement is still too unclear, may be cancelled, lacks enough direction to commit a feature artifact, or has a blocking question that could change scope, core behavior, or acceptance.
9. When ready to commit the requirement, derive the base feature name, then run the bundled script `../../shared/scripts/next_feature_slug.py` resolved relative to this skill directory: `python3 ../../shared/scripts/next_feature_slug.py "<feature-name>" --features-dir <project-root>/docs/features`. Use its output as the next numbered feature slug in `<number>-<feature-name>` format with no zero padding.
10. Before writing `requirement.md`, create or enter `feature/<feature-slug>` according to `branch-stage-contract.md`. If the current branch is not `develop` and not the matching feature branch, ask the user to confirm the base branch. If dirty state is unrelated or unclear, stop.
11. Write or append `docs/features/<feature-slug>/requirement.md` on the feature branch, including the grilling summary, confirmed domain language, alternatives, tradeoffs, recommendation, non-blocking open questions, and any glossary or ADR follow-ups.
12. Write stable project-wide glossary or ADR artifacts only when the criteria in `grilling-domain-contract.md` are met and the project `AGENTS.md` permits the target paths; otherwise keep them as requirement follow-ups.
13. Initialize `progress.md` if it does not exist and record the feature branch.
14. Run the requirement self-review from `requirement-format.md`, including the grilling readiness criteria.

## Output Contract

Write `docs/features/<feature-slug>/requirement.md` following the requirement format, where `<feature-slug>` is the full numbered slug such as `1-knowledge-base`. Preserve original requirement wording and append clarifications instead of rewriting history.

## Self-Check

Verify feature slug is numbered with no leading zero, current branch is `feature/<feature-slug>` or a project-approved equivalent, the grilling gate reached shared understanding or a blocker, goals, non-goals, key paths, constraints, domain language, open questions, alternatives, tradeoffs, recommendation, acceptance signals, glossary/ADR follow-ups, and self-review conclusions are present.
## Blockers

Stop and report a blocker when required inputs are missing, an upstream review is not Approved, the project `AGENTS.md` forbids the planned action, or continuing would require guessing a product or technical decision.
