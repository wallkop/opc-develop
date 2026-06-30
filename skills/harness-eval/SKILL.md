---
name: harness-eval
description: Evaluate a repository's engineering harness maturity with a reusable 0-5 score in 0.5 increments. Use when Codex is asked to assess, audit, score, benchmark, or improve project harness completeness, including AI agent rules, branch/release flow, documentation governance, API mock and storage mock maturity, fixture isolation, test strategy, local E2E, runtime evidence, CI gates, traceability, or verification readiness.
license: MIT
---

# Harness Eval

## Overview

Assess the current repository's Harness as an executable engineering system, not as a documentation checklist. Favor observed scripts, gates, reports, traceability, and failure evidence over aspirational plans.

Use a 0-5 scale with 0.5 steps. Compute the overall score as the rounded-to-nearest-0.5 average of the dimension scores, then apply any cap rules.

## Required References

Read before acting:

- `../../shared/references/language-contract.md`
- `../../shared/references/harness-doc.md`
- `../../shared/references/branch-stage-contract.md`
- `../../shared/references/mock-system-contract.md`

Use `harness-doc.md` as the baseline for documentation architecture, feature artifact layout, global testcase organization, technical docs, reviews, progress records, and changelog expectations. Use `branch-stage-contract.md` as the baseline for branch lifecycle: early brainstorming can remain on the current branch, `product-brainstorm` creates or enters the feature branch before writing `requirement.md`, and `create-demo` plus later Full feature skills must run on that feature branch. Use `mock-system-contract.md` as the baseline for API mock, storage mock, fixture isolation, scenario switching, reset, and mock evidence. Project `AGENTS.md` and project-specific runbooks remain binding when stricter.

## Workflow

1. Read project rules first.
   - Read root `AGENTS.md` and any scoped `AGENTS.md` that applies.
   - Read project runbooks, standards, harness docs, testcase docs, runtime docs, release/rollback docs, and package scripts if present.
   - Obey repository-specific rules about where assessment reports must be written.

2. Inventory the Harness assets.
   - Inspect branch/status and avoid reverting unrelated user changes.
   - Discover harness docs, test directories, local-dev scripts, CI configs, release scripts, runtime-evidence tooling, testcase indexes, Playwright/E2E assets, API coverage inventory, mock-system docs, API mock entrypoints, storage mock entrypoints, fixture directories, scenario profiles, reset commands, mock reports, and generated reports.
   - Use `rg`, `find`, and package metadata before slower or ad hoc approaches.

3. Validate with lightweight commands when safe.
   - Prefer non-destructive checks: syntax checks, static audits, inventory audits, check-only health commands, or existing harness dry-run commands.
   - Do not start/stop services, run long tests, publish, migrate data, or mutate external systems unless the user asked or project rules require it.
   - If a check fails because prerequisites are missing, record it as evidence. Do not mark it as passed.

4. Score each dimension.
   - Score from 0 to 5 using 0.5 steps.
   - Credit runnable, repeatable, reported evidence more than written intent.
   - Distinguish "covered by real tests" from "explicitly not applicable", "manual only", or "planned".
   - Penalize contradictions between project rules, runbooks, scripts, and reports.

5. Write the report.
   - If the repository has a Harness docs location, write there, using a dated filename such as `harness-assessment-YYYY-MM-DD.md`.
   - Otherwise write under `docs/technical/harness/` if appropriate, or provide the report inline if the user only asked for a summary.
   - Include command results, limitations, scores, major risks, and prioritized improvements.

## Scoring Anchors

| Score | Anchor |
| ---: | --- |
| 0 | No corresponding assets or process. |
| 0.5 | Scattered notes, temporary scripts, or informal convention only. |
| 1.0 | Initial documents or directories exist but are not executable. |
| 1.5 | Partial standards exist; execution requires substantial human inference. |
| 2.0 | Basic assets and entrypoints exist, with small coverage or weak reporting. |
| 2.5 | Runnable prototype covers a few main paths. |
| 3.0 | Standard workflow exists and main entrypoints run, but coverage or closure is incomplete. |
| 3.5 | Scripted gates, reports, and evidence indexes exist; key paths still rely on manual work or plans. |
| 4.0 | Core flow is mostly automatable, failures are diagnosable, and remaining gaps are explicit governance debt. |
| 4.5 | Broad coverage and strong drift protection; only edge cases require manual confirmation. |
| 5.0 | Full repeatable, auditable development-to-release Harness with closed coverage, evidence, rollback, and governance loops. |

## Standard Dimensions

Use these dimensions unless the repository clearly needs a narrower or broader model:

1. **Governance Contract And Agent Rules**
   - Looks for root/scoped agent rules, stable blocking rules, secret handling, tool usage constraints, and clear AI execution boundaries.

2. **Documentation Architecture And Traceability**
   - Looks for feature docs, technical docs, standards, runbooks, decisions, testcase indexes, historical migration handling, and requirement-to-test traceability.

3. **Branch, Integration, Release, And Rollback Flow**
   - Looks for branch policy, `product-brainstorm` requirement-commit as the Full feature branch boundary, `create-demo` and later Full skills requiring the feature branch, current-branch Lite/bugfix rules, non-`develop` confirmation boundaries, optional worktree trigger criteria, merge gates, feature/integration/release separation, release runbook, rollback runbook, and dry-run evidence.

4. **Local Development Service Orchestration**
   - Looks for standard start/stop/status commands, detached service behavior, health checks, logs, PID management, troubleshooting, and lifecycle discipline.

5. **White-Box Test Foundation**
   - Looks for unit, API, integration, coverage thresholds, deterministic test DB or mocks, aggregation commands, and recent passing evidence.

