# Rubric: demo / prototype

You are reviewing a running frontend prototype (or runnable skeleton for non-UI features) against
the source result card or `requirement.md`, plus the mock inventory. Use whichever source artifact
actually exists; do not invent a mandatory predecessor. You must actually exercise it — a review
from screenshots or code reading alone is invalid. End with one `**Status:**` line and
`Reviewed-SHA:` lines for the inventory and reviewed source docs; record the preview URL/command.

## Blocking checks

1. **It runs and is reachable**: start it per the documented command, open the preview URL (or run
   the skeleton command). Failure to launch ⇒ Issues Found, no further checks needed.
2. **Real-codebase integration**: the prototype lives in the project's real frontend on the feature
   branch. Reject: detached playground apps, query-param-only alternate roots, entry points that
   exist in code but are not reachable through the real UI shell.
3. **Fidelity**: layout, interaction, and state transitions are close enough to judge taste —
   target ≥80% of the intended experience. Placeholder styling in secondary areas is fine;
   placeholder *interaction* in the core path is not.
4. **Intent coverage**: every key path in the available source card or `requirement.md` can be
   walked in the prototype. List any that cannot.
5. **Mock inventory honesty**: every faked behavior you encounter while exercising the prototype
   has an inventory entry (id, file, type, scenario, replacement). Undocumented mocks are the
   single most dangerous defect here — hunt for them.
6. **No backend mutations**: the prototype changed no backend/production code. Frontend-only mocks.

## Non-UI variant (runnable skeleton)

Checks 1, 4, 5 apply unchanged. Checks 2-3 become: the skeleton exercises one real
request/response or command chain with production-shaped data (a stub returning the real schema
counts; a hardcoded print does not). Check 6 becomes: the skeleton's stubs are additive and
isolated — inventoried like any mock, changing no existing production behavior outside the
skeleton path.
