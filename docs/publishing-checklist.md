# Publishing Checklist

This checklist tracks public distribution channels for opc-develop.

## Already Prepared

- GitHub repository: `https://github.com/wallkop/opc-develop`
- MIT license
- English-first `README.md`
- Chinese `README.zh-CN.md`
- System architecture image: `assets/opc-develop-skills.png`
- Budget-routing image: `assets/opc-develop-routing.png`
- Codex plugin manifest: `.codex-plugin/plugin.json`
- Claude Code plugin manifest: `.claude-plugin/plugin.json`
- Claude marketplace manifest: `.claude-plugin/marketplace.json`
- Codex repo marketplace manifest: `.agents/plugins/marketplace.json`
- Security policy: `SECURITY.md`
- Contribution guide: `CONTRIBUTING.md`
- Submission copy: `docs/submission-copy.md`

## Validation Commands

```bash
python3 shared/scripts/test_opc_scripts.py
python3 shared/scripts/opc_benchmark.py validate shared/fixtures/opc-benchmark/registry.json
python3 shared/scripts/opc_benchmark.py run shared/fixtures/opc-benchmark/registry.json --repo .
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/plugin.json >/dev/null
python3 -m json.tool .claude-plugin/marketplace.json >/dev/null
python3 -m json.tool .agents/plugins/marketplace.json >/dev/null
ruby -ryaml -e 'Dir["skills/*/agents/openai.yaml"].each { |f| YAML.load_file(f) }'
rg -q 'v0\.5\.1' assets/opc-develop-skills.svg assets/opc-develop-skills.zh-CN.svg
rg -q 'Budget-first|预算优先' assets/opc-develop-routing.svg assets/opc-develop-routing.zh-CN.svg
claude plugin validate .
claude plugin validate .claude-plugin/plugin.json
claude plugin tag --dry-run .
```

## Channels

| Channel | Status | Next Action |
| --- | --- | --- |
| GitHub repository | Live | Keep `main` and tags updated. |
| Codex repo marketplace | Prepared in repo | Test from a clean Codex config or ask a peer to install from GitHub. |
| Claude Code plugin marketplace | Prepared in repo | Submit through the Claude community marketplace flow after account access is ready. |
| GitHub Agent Skills | Pending GitHub CLI auth and dry-run | Install/authenticate `gh`, run `gh skill publish --dry-run`, then publish if dependency layout is accepted. |
| LobeHub Skills | Pending account/submission route | Submit suite-level listing using `docs/submission-copy.md`. |
| SkillsHub.wtf | Pending API key | Register an agent, then submit a single suite-level skill entry. |
| SkillsLLM | Pending form/account | Submit suite-level listing using `docs/submission-copy.md`. |
| Agent Skills Hub | Pending PR | Submit repository link or supported catalog entry. |
| awesome lists | Pending PR | Submit after repository metadata and security docs are in place. |

## GitHub Agent Skills Risk

opc-develop has 12 interdependent skills that rely on repository-level `shared/packs/`,
`shared/formats/`, `shared/rubrics/`, and `shared/scripts/`. Before publishing through GitHub Agent
Skills, verify whether `gh skill publish` and `gh skill install` preserve those shared resources.

If GitHub installs each `skills/*/SKILL.md` folder independently without `shared/`, create a dedicated GitHub Agent Skills packaging layer before publishing.
