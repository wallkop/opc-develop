# Rubric: technical.md

You are reviewing a technical design against `formats/technical-format.md`, the result card, any
approved PRD that exists, and the project's actual architecture. Inspect the codebase; do not take
the document's word for what exists. End with one `**Status:**` line and `Reviewed-SHA:` lines.

## Blocking checks

1. **One committed route**: exactly one design. Parallel "we could also" paths outside decision
   records' Options ⇒ reject.
2. **Decision records complete**: every contested choice (datastore, provider, queue, API shape,
   layering) is a numbered TD record with context/options/decision/consequences and a reversibility
   tag. Untagged irreversible choices are the highest-severity finding.
3. **Baseline compliance**: datastore/infrastructure choices match the project's existing baseline,
   or a TD record explicitly justifies divergence as [ONE-WAY]. Verify the baseline by inspecting
   the project, not the document.
4. **Public contracts fully specified**: every endpoint has request/response shapes and an error
   envelope; every schema change has a forward migration and a rollback note.
5. **Outcome/AC coverage**: the result-card journey is implementable; when a PRD exists, every AC is
   supported. Name any constraint the design cannot satisfy.
6. **Runtime Evidence Plan present and concrete**: per AC-cluster, named log events with
   correlation IDs, DB assertions, or dump commands — written against the project's actual
   observability (check `packs/harness-verbs.md` L3). "We will add logging" is not a plan.
7. **Boundary discipline**: no broad internal module plan or future test matrix. Slice-level detail
   stays in `feature-plan.md`; leakage downward is not thoroughness.
8. **Risk integration**: matching spike results are referenced only where the decision needed them;
   the 45-minute core slice remains viable.
9. **Demo alignment**: when an optional demo exists, the design supports its contractual
   interactions (data shapes, latency class, state visibility).

## Non-blocking

Capacity estimates, sequencing detail, appendix depth.
