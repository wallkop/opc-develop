---
name: harness
description: "Use to assess or build a project's harness — the run/reset/observe/drive capabilities that let agents work verifiably. Scores each verb by executing, not by reading docs; builds missing capabilities as executable scripts/seeds/log conventions with each verified by use; consumes gap entries from feature ledgers as its backlog. Replaces harness-init and harness-eval."
license: MIT
---

# harness

The harness is executable capability, not documentation. Docs index; scripts prove.

## Load

- `${CLAUDE_PLUGIN_ROOT}/shared/core-contract.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/packs/harness-verbs.md`
- `${CLAUDE_PLUGIN_ROOT}/shared/formats/report-style.md`

## Process

### Assess (default when asked to evaluate)

1. Score each verb 0-5 in 0.5 steps **by doing**: actually run the start command, actually reset
   and seed, actually trace one request through the logs, actually run one Tier-1 spec. A
   capability that exists only in a document scores as absent.
2. Anchors: 0 = verb impossible; 2 = possible with hand-discovery each time; 3.5 = documented and
   executable but gaps in coverage; 5 = one command, deterministic, agent-proven.
   Caps: never score `observe` ≥4 without correlation IDs reconstructing one action's chain;
   never score `drive` ≥4 without named seeds; never score any verb 4.5+ from plans or partial
   evidence; cap 3.5 overall when mocks/fixtures touch real secrets or production data.
3. Report per verb: score, evidence of what was executed, the label caps current gaps impose,
   and the top 3 highest-leverage builds. Write machine JSON/markdown truth and render/lint the
   same-basename plain-language HTML companion.

### Build (default when asked to initialize or improve)

4. Backlog = assessment gaps + `gap` entries read from the feature ledgers' JSONL directly
   (`opc_ledger.py summary` shows only counts).
   Order by label-cap impact: what blocks `local real service passed` claims comes first;
   `reset`/seed usually beats new tooling.
5. Build each capability as the executable thing itself — make targets, seed scripts with named
   scenarios, log configuration (four elements: JSON lines, correlation ID, fixed path, recipe in
   AGENTS.md), state-dump command, read-only DB recipe, Tier-1 spec scaffolding. Follow the L1-L4
   standards in `harness-verbs.md`.
6. Verify each build by using it once for real; record the command and output. Update AGENTS.md
   as the index pointing at everything built (keep it thin — pointers, not prose).
7. **L0 wiring is a default recommendation, not an afterthought**: propose project-local hooks
   or CI steps invoking `validate_artifacts.py`, `opc_increment.py check`, `opc_ledger.py audit`,
   `check_freshness.py`, and `check_gate_chain.py` at the appropriate gate points — "the gate and
   real core journey must happen" is the suite's most
   important rule and deserves its strongest layer. Install on the human's yes (hooks change the
   project's behavior for everyone); a decline is recorded as a `gap` with the enforcement
   downgrade it implies.

## Fail-open

Capabilities that need human-held access (production credentials, provider dashboards) become
documented handoff points, not fabricated capabilities. Building never blocks on scoring — a bare
repo starts at build step 5 with `run` and `reset`.

## Output

Assessment report with per-verb scores and evidence, and/or built capabilities each verified by
use, updated AGENTS.md index, closed `gap` entries.
