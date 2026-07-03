# Living Spec Format

Path: `docs/opc/specs/` — the system-level truth of what the product currently promises,
maintained by merging each feature's deltas at `ship`'s merge stage. Per-feature artifacts
describe increments; the living spec is where 30 features later you can still answer "what is
the permission model, in full, right now".

## Files

```
docs/opc/specs/
  <domain>.md          one per product domain (e.g. export.md, auth.md) — split when a file
                       passes ~300 lines; a spec nobody reads is not a spec
  _index.md            domain list + one-line scope each + decision index
```

## <domain>.md structure

```
# <Domain>

## Behavior                          the current AC registry for this domain
- 7-export/AC-3: exports respect role permissions        (since 2026-07)
- 9-share/AC-1: shared links expire after 30 days
                                     Feature-qualified ids — never renumbered, superseded
                                     entries struck through with the superseding id noted.

## State Machines                    current full state machines (not deltas)
## Permission Model                  current full table
## Decision Index                    PD/TD records that shaped this domain, by reference:
                                     7-export/TD-2 [ONE-WAY] datastore choice — technical.md link
```

## Merge Rules (executed by ship, merge stage)

- Copy the feature's non-struck ACs into the owning domain's Behavior registry, feature-qualified.
- An incoming AC that contradicts an existing entry is a **conflict, not an overwrite**: stop,
  route `revise` (the PRD should have declared the supersession). Deliberate supersession strikes
  the old entry with a note.
- Rebuild affected state machines and permission tables to the new full truth — the living spec
  holds current state, not history (git holds history).
- Append PD/TD references to the Decision Index.
- Nonexistent `docs/opc/specs/` bootstraps on first merge.

## Readers

- `prd` checks the owning domain file for AC conflicts **before** writing new ACs.
- `architect` intake reads the domain file first — it is the missing layer between one feature's
  artifacts and the whole codebase.
- `oncall` uses it to tell expected behavior from regression.
