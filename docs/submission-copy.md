# Submission Copy

Use these descriptions when submitting opc-develop to skill directories, plugin marketplaces, and awesome lists.

## One-Line Description

Language-adaptive AI product development workflow suite for Codex and Claude Code, built around Harness initialization, prototype-driven design, review gates, TDD implementation, local E2E, and release verification.

## Short Description

opc-develop is a Codex and Claude Code skill suite for controlled AI-assisted product development. It is built for builders and OPC founders who want to turn raw ideas into reviewed requirements, real frontend prototypes, PRDs, technical designs, executable specs, testcases, plans, implementation, local verification, and release checks without losing product taste or engineering ownership.

## Medium Description

opc-develop packages a complete product-to-release workflow for AI-assisted builders. It starts with Harness initialization so the agent can understand the target repository, local runtime, tests, mocks, evidence, and release rules. Product work begins with a grilling-style brainstorm that turns a raw idea into a reviewed requirement. The suite then builds a high-fidelity frontend prototype directly inside the real project with frontend-only mocks, reviews it, and uses it as the product-experience anchor for PRD and technical design.

After design approval, opc-develop creates executable specs, black-box testcases, implementation plans, and dispatches TDD implementation work through mandatory subagents. It emphasizes artifact boundaries, independent review gates, prototype mock retirement, runtime evidence, local E2E, human acceptance routing, release verification, and rollback readiness. User-visible output adapts to the user's language while preserving technical identifiers and machine-readable status tokens.

## Long Description

opc-develop is an opinionated but project-agnostic workflow suite for controlled AI-assisted product development in Codex and Claude Code. It is designed for builders, OPC founders, and solo operators who personally own product judgment, design taste, and engineering quality. It is not a generic prompt pack for unconstrained code generation. Instead, it provides a staged operating model that keeps product structure, demo fidelity, architecture decisions, implementation contracts, testing evidence, and release gates explicit.

The workflow starts with Harness initialization and evaluation. These skills help a repository expose the context an AI agent needs: agent rules, documentation standards, local development runbooks, runtime evidence, logs, database or storage inspection rules, traces, API mocks, storage mocks, test gates, release runbooks, rollback paths, and acceptance standards. Once the project is legible, product work starts with `product-brainstorm`, which asks hard questions until a raw idea becomes a clear requirement with domain language, goals, non-goals, tradeoffs, constraints, alternatives, blockers, and acceptance signals.

For UI-facing features, opc-develop is prototype-driven. `create-demo` and `build-demo` build high-fidelity frontend prototypes inside the real frontend codebase, using frontend-only mocks for missing backend behavior. The running demo is reviewed independently and becomes the product-experience anchor for the PRD and technical design. Technical decisions are made explicitly in `technical.md`: public API contracts, system boundaries, storage choices, migration, security, operations, and runtime evidence. Data storage choices follow the target project's existing or explicitly approved architecture baseline; the suite does not impose a fixed database or cloud stack.

After design approval, `loop-develop` runs the development side of the workflow: executable specs, black-box testcases, boundary-only implementation plans, TDD implementation, implementation review, local E2E verification, runtime demo parity evidence, human acceptance routing, release verification, and rollback readiness. The suite includes shared contracts, reviewer prompts, implementer prompts, validation scripts, Codex plugin metadata, Claude Code plugin metadata, and a native Codex repo marketplace manifest.

## Suggested Tags

- agent-skills
- codex
- codex-plugin
- claude-code
- ai-agents
- product-development
- developer-workflow
- harness
- tdd
- local-e2e
- release-verification
- prototype-driven-development

## Directory Fields

| Field | Value |
| --- | --- |
| Name | opc-develop |
| Repository | https://github.com/wallkop/opc-develop |
| License | MIT |
| Author | wallkop |
| Contact | wallkop2026@zohomail.com |
| Category | Coding / Product Development / AI Agents |
| Install source | https://github.com/wallkop/opc-develop |
| Codex marketplace path | `.agents/plugins/marketplace.json` |
| Codex plugin manifest | `.codex-plugin/plugin.json` |
| Claude plugin manifest | `.claude-plugin/plugin.json` |
| Claude marketplace tag | `opc-develop--v0.1.3` |

## Account Checklist

| Channel | Account Or Token Needed | Notes |
| --- | --- | --- |
| GitHub Agent Skills | GitHub account authenticated with `gh auth login` | Run `gh skill publish --dry-run` before publishing. |
| Claude Code Community Marketplace | Anthropic / Claude account | Submit repository and plugin metadata through the official community marketplace flow. |
| Codex Repo Marketplace | No separate account beyond GitHub repo access | Users can add the repo marketplace from GitHub after `.agents/plugins/marketplace.json` is present. |
| LobeHub Skills | GitHub or site submission account if required | Use the one-line, short, and medium descriptions above. |
| SkillsHub.wtf | SkillsHub agent API key | Register an agent, then submit a suite-level entry pointing back to this repository. |
| SkillsLLM | Site submission account or form access if required | Submit the suite-level entry, not 27 separate dependent skills. |
| Agent Skills Hub / awesome lists | GitHub account | Submit PRs with repository link and short description. |
