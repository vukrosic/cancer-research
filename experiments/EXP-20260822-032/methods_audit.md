# EXP032 methods audit

Selection used only frozen input hashes, metadata joins, the SMAD4 damaging-
matrix column, the AURKA endpoint header identity, literature metadata, and
seeded synthetic planning simulations. The target score column was not parsed
beyond confirming that `AURKA (6790)` exists exactly once. The selection
artifacts are therefore outcome-free.

The status is `1` when the SMAD4 matrix value is `1` or `2`, and `0` when it is
`0`. The canonical roster contains 1,290 source/model rows: 975 Avana and 315
KY. Avana and KY each clear the minimum context counts, with 12 and 6 mixed
lineages, respectively.

Planning uses the frozen lineage-stratified rank-delta estimator, independent
Normal null scores, an exposed mean shift of `-0.358286909243`, PCG64 streams,
100,000 permutations, and 10,000 alternative simulations. The exact planning
powers are `0.6502` and `0.4713`; neither source can support a confirmatory
label.

Any input, schema, identity, coverage, canonical-roster, or manifest drift is a
non-evaluable stop. No target-specific threshold, lineage exclusion, proxy
relabelling, or post hoc rescue is permitted.
