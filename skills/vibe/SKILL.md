---
name: vibe
description: "Use when the human explicitly wants the fastest possible implementation and will personally accept the result. Write code directly with no planning artifacts, no tests, no automated or browser verification, and no acceptance evidence. Stop only for missing requirements that make implementation impossible or for destructive, security-sensitive, permission, schema, or production actions that require human approval."
---

# vibe

Optimize for a directly human-reviewable implementation. The human owns all acceptance.

## Process

1. Read the request, the applicable `AGENTS.md`, and only the code needed to locate the change.
2. Make reasonable assumptions and edit the code immediately. Do not create plans, requirements,
   design records, contracts, ledgers, reports, or other workflow artifacts.
3. Do not write, update, run, or repair tests. Do not run linters, type checks, builds, syntax
   checks, browser flows, application smoke checks, or any other automated or manual verification.
4. Review the diff only to catch obvious unintended edits. Do not expand this into verification.
5. Hand the changed code to the human with a concise summary of what changed, the assumptions made,
   and the exact areas that require manual acceptance. State plainly that no tests were run.

## Boundaries

- Preserve unrelated user changes and keep the patch scoped to the request.
- Do not broaden scope for cleanup, refactoring, documentation, or speculative edge cases.
- Do not claim the change works, passes, or is production-ready; it is unverified until the human
  accepts it.
- Human approval remains mandatory before destructive operations, force pushes, publication,
  production changes, permission/security changes, or irreversible data/schema changes.
- If the request cannot be implemented without one of those actions, stop at that boundary and ask.

## Output

Changed code ready for human acceptance, plus a no-tests disclosure. No evidence or process artifacts.
