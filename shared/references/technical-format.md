# Technical Design Format

`technical.md` is feature-specific. Global architecture and durable standards belong under `docs/technical/`.

It is for human architecture review. It must explain and commit to the macro technical decisions that downstream AI implementers are not allowed to change.

## Must Cover

- Relevant existing modules and current behavior.
- One explicit technical approach and rationale. Do not leave multiple viable approaches open.
- Chosen technical components. SaaS / infrastructure components such as datastore/database, cache, queue, object/blob storage, external APIs, model providers, auth services, and audit services must be decided here.
- If a new or changed datastore/database is involved, it must follow project rules, existing architecture facts, or an explicit human-approved decision. If no baseline exists or facts conflict, block for human architecture review instead of inventing a default.
- Public API input/output contracts: endpoint, method, request schema, response schema, status code, error code, auth/permission boundary, and external dependency failure semantics.
- UI, data, storage, and state impacts at architecture level.
- Demo-to-implementation mapping for UI-facing work: production components, routes, state owners, and any technical constraints that require approved demo deviations.
- Compatibility and migration requirements.
- Security and permission boundaries.
- Performance and operational impact.
- Runtime evidence plan: Log, DB, Trace.
- Merge gate, release gate, and external blocker classification when relevant.
- Risks and blocking decisions.

## Boundary With Spec

`technical.md` owns:

- chosen architecture and component decisions
- public API contracts
- SaaS / infrastructure component contracts
- module boundaries and ownership at architecture level
- migration, compatibility, rollback, and operational strategy
- Runtime evidence strategy
- risks and high-impact unknowns

`technical.md` must not become a line-by-line implementation contract. Internal module placement, local component details, state machines, internal error mappings, acceptance mapping, and TDD seed lists belong in `spec.md`.

Do not present multiple unresolved choices. Mark high-impact unknowns as blockers instead of guessing, and request a human architecture decision.

For UI-facing features, technical design must not merely say "match the demo". It must identify the real frontend modules/components responsible for the demo's layout, interactions, and states, plus any implementation constraints that must be reflected back into PRD/spec before coding.

See `artifact-boundary-contract.md` for the full technical/spec/plan boundary.
