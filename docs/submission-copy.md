# Submission Copy

## Short description

Human-approved black-box semantics for Codex and Claude Code: executable testcase manifests,
runner-derived evidence, semantics-routed increments, and convergent reviews.

## Medium description

opc-develop makes product test semantics visible before implementation. Small changes that reuse
existing semantics use `lite`; standard/releasable increments follow
`demo -> prd -> testcase -> build`. The human approves the prototype, durable AC truth, and exact
Given/When/Then cases; a deterministic manifest drives Playwright and structured evidence. Builds
route by changed product semantics and risk, reach a real vertical path, and do not enforce effort
estimates or fixed repair quotas.

## Long description

opc-develop is an opinionated, project-agnostic workflow suite for builders who personally own
product and engineering judgment. Version 0.6 separates testcase from PRD and requires approved
demo, PRD, and testcase artifacts before a standard or releasable build.

The route is selected by semantics and risk: `vibe` for explicitly human-accepted unverified code,
`lite` for localized changes that do not create or change E2E semantics, and `build` for approved
new/changed behavior or release-bound work. Predicted duration never routes or blocks a request.
Risk adds only its matching protection—migration snapshot/rollback, permission allow/deny,
concurrency/idempotency, or provider replay/canary.

`testcase` compiles `testcases.md` into deterministic `testcases.json` only after fresh demo/PRD
approval, then requires independent review and explicit product-owner approval. `build` selects an
approved Core-Case and reaches the first real vertical path. UI uses Playwright as the
primary driver; Computer Use is limited to a reasoned atomic fallback.

The standard-library helpers record commands, exits, output, commit, fingerprints, object IDs,
traces, and artifacts. E2E runners emit separate assembly, data, provider, driver, observation, and
product-outcome axes; authenticity labels are derived rather than supplied by CLI flags.
Code/test/plan/seed/config changes make old evidence stale. External providers stay locked until
offline layers pass and allow one canary attempt per revision. Completion is reported as code build,
automated core journey, real-service core journey, or human accepted.

Independent reviewers start with empty context and receive only the rubric, plan, diff, receipt,
project rules, and commands. A reality review follows the first slice and a final integration review
follows the scoped work. Repairs continue until approval or a genuine blocker; ledger validation
rejects invalid review chains and full-conversation task dispatch.

`brainstorm` remains optional before the mandatory product-definition chain; `architect` remains
conditional after testcase for public contracts or one-way technical decisions. Harness,
ship, deploy, oncall, retro, executable incident benchmarks, SHA freshness, HTML reports, and
language-adaptive output complete the suite.

## Suggested catalog tags

`product-development`, `coding`, `acceptance-testing`, `browser-e2e`, `tdd`, `workflow`,
`loop-engineering`, `harness`, `release-safety`, `codex`, `claude-code`

## Submission notes

Submit one suite-level listing linked to `https://github.com/wallkop/opc-develop`. The 13 skills
share repository-level packs, formats, rubrics, and scripts; verify that a catalog preserves those
shared resources rather than installing isolated skill folders.
