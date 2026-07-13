# Rubric: testcase phase

Review `testcases.md` and compiled `testcases.json` against the live approved demo, approved PRD,
`formats/testcase-format.md`, and the proposed project runner. End with one `**Status:**` line and
`Reviewed-SHA:` lines for both testcase artifacts. The reviewer must exercise the demo and inspect
the named data; code reading alone is invalid.

## Blocking checks

1. **Dual prerequisite**: demo and PRD reviews are Approved, fresh, and cover their required files.
2. **Semantic fidelity**: Given/When/Then names the correct product object and matches both the demo
   interaction and PRD AC. A plausible but different object/journey is a false oracle and blocks.
3. **Human inspectability**: title, starting state, action, success/failure signals, durable result,
   safety conditions, and visible screenshots plan are understandable without reading test code.
4. **Coverage both ways**: every active AC maps to at least one TC; every TC maps to active ACs.
5. **Data truth**: named existing data resolves to a canonical isolated clone or allowed live/read-
   only source with a runtime hash. Synthetic data is explicitly synthetic and cannot support a
   compatibility claim about a named real object.
6. **Action origin**: UI cases use Playwright for the product action. API/DB setup may prepare Given
   state but never manufacture Then. Computer Use is a reasoned single-action fallback only.
7. **Atomic oracle**: success and failure observers are armed before the action; either signal ends
   the wait immediately. No model round-trip, arbitrary sleep, or retry loop sits between action and
   decisive observation.
8. **Evidence triangle**: interface, correlation-linked logs/traces, and read-only state assertions
   are independently specified, including the error path.
9. **Provider isolation**: stub/replay/live is explicit. Live provider calls have a stop-loss and are
   never the ordinary debug loop.
10. **Mechanical compilation**: `opc_testcase.py compile` is deterministic; `testcases.json` exactly
    reflects the Markdown and `opc_testcase.py check` succeeds.
11. **Runner boundary**: the project exposes a testcase entry such as `npm run case -- TC-1`; raw
    Playwright is hidden behind it and emits `opc-case-evidence-v1` with per-step results and hashes.
12. **Screenshot limit**: at most before, decisive signal, and final screenshots are human-facing;
    trace/video/log artifacts may remain detailed.

## Non-blocking

Prose polish, case ordering, report styling.
