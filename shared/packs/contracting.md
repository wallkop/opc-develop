# Optional Coordination Contracts

Do not load this pack for normal standard increments. Use contracts only when the human explicitly
needs multi-owner coordination or an approved public technical design has independently separable
workstreams. Contracts are not a quality badge and never justify exceeding the four-hour increment.

## Partition by runnable outcome

- Every top-level item adds one user-visible result with its own black-box proof.
- Tables, services, modules, APIs, and migrations are child implementation tasks, not top-level
  completion nodes.
- If a workstream is not independently demonstrable, keep it under the owning slice.
- Any item estimated above two hours or requiring unrelated journeys must split again.
- Start from the core vertical slice; do not create one giant “thin slice” containing the whole
  platform.

## Tests

Define the core journey first. Add slice regressions as slices land. Do not translate every future
AC into committed failing skeletons before implementation. High-risk boundaries may use a failing
test first; ordinary future behavior waits for its slice.

Cross-workstream seams still need a real boundary check, not two mocks of each other. No production
test control may manufacture the success state.

## Dispatch

Contracts do not imply subagents. Dispatch only genuinely independent bounded work, one implementer
at a time, with cold one-page context and `context_mode: none|summary`. Use worktrees for isolation.
Review the assembled slice at the reality/final moments rather than reviewing every internal module.