6. **API Or Contract Coverage Audit**
   - Looks for endpoint or interface inventory, scenario mapping, drift detection, strict coverage rules, generated reports, and a clear distinction between real tests and N/A.

7. **Black-Box Testcases And UI Automation**
   - Looks for long-term testcase docs, product-module organization, Playwright/Web automation, desktop/Electron/manual harness evidence, login handling, screenshots/traces, and reports.

8. **Mock System And Fixture Isolation**
   - Looks for both API mock and storage mock, explicit mock mode/profile, scenario switching, fixture reset/cleanup, non-sensitive fixture policy, demo/prototype worktree support, local E2E/regression/human acceptance reuse, report generation, drift checks, and clear separation from real backend, real storage, credentials, and production data.

9. **Local E2E Aggregation And Machine Reports**
   - Looks for a single local E2E entrypoint, precondition checks, report JSON, raw report paths, failure classification, and optional service/tool/provider E2E modes.

10. **Runtime Evidence, Logs, DB, And Trace**
   - Looks for runtime evidence package generation, manifest schema, log collection, DB allowlist diagnostics, agent/tool/provider trace, payload retention, redaction, and reproduction commands.

11. **Drift Protection, Metrics, And Continuous Governance**
   - Looks for inventory audits, doc/test consistency checks, CI/pre-push gates, dirty-worktree awareness, trend reports, stale asset detection, and clear ownership of remaining gaps.

## Cap Rules

Apply these after averaging:

- Cap at 2.0 if no stable project rules or runbooks exist.
- Cap at 2.5 if there is no runnable test or validation entrypoint.
- Cap at 3.0 if tests exist but no machine-readable report or failure artifact exists.
- Cap at 3.5 if local E2E or equivalent end-to-end validation is entirely absent.
- Cap at 4.0 if release or rollback is only documented and has no dry-run, gate, or evidence path.
- Cap at 4.0 if multiple required rules contradict each other and the contradiction affects merge, release, test, or evidence conclusions.
- Cap the Mock System dimension at 2.0 when either API mock or storage mock is missing.
- Cap the overall score at 4.0 when API mock and storage mock are not both present.
- Cap the overall score at 3.5 and list a high risk when mock flows access real secrets, production data, real protected user data, real cloud storage, or real production services.
- Cap Black-Box Testcases And UI Automation and Local E2E Aggregation And Machine Reports at 3.5 when high-fidelity demo or prototype validation requires real backend/storage because mock support is absent.
- Never score 4.5 or 5.0 when the assessment relies mainly on plans rather than recent executable evidence.

## Evidence To Capture

Record exact commands, exit codes, and key summaries. Typical lightweight commands include:

```bash
git status --short --branch
find docs -maxdepth 4 -type f | sort
find scripts test -maxdepth 4 -type f | sort
node -e "const p=require('./package.json'); console.log(JSON.stringify(p.scripts,null,2))"
```

Also run repository-specific audit commands when available and safe, for example coverage inventory checks, static testcase audits, mock smoke/check commands, local E2E check-only commands, or runtime evidence smoke commands.

## Report Shape

Use this structure:

```markdown
# Harness Assessment

**Assessed at**: <timestamp>
**Branch**: `<branch>`
**Commit**: `<commit>`
**Scope**: <what was assessed and what was not>

## Scoring Method
<0-5 anchors, 0.5 step, average and caps>

## Command Evidence
| Command | Result | Key evidence |

## Dimension Scores
| Dimension | Score | Assessment |

## Mock System Summary
| Area | Status | Evidence |
| --- | --- | --- |
| API mock | Present/Partial/Missing/Unknown | <evidence> |
| Storage mock | Present/Partial/Missing/Unknown | <evidence> |
| Fixture isolation risk | Low/Medium/High/Unknown | <evidence> |
| Recommended next step | <action> | <acceptance standard> |

**Overall score**: `<score> / 5.0`

## Main Risks
1. ...

## Priority Improvements
| Priority | Recommendation | Acceptance standard |

## Limitations
<commands not run, missing services, missing credentials, unavailable remote, etc.>
```

## Common Findings To Check

- Rules say one gate is required, but runbooks or scripts use a different gate.
- API coverage is closed mostly through `not_applicable` entries rather than real tests.
- API mock exists but storage mock is missing, causing high-fidelity demo, E2E, or acceptance to depend on real backend/storage.
- Mock fixtures include real tokens, production payloads, protected user files, or unredacted personal data.
- Mock mode is implicit or can accidentally run on production/default paths.
- Mock scenarios cannot reset state, making E2E/regression failures non-reproducible.
- Testcase documents exist, but Playwright, Computer Use, or equivalent automation covers only one or two of them.
- Historical feature docs lack `testcases.md`, PRD links, progress reports, or acceptance evidence.
- Local E2E does not own service lifecycle, or its lifecycle responsibility is ambiguous.
- Runtime evidence exists but is not indexed from failing E2E reports.
- Trace payloads are collected without a retention or redaction policy.
- Release and rollback docs exist but have no dry-run report.
- CI or local gates do not run the same commands required by project rules.
- The worktree is dirty and unrelated changes could be merged accidentally.

## Integrity Rules

- Do not claim a gate passed unless it was run successfully or a dated report proves it.
- Do not treat missing credentials, missing services, or unavailable remotes as success.
- Do not paste secrets, cookies, tokens, provider configs, or full sensitive logs into the report.
- Do not overwrite project-specific Harness plans; add a dated assessment or update only the intended report.
- Mark evidence as "not run" when it was not run.
