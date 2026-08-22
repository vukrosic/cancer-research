# EXP033 methods audit

Selection used only frozen input hashes, metadata joins, the ARID1A
damaging-matrix column, the ATR endpoint header identity, literature metadata,
and seeded synthetic planning simulations. The target score column was not
parsed beyond confirming that `ATR (545)` exists exactly once. The selection
artifacts are therefore outcome-free.

The status is `1` when the ARID1A matrix value is `1` or `2`, and `0` when it is
`0`. The canonical roster contains 1,290 source/model rows: 975 Avana and 315
KY. ARID1A damaging/matrix-intact counts are Avana `101/874` and KY `43/272`;
mixed-lineage counts are `19/11`.

Planning uses the frozen lineage-stratified rank-delta estimator, independent
Normal null scores, an exposed mean shift of `-0.358286909243`, PCG64 streams,
100,000 permutations, and 10,000 alternative simulations. The exact planning
powers are `0.8666` and `0.5810`; KY is below the confirmatory threshold, so
the result is permanently feasibility-only.

Any input, schema, identity, coverage, canonical-roster, or manifest drift is
a non-evaluable stop. No target-specific threshold, lineage exclusion,
proxy relabelling, or post hoc rescue is permitted.
