# EXP039 methods audit

The frozen direction is a composite damaging-matrix proxy defined by either
`PBRM1 (55193)` or `ARID2 (196528)` status to `PARP1 (142)` dependency in the
DepMap 23Q4 naive CRISPR endpoint. The composite was selected because isolated
PBRM1 damaging status has only 11 eligible KY models, below the frozen minimum
of 20; broadening to the related PBAF subunit ARID2 makes the proxy executable
while lowering the claim boundary.

Selection used only frozen input hashes, QC and model metadata, the two
status-matrix columns, the exact PARP1 endpoint header, literature metadata,
and seeded synthetic planning simulations. No PARP1 score row or endpoint
value was parsed during selection.

The implementation must:

- bind both matrix columns and the OR-composite rule before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- preserve source-specific analysis and the lineage-stratified estimand;
- write a pre-endpoint receipt before loading PARP1 values;
- stop at T0 on coverage, identity, domain, or design drift; and
- keep the result permanently feasibility-only because both planning powers
  are below `0.80`.

The source study supports PBRM1-deficiency sensitivity to PARP and ATR
inhibitors. EXP039 tests only transport of the broader PBRM1-or-ARID2 matrix
proxy to genetic PARP1 dependency; it cannot support isolated-PBRM1,
pharmacologic, HRD, causal, treatment, or clinical claims.
