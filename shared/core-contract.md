# OPC Core Contract

Always loaded. Everything else loads on demand — see the Pack Index at the bottom.
Enforcement lives at the lowest possible layer: script/hook (L0) > structured artifact (L1) > this prose (L2).

## Status Tokens

Reviews end with exactly one line: `**Status:** Approved` or `**Status:** Issues Found`.
Implementers report exactly one of: `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `BLOCKED`.
Tokens are machine-parsed (`shared/scripts/parse_review_status.py`). Never translate, rephrase, or duplicate them.

## Evidence Before Claim

Never claim passed, fixed, verified, done, or releasable without fresh evidence from the current
code revision: command, exit code, report path, branch/commit. A subagent report alone is not
evidence — inspect the actual diff, test output, or runtime artifacts.

Every verification claim carries one authenticity label:
`mock passed` | `seeded passed` | `local real service passed` | `external provider passed` |
`human accepted` | `long-run passed` | `not run` | `pending` | `blocked`.
Never report a lower-realism label as a higher one. Missing environment does not block work;
it caps the achievable label, and the cap is reported honestly.

## Feedback Taxonomy

All human feedback, at any touchpoint, classifies as exactly one of:

- `tune` — same intent, different execution. Iterate inside the current phase. Free, unlimited, unrecorded.
- `revise` — an upstream artifact was wrong. Route to the earliest broken layer, mark every
  downstream artifact stale (freshness cascade), replay forward. Record in the ledger.
- `park` — stop this line of work. Record the decision, close out cleanly.

Acceptance failures additionally classify three ways before routing:
implementation defect (code ≠ artifact → fix code), artifact defect (code = artifact, artifact
wrong → `revise` upstream), taste change (artifact was right, intent moved → new increment, not rework).

## Freshness

A review is valid only for the exact content it reviewed. Reviews record `Reviewed-SHA` per
artifact (via `git hash-object`); `shared/scripts/check_freshness.py` verifies. Never trust mtimes.
Any `revise` invalidates downstream approvals automatically.

## Failure Philosophy

Fail open with a recorded gap: when an environment assumption is unmet (missing runbook, missing
service, no subagent support), degrade honestly — record the gap in the ledger, cap evidence labels
accordingly, and continue. Fail closed only for destructive or irreversible actions (deleting work,
force-push, production mutation, external publication) and for guessing product/technical decisions
that belong to the human.

## Ledger

Every gate outcome, rework routing, evidence label, resolved failure, and recorded gap appends one
JSON line to the feature ledger (`docs/features/<slug>/ledger.jsonl`) via `shared/scripts/opc_ledger.py`.
Resolved failures also append root-cause records to `docs/opc/error-ledger.jsonl`.
The ledger is the substrate for `retro`; unrecorded events are invisible to improvement.

## Language

Adapt conversational output and generated artifacts to the user's language. Normative suite text,
status tokens, ledger fields, and label vocabulary stay in English exactly as written.

## Isolation

Parallel implementers require worktrees; without worktrees, dispatch serially. Reviews run in fresh
subagents given the rubric and the artifact — never the creator's chat history, reasoning, or
desired outcome. If subagent isolation is unavailable, perform the gate inline with a cold restart
of context, record `self-reviewed (no isolation)` in the ledger, and surface it at the next human
touchpoint.

## Pack Index

Read a pack only when your current role needs it:

- `packs/gate-protocol.md` — running any review gate; freshness mechanics; convergence stop-loss.
- `packs/decision-protocol.md` — presenting decisions to the human; doors; decision-spikes.
- `packs/feedback-routing.md` — handling tune/revise/park in detail; stale cascade; acceptance triage.
- `packs/evidence.md` — evidence triangle; RED/GREEN fields; prohibited claims.
- `packs/tdd-implement.md` — dispatching implementers; status protocol; controller duties.
- `packs/mock-retirement.md` — prototype mock inventory and retirement lifecycle.
- `packs/risk-readiness.md` — risk categories, spikes, thin-slice gates.
- `packs/branch-worktree.md` — branch rules, worktree mechanics, destructive-op confirmation.
- `packs/harness-verbs.md` — run/reset/observe/drive standards; seed scenarios; E2E tiers.
