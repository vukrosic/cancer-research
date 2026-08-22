# EXP-20260822-018 independent artifact audit

## Local release checks

The runner completed its atomic staged-bundle validation. Independent checks
reproduced:

- manifest and implementation-boundary verification;
- `1290` context rows, `1290` endpoint rows, and two inference rows;
- all four CSV artifact hashes in `summary.json` and the summary self-digest;
- terminal `FEASIBILITY_ONLY`, `confirmatory_claim: false`, and
  `overall_pass: false` labels;
- Avana and KY design powers `0.8954` and `0.5364`;
- Avana delta `-0.1345336840`, `p=0.0277497225`, with failures of the
  `delta <= -0.20` and no-positive-lineage gates;
- KY delta `-0.1802884615`, `p=0.0624193758`, with failures of the effect,
  permutation, bootstrap, and lineage-heterogeneity gates.

## Independent pre-endpoint audit

The independent reviewer returned **GO** after the implementation and manifest
were committed. It verified the transitive implementation hashes, exact CDKN2A
status semantics and counts, design receipt binding, matrix-coverage error
classification, claim contract, and endpoint sequencing without opening
endpoint values.

## Independent post-execution audit

The independent artifact auditor recomputed the endpoint-derived receipts,
hashes, inference, and claim boundary. All checks matched. The release gate is
**GO** only with the exact label **T1 descriptive association only; not
T2/confirmatory**. No reliable biomarker, deletion, biallelic functional-loss,
TYMP-high, treatment, clinical, pooled, or positive replication claim is
permitted.
