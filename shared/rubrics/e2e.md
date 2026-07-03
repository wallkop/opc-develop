# Rubric: E2E & acceptance readiness

You are reviewing the verify stage's output: Tier-1 specs, the acceptance sheet
(`docs/features/<slug>/acceptance.md`), and evidence. Inputs: prd.md (AC list), the spec files,
test run outputs, the feature ledger's evidence entries. End with one `**Status:**` line and
`Reviewed-SHA:` lines for the acceptance sheet and spec files.

## Blocking checks

1. **AC coverage**: every non-struck AC has ≥1 Tier-1 spec or a recorded, human-visible gap entry.
   Coverage claims are verified by reading spec annotations, not the report.
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
