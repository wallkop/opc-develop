# Security Policy

## Supported Versions

Security fixes target the latest tagged release and the `main` branch.

## Reporting A Vulnerability

Please report security issues by emailing `wallkop2026@zohomail.com`.

Do not open public issues for suspected credential exposure, private project data leakage, unsafe command execution, or supply-chain concerns. Include:

- affected version or commit;
- the vulnerable skill, reference, script, or manifest;
- reproduction steps;
- impact and suggested fix when available.

## Sensitive Data

This repository should not contain project-specific business artifacts, credentials, private logs, `.env` files, generated feature documents, customer data, production payloads, or provider secrets.

Reports, examples, fixtures, and screenshots must be redacted before being submitted.

## Supply Chain

opc-develop is distributed as source. Before installing or updating, review:

- `README.md`
- `.codex-plugin/plugin.json`
- `.claude-plugin/plugin.json`
- `.agents/plugins/marketplace.json`
- `skills/*/SKILL.md`
- `shared/scripts/*`

Run the local validation command before publishing changes:

```bash
python3 shared/scripts/test_opc_artifacts.py
```
