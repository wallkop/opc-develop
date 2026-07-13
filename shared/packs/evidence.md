# Evidence Pack

## Command receipt

Every verification records command argv, exit code, start/end time, working directory, output path
or excerpt, branch/commit, content-tree fingerprint, and authenticity label. Browser/runtime checks
also record the available build ID, origin, session type, scratch DB, core object IDs, screenshot or
artifact, and correlation/trace ID. Use `opc_increment.py` for standard increments so code, tests,
plan, seed, or tracked-config changes invalidate old results automatically.

## Runtime evidence

A `local real service passed` claim proves the production assembly, not just an isolated service:

1. interface evidence—browser assertion for UI, real HTTP/CLI/job result otherwise;
2. correlation-linked log/trace evidence for the route actually executed;
3. read-only state evidence for the durable result and safety invariants.

If the harness cannot expose a corner, record the gap and cap the label. Do not rerun expensive
checks merely to compensate for missing observability; route that gap to `harness`.

## RED/GREEN

When using TDD, record `RED:` command + relevant failing output before implementation and `GREEN:`
the same command + passing output after. Missing RED is test-after, not automatically a product
failure; label it honestly. Never delete working code just to recreate ceremonial RED.

## Data provenance

Distinguish synthetic seed, source-hashed read-only snapshot, and real object/provider. Report what
each can prove. If the requested journey concerns existing user data, only the allowed snapshot or
real object supports compatibility claims.

## Prohibited claims

Do not say passed/done/fixed/verified/ready when the command did not run, exit is unknown, evidence
path is missing, fingerprint is stale, a bypass created the result, or a lower-realism label is
presented as higher. Always state the exact completion level.
