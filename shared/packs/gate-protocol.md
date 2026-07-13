# Gate Protocol

Use one review protocol for standard-increment reviews and explicitly requested artifact gates.

## L0 before reviewer time

1. Resolve the target language from applicable project `AGENTS.md`.
2. Run `validate_artifacts.py` for the artifact. For a standard increment, validate
   `feature-plan.md`, run `opc_increment.py check`, and audit its ledger. Reality review uses the
   ordinary partial audit; final/ship uses `opc_ledger.py audit --require-increment-complete`.
3. Verify upstream review freshness when an opt-in artifact depends on another artifact.
4. Start one gate cost span. Close it only after the gate's initial review and repair rounds end.
5. Return mechanical failures to the creator without spending reviewer context.

## Reviewer isolation

Start one fresh reviewer with `fork_turns: none` or an equivalent empty context. Give only:

- the exact rubric;
- project rules;
- reviewed artifacts/plan and actual diff;
- acceptance receipt and command outputs;
- narrowly relevant upstream references.

Withhold creator chat history, reasoning, suspected bugs, desired verdict, other reviews, and
unrelated artifacts. Never run more than one reviewer concurrently with one implementer.

## Review record and chain of custody

The reviewer writes its own record under `docs/features/<slug>/reviews/` as its one permitted write.
For standard increments use `reality-review.md` and `final-review.md`; opt-in artifact gates keep
their named records. Include severity-ordered findings, concrete failure scenarios, exactly one
status token, and `Reviewed-SHA:` lines. Standard reviews also include `Reviewed-Revision:` from the
receipt. The final revision is the freshness gate; later slices may supersede the reality revision.

The controller never transcribes or repairs a verdict. It parses the record with
`parse_review_status.py`, compares it to the reviewer's returned status, verifies the actual diff
and command output, then closes the ledger span.

## Routing and convergence

The first pass returns the complete finding list; it must not drip-feed one new subsystem per round.
`Issues Found` routes to a targeted repair and re-review. The first review is round 1; increment the
round count for each re-review. Continue until the review passes or a genuine blocker requires user
input, external state, or redesign. There is no fixed repair-round quota and no predicted-effort
gate.

Record standard gates with `flow: increment-v1`, `gate: reality|final`, and a positive `rounds`
count. `opc_ledger.py audit` rejects duplicate or extra increment gates and verifies the ordered
review chain. A review object spanning unrelated user journeys or several major subsystems should
be decomposed when that makes findings actionable.

## Reviewer conduct

- Judge the requested real object and production assembly, not effort or claimed test counts.
- Check router mount, session/origin/auth, service construction, datastore, and runtime startup when
  relevant. “Targeted tests green” is not a production-assembly check.
- For UI, verify the approved testcase runner performs the Playwright action and emits atomic
  success/failure evidence. API-created success or raw Playwright cannot substitute.
- Check tests for direct-write controls that manufacture the asserted success.
- Cite file/line, receipt command ID, and a concrete failure scenario for blocking findings.
- Findings and status must agree. Style nits do not justify `Issues Found`.

## Degraded mode

If isolated reviewers are unavailable, deliberately clear creator reasoning, reread only rubric +
inputs, self-review, and record `self-reviewed (no isolation)`. Surface the missing separation to the
human; never present it as independent.

## Chain checks

`check_gate_chain.py` supports the standard two-review chain when `feature-plan.md` exists and the
legacy explicit artifact chain otherwise. `ship` also requires a fresh real-service acceptance
receipt; review freshness never substitutes for runtime evidence.
