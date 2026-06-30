# opc-develop

[简体中文](README.zh-CN.md)

opc-develop is a Codex / Claude Code skill suite for controlled AI-assisted product development. It combines a Lite flow for small iterations, a Full flow for end-to-end product development, and Harness initialization/evaluation capabilities.

![OPC-Develop skills workflow](assets/opc-develop-skills.png)

## Highlights

- Adapts output language to the user's input instead of enforcing a fixed default language.
- Builds real frontend prototype demos before PRD and technical design.
- Maintains explicit demo parity, frontend mock inventory, and prototype mock retirement.
- Uses independent review gates before downstream artifacts and implementation.
- Treats Harness as a first-class concern: documentation, testcases, runtime evidence, local E2E, and release verification are part of the workflow.
- Requires SaaS/infrastructure decisions in technical design; data storage choices must follow the target project's existing or explicitly approved architecture baseline, and unresolved high-impact choices block for human review.

## Who It Is For

opc-develop is built for builders, especially OPC founders and solo operators, who personally own the product judgment, design taste, and engineering taste behind a project. It assumes the human user can evaluate whether a requirement is structurally sound, whether an interaction feels right, and whether an architecture is likely to age well.

**It is not a good fit for pure implementation roles, or for engineering work where the hard part is heavy team coordination, organizational negotiation, roadmap alignment, or cross-team dependency management.** This suite deliberately increases product and architecture scrutiny before implementation. If you expect the agent to replace product taste, design judgment, or engineering ownership, this workflow will feel too demanding.

## Operating Philosophy

opc-develop is prototype-driven development for AI-assisted builders. The human stays responsible for context, taste, product structure, and architectural direction. The agent does the exhausting execution work once the direction is sharp enough.

The intended operating loop:

0. **Initialize the Harness first.** Use `harness-init` and `harness-eval` to make the target project legible to AI: project rules, documentation standards, local runbooks, runtime evidence, logs, database access, traces, API mocks, storage mocks, testing gates, release flow, and acceptance rules.
1. **Give the agent the raw idea and let it grill you.** Start with `product-brainstorm`; keep answering hard questions until the feature becomes a clear `requirement.md` with domain language, goals, non-goals, tradeoffs, constraints, and acceptance signals.
2. **Design a real UI demo inside the existing project.** Use `create-demo` or `build-demo` to build a high-fidelity frontend prototype against frontend-only mocks. Then keep vibe-coding and reviewing the interaction until it matches your product taste.
3. **Design and review the PRD and technical plan.** Use `build-prd`, `build-technical`, or `loop-design`, then review the artifacts seriously. This is where product structure and engineering architecture are protected from drifting in the wrong direction. **If you cannot judge product structure or architecture depth, stop here; opc-develop is not the right workflow for you yet.**
4. **Hand implementation, testing, and release to AI with confidence.** Once the design is approved, use `loop-develop`, `local-e2e-verify`, and `release-verify` to let the agent handle implementation, unit/API tests, black-box tests, local E2E, release checks, and rollback readiness. Codex Computer Use is strongly recommended for black-box browser verification. The human should focus on final acceptance and product-quality judgment.

## Contents

- `.codex-plugin/plugin.json` - Codex plugin manifest.
- `.claude-plugin/plugin.json` - Claude Code plugin manifest.
- `skills/` - atomic and orchestration skills.
- `agents/` - Claude Code custom subagents for OPC review and implementation roles.
- `shared/references/` - shared contracts, formats, and process rules.
- `shared/prompts/` - reviewer and implementer subagent prompts.
- `shared/scripts/` - small artifact validation helpers.
- `docs/` - platform-specific usage notes.

## Main Flows

- `lite-develop` - controlled small or medium-low-risk current-branch development.
- `product-brainstorm` - early feature clarification, domain language, alternatives, tradeoffs, and requirement capture.
- `loop-design` - demo, PRD, and technical design review loop.
- `loop-develop` - spec, testcases, plan, TDD implementation, and local verification loop.
- `harness-init` - guided Harness initialization planning.
- `harness-eval` - reusable Harness maturity scoring.
- `release-verify` - release gates, post-release checks, and rollback readiness.

## Install

### Codex

Use this repository as the canonical version source. Clone it into your Codex personal plugin source directory and enable the `opc-develop` personal plugin in Codex.

```bash
git clone https://github.com/wallkop/opc-develop.git ~/plugins/opc-develop
```

If your Codex setup uses a different personal plugin source directory, clone the repository there instead. For local development, keep this repository as the source of truth and let Codex install/cache from it.

### Claude Code

Use the same repository as a Claude Code plugin source:

```bash
claude --plugin-dir ~/plugins/opc-develop
```

Claude Code skills are invoked with the plugin namespace, for example `/opc-develop:product-brainstorm` or `/opc-develop:harness-eval`.

See [docs/claude-code.md](docs/claude-code.md) for details.

## Update

Peers should update from Git tags or the default branch:

```bash
cd ~/plugins/opc-develop
git pull --ff-only
```

After updating, restart Codex or Claude Code, or reload plugins if your client requires it.

## Publishing And Discovery

GitHub is the canonical source for history, tags, diffs, issues, and release notes. SkillHub, Claude marketplace, Codex marketplace, and similar directories are better used as discovery surfaces that link back to this repository.

## Safety Notes

This repository should not contain project-specific business artifacts, credentials, private logs, `.env` files, or generated feature documents. Keep requirement-specific outputs inside the target project repository, not inside this plugin.

## License

MIT
