# opc-develop

opc-develop is a Chinese-first Codex plugin suite for controlled AI-assisted product development. It packages a Lite flow for small changes, a Full flow for product/design/technical/development loops, and Harness initialization/evaluation skills.

![OPC-Develop skills workflow](assets/opc-develop-skills.png)

The suite is intentionally opinionated:

- Chinese-first user-visible output.
- Real frontend prototype demos before PRD and technical design.
- Explicit demo parity, frontend mock inventory, and prototype mock retirement.
- Review gates before downstream artifacts and implementation.
- Harness-first documentation, testcases, runtime evidence, release verification, and local E2E discipline.
- SaaS infrastructure decisions are made in technical design, with MySQL as the default SaaS database baseline unless the target project requires escalation.

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

See [docs/claude-code.md](docs/claude-code.md) for validation and marketplace-source notes.

## Update

Peers should update from Git tags or the default branch:

```bash
cd ~/plugins/opc-develop
git pull --ff-only
```

After updating, restart Codex or reload plugins if your Codex build requires it.

## Publishing And Discovery

GitHub is the canonical source for history, tags, diffs, issues, and release notes. Skill directories such as SkillHub are better used as discovery surfaces that link back to this repository.

## Safety Notes

This repository should not contain project-specific business artifacts, credentials, private logs, `.env` files, or generated feature documents. Keep requirement-specific outputs inside the target project repository, not inside this plugin.

## License

MIT
