# Acceptance Receipt Format

Path: `docs/features/<slug>/acceptance.json`. Generate it with `opc_increment.py`; never hand-edit
it. The receipt is bound to the repository's current content tree, so committing unchanged content
does not invalidate evidence, while any code, test, plan, seed, or tracked configuration change
does. `init` refuses to overwrite an existing receipt so command history and provider-attempt
stop-loss cannot be reset accidentally; reuse the existing file. All read-modify-write commands
hold a per-receipt interprocess lock, so concurrent runs cannot duplicate a provider canary or lose
command history.

## Commands

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" init \
  --plan docs/features/<slug>/feature-plan.md \
  --receipt docs/features/<slug>/acceptance.json

python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" run \
  --receipt docs/features/<slug>/acceptance.json \
  --kind build --label "seeded passed" -- <build command>

python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" run \
  --receipt docs/features/<slug>/acceptance.json \
  --kind browser --core --case-id TC-1 \
  --case-evidence .git/opc-evidence/<run>/case-evidence.json -- \
  python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_testcase.py" run \
    --feature-dir docs/features/<slug> --case TC-1 \
    --evidence .git/opc-evidence/<run>/case-evidence.json -- \
    npm run case -- TC-1

python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" check \
  --receipt docs/features/<slug>/acceptance.json \
  --require real-service-core-journey
```

The helper records command argv, working directory, time, exit code, output, commit, content-tree
fingerprint, runner-derived authenticity label, evidence axes, build/runtime metadata, object IDs,
trace ID, artifact hashes, output-log hash, and whether the command mutated the worktree. Browser,
core, and provider commands require an approved case and fresh `opc-case-evidence-v1`; the runner,
not CLI flags, supplies assembly/data/provider/driver/observation facts. The helper rehashes those
files during every check. The receipt, review records, ledger, human
reports, and release manifest are excluded from the product fingerprint so recording process
evidence does not invalidate the code it proves; matching process records for other features are
excluded too. The plan remains included. Store generated logs/artifacts under `.git/opc-evidence`
or pass stable in-repository paths; do not record secrets.

The receipt proves command history, manifest identity, evidence structure, artifact integrity,
ordering, and freshness. It still cannot make a malicious project runner trustworthy; the
independent reality/final reviewer inspects runner code and artifacts against production assembly.

## Completion levels

1. `code-build`
2. `automated-core-journey`
3. `real-service-core-journey`
4. `human-accepted`

UI level 3 requires the approved case's Playwright action through production assembly, complete
interface/log/state observations, and canonical-clone/live-real data matching the plan `Data-Hash`.
A direct API-created result or synthetic lookalike cannot stand in for that claim.

Record level 4 only after the human accepts the fresh level-3 result:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" accept \
  --receipt docs/features/<slug>/acceptance.json --actor <name-or-role>
```

## Provider stop-loss

`kind=provider` stays locked until a cheap build/logic check, the local real core journey, and an
offline replay all pass on the same revision. One provider attempt is allowed per revision. A
repeat requires an explicit reasoned override; never use the override to keep debugging a harness,
DOM, seed, or timing failure.
