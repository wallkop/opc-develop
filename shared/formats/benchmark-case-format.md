# Benchmark Case Format

One historical problem is one case. `profiles` are cheaper or more realistic reproductions of the
same ground truth, never different problem categories. The cheapest deterministic profile runs most
often; expensive real-environment profiles periodically calibrate it.

Required top-level keys: `schema_version`, `id`, `title`, `provenance`, `initial_state`, `task`,
`ground_truth`, `profiles`. Every profile has `id`, `kind`, `fidelity`, and a verification recipe.
Supported kinds: `fixture`, `fake`, `mutation`, `historical_ref`, `local_service`, `real`.

Every executed profile proves all three phases: correct version passes, injected/historical bad
version fails as expected, restored correct version passes again. A bad version that stays green is
a benchmark failure: the test is vacuous.
