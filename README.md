# opc-develop

[简体中文](README.zh-CN.md)

opc-develop is a Claude Code / Codex skill suite for AI-assisted product development, built for
builders who personally own the product judgment, design taste, and engineering taste behind a
project. It captures your taste in three artifacts (requirement, PRD + demo, technical design),
hands execution to agents under mechanical gates — and, unlike most workflow suites, **measures
its own loop** so the process can shrink as data justifies it.

![OPC-Develop skills workflow](assets/opc-develop-skills.png)

## Highlights

- **Three nested feedback loops instead of prose front-loading.** Task-level evidence (TDD
  RED/GREEN, evidence triangles), feature-level gates (rubric-fed fresh reviewers, content-SHA
  freshness), and loop-level measurement (`retro` mines ledgers and proposes improvements).
- **Demo first: data fake, feeling real.** A high-fidelity prototype inside the real frontend
  codebase before any PRD — taste is verified by experience, not by reading. Every mock is
  inventoried at creation and retired before done, with a final residual audit.
- **AC-ID spine.** PRD acceptance criteria are numbered once and referenced — never restated — by
  the technical design, implementation contracts, E2E specs, reviews, and the acceptance sheet.
- **Honest evidence, always labeled.** Every verification claim carries an authenticity label
  (`mock passed` → `seeded passed` → `local real service passed` → `external provider passed` →
  `human accepted` → `long-run passed`). A missing harness capability caps the achievable label;
  it never silently upgrades a claim.
- **Mechanical gates, not exhortations.** Review freshness is a `git hash-object` comparison
  (`check_freshness.py`), artifact structure is script-checked (`validate_artifacts.py`), ledger
  writes are schema-validated (`opc_ledger.py`), status tokens are machine-parsed. All stdlib
  Python, all covered by tests.
- **Token-lean by architecture.** One always-loaded core contract (~1.1k tokens) plus role packs
  pulled on demand. The heaviest invocation chain (build) is ≈5.4k framework tokens — roughly a
  quarter of comparable gate-heavy suites.
- **Self-evolution with governance.** Resolved failures append root causes to an error ledger;
  `retro` detects recurrences and proposes rules at the lowest enforcement layer (lint/hook first,
  prose last) — every rule needs human approval, records its provenance, and faces retirement
  review.
- **Fail open with recorded gaps.** Missing runbooks, services, or subagent support degrade
  honestly (recorded gap + capped labels) instead of blocking. Bare repositories work, including
  the lite path. Only destructive actions — deploys, force-pushes, deletions, publication — fail
  closed.

## Who It Is For

opc-develop is built for builders, especially OPC (one-person company) founders and solo
operators, who can evaluate whether a requirement is structurally sound, whether an interaction
feels right, and whether an architecture will age well. The suite protects those judgments; it
does not replace them.

**It is not a good fit** for pure implementation roles, or for work where the hard part is team
coordination and roadmap negotiation. The suite deliberately concentrates human attention on five
decision points; if you cannot judge product structure or architecture depth at those points, the
workflow will feel demanding rather than helpful.

## Operating Philosophy

The human stays responsible for context, taste, product structure, and architectural direction.
The agent does the execution once direction is sharp — and the loop itself is instrumented so you
can see where tokens, rework, and repeated mistakes actually go.

The intended operating loop:

0. **Make the project legible first.** Run `harness` to score and build the four verbs — *run*
   (one-command stack + logs to a fixed path), *reset* (idempotent clean state + named seed
   scenarios), *observe* (structured logs with correlation IDs, read-only DB recipes, state
   dumps), *drive* (committed Tier-1 E2E specs, authored by agentic exploration). Capabilities
   are scored by executing them, never by reading documents.
1. **Give the agent the raw idea and let it grill you** (`brainstorm`). One question at a time,
   each with a recommended answer, until the idea becomes a ≤150-line decision-first
   `requirement.md` with domain language, non-goals, tradeoffs, risk profile, and acceptance
   signals — on its own numbered feature branch.
2. **Experience it before specifying it** (`demo`). The agent builds a prototype inside the real
   frontend (or a runnable skeleton for non-UI features) against frontend-only mocks. You play
   with it; the tune-loop is free and unlimited. Cheap `revise` here beats expensive rework later.
3. **Sign the product decision sheet** (`prd`). The product owner — a PM, or you solo — turns
   the experienced demo into a PRD with numbered ACs and PD decision records, signs the decision
   sheet, and pushes the feature branch as the handoff.
