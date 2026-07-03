# Gate Protocol

Every artifact gate follows the same anatomy, parameterized by a rubric file.

## Anatomy

1. **L0 precheck (scripts, before any subagent):**
   - `python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/validate_artifacts.py" <artifact>` — structure,
     required sections, AC-ID integrity.
   - `python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/check_freshness.py" <upstream-review>`
     (once per upstream review) — upstream approvals still fresh. Stale upstream ⇒ stop, route
     per `feedback-routing.md`.
   - Precheck failures return to the creator without spending a reviewer.
2. **Fresh reviewer subagent** — prefer the `opc-reviewer` agent (read-only by tool restriction);
   otherwise a fresh isolated subagent primed with
   `${CLAUDE_PLUGIN_ROOT}/shared/prompts/reviewer.md`. Context given: the rubric for this artifact type
   (`shared/rubrics/<type>.md`), the artifact itself, the upstream artifacts it must align with
   (or their AC index), the diff when reviewing code. Context withheld: creator chat history,
   creator reasoning, suspected issues, desired outcome, unrelated conversation.
3. **Review record** written to `docs/features/<slug>/reviews/<type>-review.md` (per-contract
   implementation reviews: `reviews/C-XX-implementation-review.md`):
   findings, per-AC verdicts where applicable, one status token, and one `Reviewed-SHA:` line per
   reviewed file (`git hash-object <file>`).
4. **Ledger entry** via `opc_ledger.py`: gate type, status, rounds, SHA.
5. **Routing.** `Issues Found` → creator fixes → targeted re-review of blocking issues and changed
   regions only. Full re-review only when main semantics changed.

## Stop-Loss

One counter, suite-wide: when the same blocking issue survives **2** repair rounds, stop. Write the
unresolved issue to the ledger and escalate: route `revise` upstream if the artifact is the problem,
or surface to the human if judgment is required. Nested loops (e.g. a failing test inside a review
round) inherit the outer counter; do not stack counters.

## Reviewer Conduct

- Judge the artifact against the rubric and upstream artifacts, not against effort or intent.
- Do not edit any artifact. Report findings; the creator fixes.
- Cite evidence (file, line, AC-ID) for every blocking finding.
- An empty findings list with `Issues Found`, or findings with `Approved`, is malformed — pick one.

## Degraded Mode

If the environment cannot start subagents: run the gate inline after a deliberate context reset
(re-read only rubric + artifact, set aside creator reasoning), record
`self-reviewed (no isolation)` in the review record and ledger, and flag it at the next human
touchpoint. Never silently skip a gate.
