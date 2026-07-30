# Submission Copy

## Short description

Human-approved black-box semantics for Codex and Claude Code: fast bounded Lite delivery,
engineering-depth Build routing, executable testcase manifests, and runner-derived evidence.

## Medium description

opc-develop defaults bounded work through existing architecture to `lite`, including localized
behavior changes. `build` is reserved for complete new capabilities, shared-core refactors,
breaking evolution, broad regression surfaces, or coordinated rollouts, and follows
`demo -> prd -> testcase -> build`. Risk adds matching protection instead of process ceremony.

## Long description

opc-develop is an opinionated, project-agnostic workflow suite for builders who personally own
product and engineering judgment. Version 0.6 separates testcase from PRD and requires approved
demo, PRD, and testcase artifacts before a standard or releasable build.

The route is selected by engineering depth and change radius: `vibe` for explicitly human-accepted
unverified code, `lite` by default for bounded changes through existing architecture, and `build`
only for an explicitly named structural trigger. Behavior, billing, permissions, providers, APIs,
databases, and release intent are not Build triggers by themselves. Predicted duration never routes
or blocks a request. Risk adds only its matching protection—migration snapshot/rollback,
permission allow/deny, money/idempotency/rollback, concurrency checks, or provider replay/canary.

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
