# Contributing

opc-develop is a workflow suite for controlled AI-assisted product development. Contributions should keep the suite platform-aware, language-adaptive, and project-agnostic.

## Contribution Rules

- Do not add project-specific business context, private runbooks, customer data, credentials, logs, `.env` files, or generated feature artifacts.
- Do not hard-code a product, company, cloud provider, database, frontend framework, CI system, or deployment platform as a required default.
- Preserve language-adaptive behavior. User-visible output should follow `shared/core-contract.md`.
- Preserve the budget-first default: `lite` <=60 minutes, one `build` increment <=4 hours, and
  split anything larger. Standard increments keep one result card and one real core journey.
- Keep brainstorm/demo/PRD/technical artifacts opt-in. Risk adds the matching check rather than
  activating the complete artifact chain.
- Preserve receipt freshness, browser-driven UI acceptance, provider stop-loss, and the aggregate
  two-repair review cap as machine-enforced rules.
- Keep skills concise. Put reusable workflow detail in `shared/packs/`, formats/rubrics in their
  existing shared folders, and deterministic helpers in `shared/scripts/`.

## Local Validation

Run these checks before submitting a change:

```bash
python3 shared/scripts/test_opc_scripts.py
python3 shared/scripts/opc_benchmark.py validate shared/fixtures/opc-benchmark/registry.json
python3 shared/scripts/opc_benchmark.py run shared/fixtures/opc-benchmark/registry.json --repo .
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
ruby -ryaml -e 'Dir["skills/*/agents/openai.yaml"].each { |f| YAML.load_file(f) }'
```

If Claude Code is installed, also run:

```bash
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
claude plugin tag --dry-run .
```

## Release Checklist

1. Update `.codex-plugin/plugin.json`.
2. Update `.claude-plugin/plugin.json`.
3. Update `.claude-plugin/marketplace.json`.
4. Update `CHANGELOG.md`.
5. Run validation.
6. Commit the change.
7. Create both tags:

```bash
git tag -a vX.Y.Z -m "opc-develop X.Y.Z"
git tag -a opc-develop--vX.Y.Z -m "opc-develop X.Y.Z"
```

8. Push `main` and both tags.

## Pull Requests

Pull requests should explain:

- the workflow problem being solved;
- affected skills and shared contracts;
- validation commands run;
- any compatibility impact for Codex, Claude Code, or repository marketplace users.
