# technical.md Format

Path: `docs/features/<slug>/technical.md`. One committed route, decision records first, detail in
the appendix. Owns: architecture layering, SaaS/infrastructure choices, public API contracts,
system boundaries, migration, security posture, runtime evidence strategy. Does NOT own ordinary
internal module design — keep that near the result-card slice or, when coordination contracts were
explicitly requested, in the owning packet.

## Structure

```
# Technical Design: <feature>

## Decision Records                   ← the human-facing part
TD-1: <title> [ONE-WAY|two-way]
  Context / Options / Decision / Consequences        ADR-style, compact
TD-2: ...
                                      Every contested choice (datastore, provider, queue, API
                                      shape, layering) is a numbered record. Datastore choices
                                      follow the project's existing baseline unless a record
                                      explicitly justifies divergence — divergence is [ONE-WAY].

## Public Contracts
API endpoints                         method, path, request/response shape, error envelope
Events / jobs                         names, payloads, delivery guarantees
Schema changes                        migrations forward + rollback note

## System Boundaries
                                      which components change, which are read-only, how this
                                      feature's slice fits the architecture's growth direction

## Runtime Evidence Plan
                                      per AC-cluster: which log events (with correlation ID),
                                      which DB assertions, which dump commands will prove behavior
                                      at verify time — written against harness-verbs.md L3

## Risk & Readiness
                                      spike results reference, thin-slice designation, per-risk
                                      readiness verdicts

## Appendix                           sequencing, capacity notes, security detail, alternatives
```

## Rules

- Localize every ordinary heading and prose block to the target language resolved from project
  `AGENTS.md`; keep TD/AC IDs, reversibility tags, commands, paths, and parser-required tokens
  unchanged. Template headings are semantic section names, not mandatory English display text.
- Exactly one committed route. Alternatives live in decision records' Options, not as parallel maybes.
- Every `[ONE-WAY]` record requires explicit human approval at the architecture sign-off touchpoint.
- Public contracts here are the single source of truth; impl-contracts reference, never redefine.
- The Runtime Evidence Plan is mandatory: a design that cannot say how it will be observed is not done.
