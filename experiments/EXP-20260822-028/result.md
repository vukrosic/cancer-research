# EXP028 result — TP53 damaging proxy to TIPARP dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `TIPARP (25976)` / PARP7 from the frozen DepMap 23Q4 naive CRISPR
  screen;
- exposure: TP53 matrix value `1` or `2`, labeled `damaging`;
- reference: TP53 matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from the SCHEMATIC literature and
metadata-only frozen-matrix planning. The primary study describes a
multilineage PARP7 interaction network that includes TP53 and related genome
integrity factors, while its strongest pharmacologic validation focused on
KDM5C/KDM6A alterations: [Nature Genetics study](https://www.nature.com/articles/s41588-024-01971-9).
This experiment tests only a TP53 damaging-matrix proxy against a genetic
TIPARP screen endpoint; it does not recreate the paper's combinatorial CRISPR
interaction score or pharmacologic experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.027367551378704946 | 9683 | 0.28495715042849573 | [-0.11742228648146236, 0.06103480326345141] | 14 | +0.5703703703703704 | FAIL |
| KY | -0.07959479015918958 | 1382 | 0.1835081649183508 | [-0.24457308248914617, 0.08827785817655572] | 8 | +0.3333333333333333 | FAIL |

Both source estimates were weakly negative, but neither reached the required
delta threshold of `-0.20`, permutation p-value threshold of `0.05`, or
bootstrap upper-bound threshold of `0`. Both met the minimum count of negative
lineages, but both violated the no-positive-lineage gate.

Avana planning power was `0.9952`; KY planning power was `0.7509`. The paired
experiment is therefore permanently feasibility-only even though Avana had
adequate planning power by itself.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
TP53 damaging-matrix proxy showed weak, uncertain, lineage-heterogeneous
negative associations with TIPARP dependency in both source families, with no
source-specific nominal gate passing. This is not evidence of a robust
TP53–TIPARP dependency.

This does not establish functional TP53 loss, a SCHEMATIC combinatorial
interaction, causal synthetic lethality, pharmacologic PARP7 inhibition,
inhibitor response, treatment benefit, patient selection, or clinical utility.
No source pooling, post hoc lineage exclusion, threshold change, or proxy
rescue was used.

## Artifact receipts

- `context_ledger.csv`: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`
- `design_sensitivity.csv`: `b24e122734ed5d68787fed9cd2e49a30afa9a6d0e68fb4b1648a33270fa51637`
- `endpoint_scores.csv`: `0fe6f5be0e9f4fd79d852038a7ecb36ed4adf188b1c698075162f2b0bf491810`
- `inference.csv`: `c2ad9f57fcf78d3c89ee7c56c1e7ab456de40b4de532b798f4fb9dcd9bfaaf87`
- normalized `summary.json` digest: `4618dfde63fbc00553835965f3c051f70e12b981467d863033a45287d0fd1fd4`
- pre-endpoint receipt: `c1d108260fe014335f20ff3e195aa7fa41366ad02950fb26b62a7542c2f745a3`
