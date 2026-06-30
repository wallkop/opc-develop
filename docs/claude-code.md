# Claude Code Support

opc-develop supports Claude Code as a native plugin shape without an adapter directory.

## Structure

Claude Code reads:

- `.claude-plugin/plugin.json` for plugin metadata.
- `skills/<name>/SKILL.md` for plugin skills.
- `agents/*.md` for custom subagents.

The same root-level `skills/` and `shared/` content is also used by the Codex plugin. Platform-specific metadata stays in peer root directories such as `.claude-plugin/` and `.codex-plugin/`.

## Local Validation

From the repository root:

```bash
claude plugin validate .
```

For a local Claude Code session:

```bash
claude --plugin-dir /path/to/opc-develop
```

Then invoke skills by their Claude plugin namespace, for example:

```text
/opc-develop:product-brainstorm
/opc-develop:loop-design
/opc-develop:harness-eval
```

## Marketplace Source

This repository also includes `.claude-plugin/marketplace.json`, so it can be registered as a Claude Code marketplace source during development:

```text
/plugin marketplace add wallkop/opc-develop
/plugin install opc-develop@opc-develop-marketplace
```

Use GitHub as the canonical source for versions, issues, and release notes.

## Current Boundary

The Claude plugin currently relies on Claude Code's native skill discovery and explicit slash-command invocation. It does not install a session-start bootstrap hook. That means it should be invoked intentionally for OPC flows instead of trying to govern every Claude Code session automatically.