4. **Intake, then sign the architecture decision sheet** (`architect`). The architect pulls the
   branch, runs intake (understand before designing; questions route back to the product owner
   as `revise`, never self-answered), runs risk spikes, commits to one route in ADR-style TD
   records, and explicitly approves anything tagged `[ONE-WAY]`. Contested choices arrive with
   options, tradeoffs, a recommendation, reversibility, and the cost of deferring — or they
   don't arrive at all.
5. **Hand off everything local in one run** (`build`). Internally it partitions the work into
   gated implementation contracts, dispatches TDD implementer subagents with captured RED/GREEN
   evidence, runs a merged compliance + quality review per contract, applies this feature's
   migrations/config to the local or shared dev environment under safety rules, deploys locally,
   and runs the full black-box regression — evidence triangles (interface assertion +
   correlation-ID log chain + state assertion) per AC, distilled into committed Tier-1 specs,
   ending in a gated acceptance sheet. No human touchpoint; the output is evidence.
6. **Accept on the test environment** (`ship`). Release manifest (DDL, env vars, config —
   collected from the diff, gated against technical.md) → test-env deploy → automated regression
   there → the test-acceptance touchpoint. Your verdict routes mechanically: code defect →
   `build` (fix mode; ship resumes at deploy), artifact defect → `revise` upstream, new need →
   `brainstorm`. Approval merges the branch to the trunk.
7. **Release to production separately** (`deploy`), fail-closed: preflight verifies test
   acceptance + trunk merge + complete manifests + rollback readiness before anything runs;
   then production env changes with backups, the deploy, prod-safe online regression, and a
   watch window. `oncall` handles anything that breaks in production: diagnostic report, then
   rollback / expedited hotfix / mitigation. `retro` closes the loop weekly: where tokens went,
   which gates earn their keep, which mistakes repeat.

## The Feedback Model

All human feedback, at every touchpoint, classifies as exactly one of:

| Class | Meaning | Cost |
|---|---|---|
| `tune` | same intent, different execution — iterate in place | free, unlimited, unrecorded |
| `revise` | an upstream artifact was wrong — fix at the earliest broken layer, downstream approvals go SHA-stale, replay forward | one ledger entry |
| `park` | stop this line of work cleanly | one ledger entry |

Acceptance rejections triage further: **implementation defect** (code ≠ artifact → targeted fix),
**artifact defect** (code = artifact, artifact wrong → revise + cascade), **taste change**
(artifact was right, intent moved → new increment via `brainstorm`, recorded as `change`, never
as rework). Attribution is the agent's job; arbitration is yours.

## Skills

| Skill | Use | Human touchpoint |
|---|---|---|
| `brainstorm` | raw idea → grilled, decision-first requirement + feature branch | ① confirm the 1-page summary |
| `demo` | experienceable prototype in the real codebase + mock inventory | ② play until the feel is right |
| `prd` | PRD (AC/PD ids), gated, then push = product→architecture handoff | ③ product sign-off |
| `architect` | intake → risk spikes → technical design (TD records), gated | ④ architecture sign-off |
| `build` | everything local: contracts → TDD implementers → local deploy (incl. dev-env DDL/config) → black-box regression → acceptance sheet | — |
| `ship` | release manifest → test-env deploy → automated regression → test acceptance → merge to trunk | ⑤ test acceptance |
| `deploy` | fail-closed production release: preflight, env changes with backups, deploy, prod-safe regression, watch | confirm every destructive step |
| `oncall` | production diagnosis → report → rollback / expedited hotfix / mitigation → long-term proposal | choose the path |
| `lite` | small/low-risk changes on the current branch, zero ceremony, bare-repo OK | quick before/after check |
| `retro` | weekly loop report + rule crystallization + gate pruning proposals | approve rules and prunings |
| `harness` | score the four verbs by executing; build gaps as scripts/seeds/conventions | — |

## Working With a PM

The full flow supports a two-person split along the taste boundary:

- **Product owner** runs `brainstorm` → `demo` → `prd` on the feature branch. `prd` ends by
  pushing the branch and printing a handoff summary (ACs, open questions, risk profile, gaps).
- **Architect/builder** pulls the branch and runs `architect` onward. It starts with an intake
  pass — read the artifacts, exercise the demo, list understanding questions. Questions route
  back to the product owner as `revise` entries (with an `actor` field in the ledger), never
  silently self-answered.
