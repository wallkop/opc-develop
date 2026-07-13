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
  --kind browser --label "local real service passed" \
  --core --browser-action --production-assembly --data-hash <plan-hash> \
  --origin <origin> --session-type <session> --scratch-db <path> \
  --object-id <durable-result-id> --trace-id <id> \
  --artifact .git/opc-evidence/<screenshot-or-report> -- <browser journey command>

python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/opc_increment.py" check \
  --receipt docs/features/<slug>/acceptance.json \
  --require real-service-core-journey
```

The helper records command argv, working directory, start/end time, exit code, output path and
excerpt, commit, content-tree fingerprint, authenticity label, build/runtime metadata, object IDs,
trace ID, artifact hashes, output-log hash, and whether the command mutated the worktree. Level-3
core evidence and provider canaries require origin, session type, object ID, trace ID, and an
in-repository artifact created or updated by that command; core evidence also requires
scratch-state metadata. The helper rehashes those files during every check. The receipt, review records, ledger, human
reports, and release manifest are excluded from the product fingerprint so recording process
evidence does not invalidate the code it proves; matching process records for other features are
excluded too. The plan remains included. Store generated logs/artifacts under `.git/opc-evidence`
or pass stable in-repository paths; do not record secrets.

The receipt proves command history, metadata presence, artifact integrity, ordering, and freshness;
it does not semantically prove that an arbitrary executable truly controlled a browser or contacted
a provider. The independent reality/final reviewer must inspect the command and artifacts against
the production assembly before approving the claim.

## Completion levels

1. `code-build`
2. `automated-core-journey`
3. `real-service-core-journey`
4. `human-accepted`

UI level 3 requires the key action to be browser-driven through the production assembly. A direct
API-created result cannot stand in for the UI action. Snapshot/real data must match the plan's
`Data-Hash`.

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
