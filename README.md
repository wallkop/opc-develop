# opc-develop

[简体中文](README.zh-CN.md)

opc-develop is a Claude Code / Codex skill suite for shipping one real user outcome inside an
explicit time budget. Its default path is now deliberately small: reach the production-assembled
core journey first, expand in runnable slices, and let fresh machine receipts—not test counts or
review prose—decide what is actually complete.

Version 0.5 replaces the former “specify everything, contract everything, review every contract,
then integrate” default with a budget-first standard increment. The full requirement/demo/PRD/
technical toolchain remains available when a lasting decision truly needs it, but it is opt-in.

![OPC Develop v0.5 budget-first workflow](assets/opc-develop-skills.png)

## Choose the smallest route

| Route | Use when | Process |
| --- | --- | --- |
| `vibe` | The human explicitly wants untested code and owns all acceptance | Edit immediately; no tests or verification |
| `lite` | One result, credibly <=60 minutes | Direct edit, focused regression, one real-entry check |
| `build` | One product increment, 1-4 hours; or a release-bound quick fix | One result card, one core journey, runnable slices, fresh receipt |
| split | >4 hours or several independently useful outcomes | Propose separately useful standard increments; implement the first only |

Risk adds only its matching protection. A migration adds snapshot/rollback checks; permission work
adds allow/deny checks; an external provider adds replay and one final canary. A risk label does not
automatically load every document and gate.

## The standard increment

```mermaid
flowchart LR
  A["Budget gate"] --> B["One-page result card"]
  B --> C["Core journey fails meaningfully"]
  C --> D["45-minute vertical slice"]
  D --> E["Reality review"]
  E --> F["30-90 minute runnable slices"]
  F --> G["Cheap-to-expensive verification"]
  G --> H["Final review"]
  H --> I["Fresh acceptance receipt"]
```

`build` creates only `docs/features/<slug>/feature-plan.md` by default. It records:

- the user's action, real entry point, visible success, and explicit non-goals;
- one core journey through real session/auth, production router/service assembly, scratch state,
  and the user-visible result;
- source provenance for synthetic, snapshot, or real data;
- two safety invariants;
- a first slice of at most 45 minutes and later slices of at most 90 minutes;
- build and core-journey acceptance commands.

For UI work, the browser must perform the accepted action. Creating a Run through an API and only
viewing it in the browser proves the API/read path, not the UI action.

## Verification without an expensive debug loop

Verification proceeds in cost/stability order:

1. logic/build;
2. local production service + scratch state;
3. browser core journey for UI;
4. saved-provider-response replay;
5. one real-provider canary;
6. human acceptance.

`shared/scripts/opc_increment.py` generates `acceptance.json` and binds command evidence to the
repository's current content tree. Changing code, tests, the plan, seed, or tracked configuration
automatically makes earlier results stale. Committing unchanged content does not. The receipt uses
canonical process-artifact exclusions, a hash-chained command history, and rehashes command logs and
runtime artifacts on every check; a later failed attempt supersedes an older pass in the same layer.

The helper reports exactly one highest completion level:

1. `code-build`
2. `automated-core-journey`
3. `real-service-core-journey`
4. `human-accepted`

A UI result cannot reach level 3 without a browser-driven key action through the production
assembly. Snapshot/real data must match the plan's source hash.

Real providers are locked until build/logic, the local real core journey, and offline replay pass on
the same revision. One provider attempt is allowed per revision; a reasoned override exists for
exceptional recovery, not for repeatedly debugging harness, DOM, seed, or timing failures.

## Reviews that stop

A standard increment has only two review moments:

1. reality review after the first vertical slice;
2. final integration review.

The first pass must return the complete severity-ordered finding list. Across both reviews, at most
two repair rounds are allowed. Remaining blockers force scope reduction or redesign. Reviewers start
with empty context and receive only the rubric, plan, diff, receipt, project rules, and commands;
copying the full creator conversation is forbidden.

`opc_ledger.py audit` mechanically rejects extra increment gates, more than two total repairs, and
dispatch records using full conversation context.

## Optional decision tools

These skills no longer sit on the default path and are disabled for implicit invocation:

- `brainstorm` when product intent genuinely needs a decision interview;
- `demo` when interaction taste needs an experienceable prototype;
- `prd` when durable product/state/permission decisions or a PM handoff justify one;
- `architect` when a public boundary or one-way technical decision changes.