- Cross-role rework stays visible: `retro` attributes rework routing by actor, so you can see
  whether defects trace to product capture or technical execution.

Solo builders run the same two skills back-to-back; the intake step auto-skips when the same
person just produced the PRD.

## Repository Layout

- `skills/` — the 11 skills (each ≤ ~95 lines; detail lives in packs).
- `shared/core-contract.md` — the one always-loaded contract: status tokens, evidence labels,
  feedback taxonomy, freshness, failure philosophy, ledger duty, isolation.
- `shared/packs/` — nine on-demand rule packs (gate protocol, decision protocol, feedback
  routing, evidence, TDD implementation, mock retirement, risk & readiness, branch & worktree,
  harness verbs).
- `shared/formats/` — artifact format specs: requirement, PRD, technical, implementation
  contract, ledger schemas.
- `shared/rubrics/` — seven gate rubrics, given to reviewers in full (the reviewer always holds
  the rulebook it enforces).
- `shared/scripts/` — L0 tooling: `opc_ledger.py`, `check_freshness.py`,
  `parse_review_status.py`, `validate_artifacts.py`, `recurrence_scan.py`,
  `next_feature_slug.py`; tested by `test_opc_scripts.py` (stdlib only).
- `agents/` — `opc-reviewer` (read-only by tool restriction) and `opc-implementer`.
- `shared/prompts/` — reviewer and implementer subagent prompts.
- `.claude-plugin/`, `.codex-plugin/`, `.agents/` — platform manifests.

Feature artifacts live in the **target project**, never in this plugin:
`docs/features/<n>-<name>/` (requirement, demo notes + mock inventory, prd, technical,
contracts/, reviews/, acceptance.md, ledger.jsonl) plus project-wide `docs/opc/`
(error-ledger.jsonl, rules.md, retro reports).

## Platform Notes

- **Claude Code** — full support: isolated reviewer/implementer subagents, `${CLAUDE_PLUGIN_ROOT}`
  path resolution, tool-restricted reviewer.
- **Codex and other harnesses** — skills and scripts work; where isolated subagents are
  unavailable, gates and builds degrade honestly (`self-reviewed (no isolation)` /
  `self-implemented (no isolation)` ledger labels, surfaced at the next human touchpoint) rather
  than blocking or silently self-approving.

## Install

### Claude Code

```bash
claude --plugin-dir ~/plugins/opc-develop
```

Invoke with the plugin namespace: `/opc-develop:brainstorm`, `/opc-develop:lite`,
`/opc-develop:retro`. Or register as a marketplace source — see
[docs/claude-code.md](docs/claude-code.md).

### Codex

```bash
codex plugin marketplace add wallkop/opc-develop --ref main
codex plugin add opc-develop@opc-develop
```

For local development, clone into your personal plugin source directory:

```bash
git clone https://github.com/wallkop/opc-develop.git ~/plugins/opc-develop
```

## Update

```bash
cd ~/plugins/opc-develop
git pull --ff-only
```

Restart Claude Code / Codex or reload plugins afterwards.

## Migrating from v0.1

| v0.2 | absorbs (v0.1) |
|---|---|
| `brainstorm` | product-brainstorm |
| `demo` | create-demo, review-demo, build-demo |
| `prd` | create/review/build-prd, loop-design (product half) |
| `architect` | create/review/build-technical, loop-design (technical half) |
| `build` | create/review-spec, create/review-testcases, create/review-plan, tdd-coding, debug-failure, loop-develop, local-e2e-verify (contracting and verification are internal phases) |
| `ship` | acceptance-rework, finish-branch, release-verify (test half) |
| `deploy` | release-verify (production half) |
| `oncall` | — (new) |
| `lite` | lite-develop |
| `retro` | — (new) |
| `harness` | harness-init, harness-eval |

v0.1 feature artifacts remain readable; new features use the v0.2 formats. The biggest behavioral
changes: reviews are SHA-fresh instead of mtime-fresh, missing project documents record gaps
instead of blocking, and parallel implementation always uses worktrees.

## Publishing And Discovery

GitHub is the canonical source for history, tags, diffs, issues, and release notes. Marketplace
directories are discovery surfaces that link back to this repository.

## Safety Notes

This repository must not contain project-specific business artifacts, credentials, private logs,
`.env` files, or generated feature documents — those belong in the target project. Destructive
actions (deploys to shared surfaces, force-pushes, deletions with unmerged work, external
publication) always require explicit human confirmation, regardless of prior approvals.

## License

MIT
