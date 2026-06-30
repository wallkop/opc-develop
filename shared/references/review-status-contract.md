# Review Status Contract

Every review report must contain exactly one status line:

```markdown
**Status:** Approved
```

or:

```markdown
**Status:** Issues Found
```

Reviewers must not edit product, technical, spec, plan, testcase, or code artifacts. A review with `Issues Found` must list only blocking issues that can make implementation, testing, acceptance, or release wrong. Advisory notes may be included after blocking issues, but advisory notes do not block the gate.

Keep the exact English status token for parser compatibility. Write review body, issue explanations, and advisory notes primarily in Simplified Chinese unless the user explicitly requests another language.

A downstream skill must not run unless every required upstream review file exists and its status is `Approved`.

## Blocking vs Advisory

Use blocking issues only for defects that affect correctness, buildability, testability, acceptance, release safety, security, data integrity, or project-rule compliance.

Use advisory notes for style, optional refactors, wording improvements, or non-essential polish. Advisory notes must not force a creator/reviewer loop.

## Creator Response Rules

Creators must not blindly apply a review issue when doing so would conflict with an upstream Approved artifact. Route the issue to the earliest affected layer, or ask for human decision when the conflict is a real product or technical choice.

If the same blocking issue fails to converge after repeated creator/reviewer loops, record the unresolved issue in `progress.md`, identify the conflicting artifacts or decisions, and request human arbitration instead of continuing the loop indefinitely.

Use `review-trigger-policy.md` to choose full vs targeted review scope. After a creator revision, the matching review must still be fresh, but it should be targeted to the previous blocking issues and changed regions unless the revision changes the artifact's main semantics.

## Review Subagent Isolation

Every `review-*` skill must be performed by a fresh, dedicated review subagent. The main controller must not perform the review inline in its existing conversation context.

When the environment provides named review agents, use the OPC artifact reviewer role for these review gates. If no named role exists, use the environment's native isolated subagent mechanism with the relevant reviewer prompt.

The controller must provide the review subagent only the minimum necessary alignment context:

1. The artifact under review.
2. Required upstream approved artifacts and original requirement needed for comparison.
3. Applicable project rules from `AGENTS.md` and required technical docs when the specific review needs them.
4. The relevant reviewer prompt and this review status contract.

The controller must not provide creator chat history, private reasoning, suspected conclusions, desired approval outcome, intended fix, or unrelated conversation context. The review subagent must be fair and independent: treat the artifact as unverified, compare only against the supplied inputs, and approve only when the gate is genuinely satisfied.

If the current environment cannot start a separate review subagent, the `review-*` skill must block and report that isolated review execution is unavailable. Do not downgrade to an inline self-review.

The review report must be authored by the review subagent. The controller may write the report file exactly from the subagent result, but must not alter the subagent's status or weaken blocking issues.

## Review Freshness

A review is valid only for the exact artifact revision it reviewed. If a creator skill changes an artifact after its matching review was written, that review becomes stale even when it still says `Approved`.

Creator/reviewer loops must follow this rule:

1. Run the creator skill.
2. Run the matching reviewer skill.
3. If the reviewer returns `Issues Found`, run the creator skill again with only the blocking findings and necessary context as required revision input.
4. After every creator revision, immediately run the matching reviewer again; default to targeted fresh review unless the change requires full review.
5. Proceed only when the latest matching review exists, has exactly one `**Status:** Approved` line, and is newer than or equal to every artifact file it reviews.

Downstream skills must block when a required upstream review is missing, not Approved, or stale relative to the reviewed artifact. Do not treat an Approved review written before the latest artifact change as a passed gate.

Freshness pairs:

- `demo/` -> `reviews/demo-review.md`
- `prd.md` -> `reviews/prd-review.md`
- `technical.md` -> `reviews/technical-review.md`
- `spec.md` -> `reviews/spec-review.md`
- `testcases.md` and real testcase files -> `reviews/testcase-review.md`
- `plan/*.md` and `plan/integration-plan.md` -> `reviews/plan-review.md`
