# Human Reports: HTML, Plain Language, Machine Truth

Every report shown to a human has a self-contained HTML companion. Markdown or JSON stays the
source of truth for hashes, gates, diffs, and automation; HTML is the required reading surface.

## Required companions

| Machine/artifact truth | Human report source and HTML |
|---|---|
| feature requirement/prd/testcases/technical/acceptance | `reports/<name>.md` + `reports/<name>.html` |
| retro JSON | `docs/opc/retro/<date>.md` + `.html` |
| oncall evidence/incident facts | same-basename `.md` + `.html` under `docs/opc/incidents/` |
| harness assessment JSON/evidence | same-basename `.md` + `.html` beside the machine source |
| benchmark report.json | `report.html` in the benchmark report directory |
| ship/deploy human handoff | feature report or same-basename HTML under `docs/opc/deploy/` |

JSONL, manifests, status tokens, IDs, and machine-only evidence are not converted to HTML.
Feature report markdown is a faithful human summary, not a second product truth: it cites the
artifact SHA and may simplify wording but may not add decisions or claims absent from the artifact.

## Plain-language contract

Every Chinese report opens with these reader questions, using equivalent headings in other target
languages: `结论`, `对用户意味着什么`, `证据`, and `下一步` or `需要决定什么`.

Prefer short active sentences and business outcomes. Put implementation detail after the outcome.
At the first use of a specialist term, explain it immediately: `GT（机器判定结果对不对的标准）`.
Do not repeat the explanation later. Common terms live in `formats/report-terms.json`; project
terms follow the same rule. A separate glossary does not satisfy first-use explanation.

## Render and lint

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/render_report.py" render SOURCE.md --out REPORT.html --lang zh-CN
python3 "${CLAUDE_PLUGIN_ROOT}/shared/scripts/render_report.py" lint SOURCE.md --html REPORT.html \
  --terms "${CLAUDE_PLUGIN_ROOT}/shared/formats/report-terms.json" --lang zh-CN
```

The HTML must contain inline CSS, no external assets, the target-language `lang`, and the SHA-256
of its source. Regenerate after any source change. Nothing may contradict the source. Reviewers
read markdown for correctness and HTML for human clarity.
