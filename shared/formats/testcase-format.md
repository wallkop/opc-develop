# Testcase Phase Format

The testcase phase is mandatory before `build`. It may start only after both the running demo and
the PRD have fresh Approved reviews. Product truth lives in
`docs/features/<slug>/testcases.md`; `opc_testcase.py compile` deterministically produces the
machine contract `testcases.json`. The two artifacts are reviewed together and then explicitly
accepted by the product owner in `testcase-approval.json`.

Keep parser fields and IDs unchanged; localize ordinary prose according to project rules.

```md
# Test Cases: <feature>

## Coverage Map
| AC | Cases |
| --- | --- |
| AC-1 | TC-1, TC-4 |

## Cases
### TC-1: <title> [level: api|ui-e2e] [seed: seed:<name>] [AC-1, AC-7]
Given <traceable starting world>
When <external user action>
Driver-Action: playwright | <one atomic click/type/upload>   # ui-e2e primary driver
Then <observable result and durable state>
Success-Signal: <positive UI/API signal that ends the wait>
Failure-Signal: <error UI/API/log signal that ends the wait immediately>
Data-Provenance: canonical-clone | <source selector or object>  # enum: synthetic/canonical-clone/live-real
Provider-Mode: stub  # enum: none/stub/replay/live
Observe: interface | <assertion + artifact>
Observe: logs | <correlation-linked event/trace assertion>
Observe: state | <read-only durable-state and safety assertion>
Fallback: computer-use | atomic-only
```

Rules:

- Every active AC maps to at least one case and every case maps to existing ACs. IDs are append-only.
- Cases are written only after the approved demo makes the experience concrete and the approved
  PRD defines durable truth. The demo answers “what should this feel like”; the PRD answers “what
  must remain true”; the testcase answers “what exact external experiment proves it.”
- The product owner reviews `reports/testcases.md/.html`, including the exact Given/When/Then,
  success/failure oracles, named object/data source, and screenshot limit. AI must not approve on
  the human's behalf.
- UI regression uses Playwright as the deterministic primary driver. Computer Use is advisory and
  may replace only one atomic action when a selector/browser limitation is recorded; it never owns
  waits, assertions, loops, or the release gate.
- API cases use `Driver-Action: api | <request>` against the real running interface.
- `opc_testcase.py compile` validates AC coverage and creates `testcases.json`; a fresh reviewer
  records `reviews/testcase-review.md`; `opc_testcase.py approve` records explicit product approval.
- Project E2E commands expose a testcase runner such as `npm run case -- TC-1`. Raw
  `playwright test ...` is an implementation detail behind that runner and is never a downstream
  acceptance command.
- The runner must pre-arm success/failure observers before the action and emit
  `opc-case-evidence-v1` with independent assembly, data, provider, driver, observation, and
  product-outcome axes. It may never infer “real passed” from CLI flags.
- Human review receives at most three screenshots per case (before, decisive signal, final). Trace,
  video, logs, and machine artifacts may be more detailed.
