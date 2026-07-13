# Optional rubric: owner handoff implementation

Use only when an explicit coordination handoff warrants its own owner review; ordinary increments
use the reality/final rubric instead. Inputs: the contract file, the actual
diff, test files and outputs, the implementer's report (as claims to verify, not truth). One pass
covers both compliance and quality. End with one `**Status:**` line and `Reviewed-SHA:` for the
contract file.

## Compliance (blocking)

1. **Boundary respected**: diff touches only allowed paths. Any forbidden-path change ⇒ Issues
   Found regardless of quality.
2. **ACs actually implemented**: for each owned AC, find the code and the test that proves it.
   The report saying so is not finding it.
3. **Regression evidence**: the workstream's named seed/regression has honest failing or baseline
   evidence and a fresh pass. Missing historical RED is labeled test-after, not an automatic block
   unless the risk/rubric requires it.
4. **Tests are honest**: assertions test behavior, not implementation echoes; no tests that pass
   vacuously; no weakened/deleted existing tests without justification.
5. **Mock retirement**: each assigned M-x is gone from production paths — verify by grep/reading,
   not by report. Residuals ⇒ Issues Found.
6. **Public contract fidelity**: API shapes match technical.md exactly.

## Quality (blocking only when risk-triggered)

Give explicit attention when the diff touches: security surfaces, migrations/data, concurrency,
money, permissions, deletion paths. There: injection/authz gaps, unsafe migrations, race windows,
missing idempotency, secret leakage are blocking. Elsewhere: significant duplication, dead code,
and error-swallowing are findings; style nits are not.

## Conduct

Do not edit code. Cite file:line per finding. Verify at least one AC end-to-end by running its
test yourself when commands are available; record the command and exit code in the review.
