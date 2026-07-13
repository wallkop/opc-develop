# Verification

Standard `build` uses `packs/increment.md` and `opc_increment.py`; this pack summarizes the runtime
rules shared with release flows and explicit legacy artifacts.

## Prepare the real local surface

- Start through the production entry/runbook, not a test-only assembly.
- Reset to scratch state and import the declared seed or source-hashed snapshot.
- Apply local migrations/config under `release-ops.md`; back up shared data before DDL and require
  approval for destructive/one-way changes.
- Record build ID, origin, session/auth mode, scratch DB path, object IDs, and trace ID.

## Run by cost

1. targeted logic/build;
2. real local service + scratch DB;
3. approved testcase runner for UI/API E2E;
4. saved-provider replay;
5. one external-provider canary;
6. human acceptance.

Use targeted tests during debugging. Run the core journey at slice boundaries and final delivery,
not after every patch. Run the full regression only when slices integrate or final delivery needs
it. A canary failure caused by harness/DOM/seed/timing returns to offline layers before any repeat.

## Complete honestly

The generated acceptance receipt is the machine truth. `opc_increment.py check` must reach the
required level on the current content tree. Review findings, test counts, and prebuilt receipt
matrices cannot substitute for commands from this revision.
