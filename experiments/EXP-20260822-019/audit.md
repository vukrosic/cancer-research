# EXP-20260822-019 independent artifact audit

## Local release checks

The runner completed its atomic staged-bundle validation. Independent checks
reproduced:

- manifest, selection-seal, and implementation-boundary verification;
- `1290` context rows, `1290` endpoint rows, and two inference rows;
- all four CSV artifact hashes in `summary.json`, the sealed pre-endpoint
  receipt, and the normalized summary self-digest;
- terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` labels;
- Avana and KY design powers `0.8562` and `0.5375`;
- Avana delta `-0.2803388986`, `p=0.0001199988`, bootstrap CI
  `[-0.3954647396, -0.1572389733]`, with only the no-positive-lineage gate
  failing;
- KY delta `-0.0066050198`, `p=0.4830751692`, bootstrap CI
  `[-0.2153236460, 0.2021136063]`, with effect-size, permutation, bootstrap,
  and no-positive-lineage gates failing.

## Independent pre-endpoint audit

The independent reviewer returned **GO** after the implementation and manifest
were committed. It verified the full endpoint hash, selection-seal ancestry,
transitive implementation hashes, exact PTEN status semantics and counts,
design receipt binding, deterministic inference contract, and claim boundary
without opening endpoint values.

## Independent post-execution audit

The independent artifact auditor recomputed all endpoint-derived receipts,
hashes, deltas, permutation p-values, bootstrap intervals, lineage gates, and
terminal labels. All checks matched. The release gate is **GO** only with the
exact label **T1 descriptive association only; not T2/confirmatory**. No
general PTEN-to-PIK3CB dependency, PTEN-null, inhibitor, treatment, clinical,
pooled, or positive replication claim is permitted.
