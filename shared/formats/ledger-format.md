# Ledger Format

Two append-only JSONL files. Write via `scripts/opc_ledger.py` (it validates shape and stamps
timestamps); never hand-edit past lines.

## Feature ledger — `docs/features/<slug>/ledger.jsonl`

Common fields: `ts` (stamped by script), `feature`, `type`.

```jsonl
{"type":"gate","gate":"prd","status":"Approved","rounds":2,"review":"reviews/prd-review.md","sha":{"prd.md":"ab12cd"},"isolation":"subagent"}
{"type":"rework","id":"RW-1","routed_to":"implementation","source":"acceptance","trigger":"AC-3 fail","note":"..."}
{"type":"gate","gate":"implementation","status":"Approved","rounds":1,"resolves":["RW-1"]}
{"type":"change","source":"acceptance","note":"taste change: ...","routed_to":"brainstorm"}
{"type":"evidence","ac":"AC-3","label":"local real service passed","evidence":"reports/e2e-0703.md"}
{"type":"decision","id":"TD-2","door":"two-way","decided_by":"agent","note":"..."}
{"type":"gap","verb":"observe","blocks":"correlation IDs missing","label_cap":"seeded passed"}
{"type":"dispatch","contract":"C-01","mode":"worktree|serial","isolation":"subagent|self-implemented (no isolation)"}
{"type":"release","stage":"deploy-test","result":"ok","evidence":"...","backup":"..."}
{"type":"park","note":"...","reason":"..."}
```

Conventions:

- `gate.isolation` is `subagent` normally, `self-reviewed (no isolation)` in degraded mode.
- Decision ids: `TD-n` for technical records, `PD-n` for PRD decision-sheet records,
  `RISK-PROFILE` for the brainstorm risk classification.
- Any entry may carry an optional `actor` field (e.g. `"actor":"pm"`, `"actor":"architect"`) —
  use it in multi-person features so `retro` can attribute rework routing by role.
- Any entry may carry optional cost fields `wall_secs` and `tokens_est` — record them on `gate`
  and `dispatch` entries when known; they are `retro`'s telemetry-independent cost baseline.
- `rework` entries carry an `id` (`RW-1`, `RW-2`, … per feature). A rework is **resolved** only
  by a later entry explicitly referencing it via `"resolves":["RW-1"]` (typically the fixing
  gate or evidence entry) — an unrelated Approved on the same layer does not close it. `ship`'s
  precheck enforces this.
- `release` stages — `ship`: `manifest` → `env-test` → `deploy-test` → `regression-test` →
  `acceptance-test`; `deploy`: `preflight` → `env-prod` → `deploy-prod` → `regression-prod` →
  `watch`. Both resume after the last `ok` stage; `preflight` always re-runs.

## Error ledger — `docs/opc/error-ledger.jsonl` (project-wide)

Appended when a failure is **resolved** (root cause known), from any of the five capture points:
debug resolution, gate rejection, acceptance rejection, mid-session human correction, retro mining.

```jsonl
{"ts":"...","feature":"7-export","symptom":"export time off by 8h",
 "tag":"stale-knowledge",
 "root_cause":"naive datetime; project stores UTC only",
 "pattern":"datetime.now() without tz",
 "files":["src/export/*"],"fix_ref":"<commit>","source":"acceptance","cost_rounds":3}
```

`tag` vocabulary (pick one): `env-assumption`, `api-misuse`, `stale-knowledge`,
`missing-project-rule`, `spec-gap`, `test-blindspot`, `taste-misjudgment`, `harness-gap`.

## Crystallized rules — `docs/opc/rules.md` (project-wide)

Written only by `retro` with human approval. Each rule records provenance and placement:

```
## R-7: Always pass tz to datetime constructors
Born from: error-ledger 2026-07-01, 2026-07-02 (2 recurrences, tag stale-knowledge)
Enforced at: L0 — lint rule `no-naive-datetime` (preferred) | L2 — AGENTS.md line
Status: active | retired <date> <reason>
```

Retirement review: rules that never fire for 8 weeks, and all rules after a model major-version
change, go back to the human as retirement candidates.
