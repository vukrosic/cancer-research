# EXP030 methods audit

Selection used only frozen input hashes, metadata joins, the BRCA1 and BRCA2
damaging-matrix columns, the CIP2A endpoint header identity, literature metadata,
and seeded synthetic planning simulations. The target score column was not
parsed beyond confirming that `CIP2A (57650)` exists exactly once. The selection
artifacts are therefore outcome-free.

The composite matrix value is `1` if either BRCA1 or BRCA2 has value `1` or `2`,
and `0` only when both are `0`. The canonical roster contains 1,290 source/model
rows: 975 Avana and 315 KY. Avana and KY each clear the minimum context counts,
with 16 and 8 mixed lineages, respectively.

Planning uses the frozen lineage-stratified rank-delta estimator, independent
Normal null scores, an exposed mean shift of `-0.358286909243`, PCG64 streams,
100,000 permutations, and 10,000 alternative simulations. The exact planning
powers are `0.6686` and `0.4355`; neither source can support a confirmatory
label.

Any input, schema, identity, coverage, canonical-roster, or manifest drift is a
non-evaluable stop. No target-specific threshold, lineage exclusion, proxy
relabelling, or post hoc rescue is permitted.
