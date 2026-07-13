# Rubric: E2E & acceptance readiness

You are reviewing the build/verify output: project testcase-runner adapters, the generated
acceptance receipt, and evidence. Inputs: approved `testcases.md` + `testcases.json`, runner code,
test run outputs, and feature-ledger evidence entries. End with one
`**Status:**` line and `Reviewed-SHA:` lines for the acceptance sheet and spec files.

## Blocking checks

1. **AC coverage through the chain**: every non-struck AC traces AC → approved TC → green runner case, or
   carries a recorded, human-visible gap entry. Coverage claims are verified by reading spec
   annotations, not the report.
1b. **Manifest provenance**: every E2E run names an approved case and current manifest SHA. Direct
   raw Playwright runs, unapproved cases, or hand-copied expectations cannot stand in for a TC.
2. **Seed declarations**: every spec declares its named seed scenario; specs that depend on
   leftover state from other specs ⇒ reject (non-deterministic).
3. **Evidence triangle**: each `local real service passed` or higher claim has all three corners
   (UI/interface assertion, correlation-ID log chain, state assertion) or is downgraded to the
   label its corners support. Check the evidence paths exist.
4. **Label honesty**: no claim exceeds the harness's label cap; gaps recorded in the ledger match
   the caps claimed. A `mock passed` result presented in the acceptance report without its label ⇒
   reject.
5. **Demo parity**: contractual demo interactions (per PRD Demo alignment) behave equivalently in
   the real implementation — exercise at least the core path yourself.
6. **Distillation rule**: agentic verifications marked "important" in the report have a
   corresponding committed Tier-1 spec. Exploration without distillation is a finding.
7. **Regression**: the pre-existing Tier-1 suite still passes; check the run output, exit code,
   and that the run postdates the last code change.

## Non-blocking

Spec style, report formatting, screenshot quality.
