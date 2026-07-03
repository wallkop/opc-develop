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
3. **Review record — chain of custody.** The **reviewer itself** writes
   `docs/features/<slug>/reviews/<type>-review.md` (per-contract implementation reviews:
   `reviews/C-XX-implementation-review.md`): findings, per-AC verdicts where applicable, one
   status token, and one `Reviewed-SHA:` line per reviewed file (`git hash-object <file>`).
   Writing its own review record is the one write the reviewer is allowed. The reviewer's final
   returned text also states the status token.
4. **Controller cross-check (no transcription).** The controller never writes or edits the
   review file. It runs `parse_review_status.py` on the file and compares the parsed token with
   the token in the reviewer's returned text — mismatch or missing file means the review did not
   happen; escalate, don't repair. Then ledger via `opc_ledger.py`: gate type, status, rounds, SHA.
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
touchpoint. In degraded mode the chain-of-custody separation is gone too — say so; do not present
a self-written review as reviewer-written. Never silently skip a gate.

## Chain Verification

"The gate happened" is itself L0-checkable:
`python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/check_gate_chain.py" docs/features/<slug>` verifies
every expected review record exists, parses to exactly one Approved, and is content-SHA fresh —
the full chain from requirement to e2e. `ship` and `deploy` prechecks run it; projects should
wire it (plus `validate_artifacts.py`) into hooks or CI per the `harness` skill's default wiring.
