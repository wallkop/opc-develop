# Submission Copy

## Short description

Budget-first product development for Codex and Claude Code: one real core journey, runnable slices,
revision-bound evidence, and reviews that stop.

## Medium description

opc-develop helps solo builders ship one real user outcome inside an explicit time budget. Small
changes use `lite`; 1-4 hour features use `build`; larger work is split before implementation. A
standard increment keeps one page of planning, reaches a production-assembled core journey within
45 minutes, expands in runnable slices, verifies from cheap logic checks to browser and one final
provider canary, and records a content-tree-bound acceptance receipt. UI completion requires the
browser to perform the key action. Two review moments share a hard two-repair stop-loss.

## Long description

opc-develop is an opinionated, project-agnostic workflow suite for builders who personally own
product and engineering judgment. Version 0.5 makes the standard increment the default instead of
front-loading a complete requirement/demo/PRD/technical/contract/test matrix.

The route is selected by elapsed-time budget: `vibe` for explicitly human-accepted unverified code,
`lite` for one <=60-minute change, `build` for one 1-4 hour increment, and split for anything larger.
Risk adds only its matching protection—migration snapshot/rollback, permission allow/deny,
concurrency/idempotency, or provider replay/canary.

`build` creates a one-page result card with the real entry, traceable data, user action, production
assembly, visible result, two safety invariants, and bounded slices. It runs the core journey before
implementation, then reaches the first vertical path within 45 minutes. UI work must be accepted by
a browser-driven key action; API-created success followed by browser inspection is rejected.

The standard-library `opc_increment.py` helper records commands, exits, timestamps, output, commit,
content-tree fingerprint, authenticity label, runtime metadata, object IDs, traces, and artifacts.
Code/test/plan/seed/config changes make old evidence stale. External providers stay locked until
offline layers pass and allow one canary attempt per revision. Completion is reported as code build,
automated core journey, real-service core journey, or human accepted.

Independent reviewers start with empty context and receive only the rubric, plan, diff, receipt,
project rules, and commands. A reality review after the first slice and a final integration review
share at most two repair rounds. Ledger validation rejects extra gates, excessive repairs, and
full-conversation task dispatch.

Optional `brainstorm`, `demo`, `prd`, and `architect` skills remain available for durable product
judgment, interaction taste, PM handoff, public contracts, or one-way technical decisions. Harness,
ship, deploy, oncall, retro, executable incident benchmarks, SHA freshness, HTML reports, and
language-adaptive output complete the suite.

## Suggested catalog tags

`product-development`, `coding`, `acceptance-testing`, `browser-e2e`, `tdd`, `workflow`,
`loop-engineering`, `harness`, `release-safety`, `codex`, `claude-code`

## Submission notes

Submit one suite-level listing linked to `https://github.com/wallkop/opc-develop`. The 12 skills
share repository-level packs, formats, rubrics, and scripts; verify that a catalog preserves those
shared resources rather than installing isolated skill folders.
