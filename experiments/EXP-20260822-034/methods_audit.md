# EXP034 methods audit

Selection used only frozen input hashes, metadata joins, the TP53
damaging-matrix column, the TDG endpoint header identity, literature metadata,
and seeded synthetic planning simulations. The target score column was not
parsed beyond confirming that `TDG (6996)` exists exactly once. The selection
artifacts are therefore outcome-free.

The status is `1` when the TP53 matrix value is `1` or `2`, and `0` when it is
`0`. The canonical roster contains 1,290 source/model rows: 975 Avana and 315
KY. TP53 damaging/matrix-intact counts are Avana `610/365` and KY `233/82`;
mixed-lineage counts are `25/16`.

Planning uses the frozen lineage-stratified rank-delta estimator, independent
Normal null scores, an exposed mean shift of `-0.358286909243`, PCG64 streams,
100,000 permutations, and 10,000 alternative simulations. The exact planning
powers are `0.9951` and `0.7617`; KY is below the confirmatory threshold, so
the result is permanently feasibility-only.

Any input, schema, identity, coverage, canonical-roster, or manifest drift is
a non-evaluable stop. No target-specific threshold, lineage exclusion,
proxy relabelling, or post hoc rescue is permitted.
