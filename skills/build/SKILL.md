---
name: build
description: "Use after the architecture sign-off to complete everything local in one run: partition the work into gated implementation contracts, author the failing Tier-1 acceptance skeletons from testcases.md before any implementation, implement via TDD implementer subagents with RED/GREEN evidence and mock retirement, apply migrations/config to the local or shared dev environment, deploy locally, and turn the skeletons green under the full black-box regression with evidence triangles — ending with a gated acceptance sheet ready for ship. Also the re-entry point for fixing code defects rejected at test acceptance."
license: MIT
---

# build

Everything that can be finished on the builder's machine, finished in one invocation:
contract → implement → locally deploy → verify. No human touchpoint; the output is evidence.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/contracting.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/tdd-implement.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/verification.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/evidence.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/branch-worktree.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/mock-retirement.md`
- For gates: `packs/gate-protocol.md` + `rubrics/impl-contract.md`, `rubrics/implementation.md`,
  `rubrics/e2e.md`
- Implementer prompt: `${CLAUDE_PLUGIN_ROOT}/shared/prompts/implementer.md`

## Phase A — Contract (skipped when fresh)

1. Precheck PRD/technical gate freshness. If `contracts/` is missing or stale, partition and
   gate the contract tree per `contracting.md`. Readiness blockers from `risk-spike.md` stop
   only the affected contracts.
2. Author the Tier-1 skeletons per `contracting.md`: every TC in testcases.md becomes a
   committed, currently-failing black-box spec **before any implementer is dispatched**. Capture
   the failing run (acceptance RED). Contracts and skeletons pass the same gate together.

## Phase B — Implement

3. Dispatch mode per `tdd-implement.md`: parallel ⇒ one worktree per implementer; else serial.
   Ledger `dispatch` entries.
4. Dispatch implementers (prefer `opc-implementer`; else isolated subagent with
   `prompts/implementer.md`) with paths and section pointers, not pasted documents.
5. Per completed contract: verify the report against reality (diff, tests, RED/GREEN fields),
   run the merged review gate (`rubrics/implementation.md`). Blocking issues → implementer →
   targeted re-review; 2-round stop-loss.
6. Failures with unclear cause get debugging discipline; resolved root causes append to the
   error ledger — resolution time is capture time. P0/P1, false-green, irreversible-risk, and
   recurring failures also link a project benchmark case (or a human-approved waiver) before the
   affected gate can be considered closed.
7. Integration steps from the contract index — including every `api`-level boundary skeleton the
   index names — then the final mock-residual audit when any prototype mock existed.

## Phase C — Local verify

8. Local deploy per `verification.md`: stack up, reset + seed, apply this feature's
   migrations/DDL and config to the local/shared dev environment under `release-ops.md` safety
   rules (backup before DDL on shared data; destructive changes need human confirmation).
9. Run the pre-authored Tier-1 suite — the Phase A skeletons turning green is the feature's
   primary acceptance signal. Per AC, assemble evidence triangles. Then the agentic pass becomes
   a gap hunt: explore beyond the cases, check demo parity, and distill only newly discovered
   behavior into additional `explored` Tier-1 specs.
10. Write the acceptance sheet (`acceptance.md`) and gate the phase (`rubrics/e2e.md`).

## Re-entry (fix mode)

When `ship`'s test acceptance rejects with implementation defects: re-enter here with the
rejection notes. Scope to the affected contracts/ACs — targeted fixes, targeted re-review,
re-run the affected Tier-1 specs plus regression, refresh the acceptance sheet. `ship` then
resumes from its deploy stage. Artifact defects and new needs do not enter build — they route to
`prd`/`architect` (revise) or `brainstorm` (change) per `feedback-routing.md`.

## Fail-open

No subagent support: degrade per `tdd-implement.md` with `self-implemented (no isolation)`
labels. Missing runbooks/commands: discover, record `gap`, continue. Shared-infra destructive
changes are the fail-closed exception.

## Output

Implemented feature with tests, contract tree, per-contract review records, mock residual audit,
committed Tier-1 specs (Phase A skeletons turned green + `explored` additions), gated
`acceptance.md`, ledger trail. Next: `ship`.