If used, their artifacts remain SHA-fresh and structurally validated. `testcases.md` now has real L0
validation: level, named seed, Given/When/Then, bidirectional AC coverage, and a browser action for
`ui-e2e`. Standard `build` does not pre-author every future executable skeleton; it adds the most
valuable regression with each completed slice.

When optional PRD/technical records or a demo mock inventory exist, the result card maps in-scope
`AC-n`/`TD-n` constraints and every `M-n` retirement to a slice and proof. Final review checks the
implementation against those mappings; optional does not mean ignored.

## Skills

| Skill | Purpose |
| --- | --- |
| `vibe` | Fastest unverified implementation with human-only acceptance |
| `lite` | One <=60-minute change, focused test, real-entry check |
| `build` | One 1-4 hour standard increment through a real core journey |
| `ship` | Test-environment deployment, core-journey regression, human acceptance, merge |
| `deploy` | Fail-closed production release with rollback and watch window |
| `oncall` | Evidence-led incident diagnosis, rollback/hotfix/mitigation |
| `harness` | Execute and improve run/reset/observe/drive capabilities |
| `retro` | Audit measured cost/data quality and verify process changes |
| `brainstorm` | Optional durable product-intent interview |
| `demo` | Optional taste prototype in the real application shell |
| `prd` | Optional durable product contract and black-box case catalog |
| `architect` | Optional public-boundary/one-way technical design |

## Machine guardrails

All helpers use the Python standard library.

```bash
# Validate the one-page result card
python3 shared/scripts/validate_artifacts.py docs/features/<slug>/feature-plan.md

# Initialize and record revision-bound evidence
python3 shared/scripts/opc_increment.py init \
  --plan docs/features/<slug>/feature-plan.md \
  --receipt docs/features/<slug>/acceptance.json

python3 shared/scripts/opc_increment.py run \
  --receipt docs/features/<slug>/acceptance.json \
  --kind build --label "seeded passed" -- <build command>

python3 shared/scripts/opc_increment.py check \
  --receipt docs/features/<slug>/acceptance.json \
  --require real-service-core-journey

# Validate explicit PRD test cases and the review/ledger chain
python3 shared/scripts/validate_artifacts.py docs/features/<slug>/testcases.md \
  --prd docs/features/<slug>/prd.md
python3 shared/scripts/check_gate_chain.py docs/features/<slug>
python3 shared/scripts/opc_ledger.py audit --require-increment-complete \
  --ledger docs/features/<slug>/ledger.jsonl
```

The suite still includes executable benchmark cases, automatic wall/token cost spans when the host
exposes usage, source-hash review freshness, human-readable HTML report rendering, error-ledger
recurrence mining, and run/reset/observe/drive harness evaluation.

For a multi-increment production release, `deploy` first fixes the release set, then refreshes each
receipt once on the final combined trunk and obtains the human verdict again. This is intentional:
a later merge must not leave an earlier whole-tree claim silently green.

## Installation

### Codex

```bash
codex plugin marketplace add wallkop/opc-develop --ref main
codex plugin add opc-develop@opc-develop
```

For local development:

```bash
git clone https://github.com/wallkop/opc-develop.git ~/plugins/opc-develop
```

### Claude Code

```bash
claude --plugin-dir ~/plugins/opc-develop
```

Invoke skills through the plugin namespace, for example `/opc-develop:build` or
`/opc-develop:lite`. See [docs/claude-code.md](docs/claude-code.md) for marketplace setup.

## Development and validation

```bash
python3 shared/scripts/test_opc_scripts.py
python3 shared/scripts/opc_benchmark.py validate shared/fixtures/opc-benchmark/registry.json
python3 shared/scripts/opc_benchmark.py run shared/fixtures/opc-benchmark/registry.json --repo .
```

Repository structure:

- `skills/` — user-facing workflows;
- `shared/core-contract.md` — budget, evidence, completion, review, context, and language rules;
- `shared/packs/` — on-demand workflow rules;
- `shared/formats/` — result card, receipt, PRD/technical/testcase, and ledger formats;
- `shared/rubrics/` — complete reviewer checklists;
- `shared/scripts/` — deterministic L0 checks and receipts;
- `agents/` and `shared/prompts/` — cold-context reviewer/exceptional implementer roles.

## Safety and language

Applicable project `AGENTS.md` target-language rules govern conversation, artifacts, reviews, and
reports; parser-required keys/tokens remain stable. Never place project business data, credentials,
private logs, `.env` files, or generated feature artifacts in this plugin repository.

Destructive actions, production mutations, permission/security changes, irreversible schema/data
work, force pushes, and external publication always require explicit human approval.

## License

MIT
