# EXP031 result — SMAD4 damaging proxy to BRD4 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `BRD4 (23476)` / bromodomain containing 4 from the frozen DepMap
  23Q4 naive CRISPR screen;
- exposure: SMAD4 damaging proxy when the matrix value is `1` or `2`;
- reference: SMAD4 matrix value `0`;
- canonical roster SHA-256:
  `3532122677a66a5fedbd664cb452d7dcd7ea6d179556ca4df1d1dbe4a81cef62`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from a study reporting selective
BET-inhibitor sensitivity after SMAD4 loss in colorectal cancer cells:
[Oncogene study](https://www.nature.com/articles/s41388-020-01580-w).
EXP031 tests only a SMAD4 damaging-matrix proxy against genetic BRD4 knockout
dependency; BRD4 is used as one genetic proxy for the BET mechanism, not as a
claim about every BET inhibitor.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | +0.08886509635974305 | 1868 | 0.8131618683813162 | [-0.10599571734475374, 0.2815845824411135] | 4 | +1.0 | FAIL |
| KY | -0.049079754601226995 | 652 | 0.35817641823581764 | [-0.29141104294478526, 0.19631901840490798] | 3 | +0.5135135135135135 | FAIL |

Avana was positive in aggregate, uncertain, and highly heterogeneous. It failed
the direction, effect-size, permutation, bootstrap, negative-lineage, and
no-positive-lineage gates; notable positive lineages included Vulva/Vagina
`+1.0`, Head and Neck `+0.6833333333333333`, and Biliary Tract
`+0.3793103448275862`.

KY was near-null and uncertain. It failed the effect-size, permutation,
bootstrap, negative-lineage, and no-positive-lineage gates; Lung was
`+0.5135135135135135` and Ovary/Fallopian Tube was `+0.38461538461538464`.

Both source planning powers were below the frozen confirmatory threshold:
Avana `0.6414`, KY `0.4630`.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
SMAD4 damaging-matrix proxy did not show a robust source-consistent association
with genetic BRD4 dependency. This does not refute pharmacologic BET biology;
the proxy, endpoint, cell-line composition, and genetic-versus-drug mechanism
are not equivalent.

This does not establish functional SMAD4 loss, BET-inhibitor sensitivity, BRD4
inhibitor efficacy, a MYC mechanism, causal synthetic lethality, treatment
benefit, patient selection, clinical utility, or a confirmatory claim. No source
pooling, post hoc lineage exclusion, threshold change, or proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `c1305ac91f5d1cd9064a3c00cb2980dac77b2fbf99990381ac34d25cf5d33b1e`
- `design_sensitivity.csv`: `6a0d1e9605c928060aed9884d82b99b235351bdf5617df6abf8e85191b6311d1`
- `endpoint_scores.csv`: `0832a49757dc75736b9f4a59bb85a88d702138e7cce233611c3936253edacac8`
- `inference.csv`: `2504a691f67580f51ad844fb99c462111d6717be97e96f4acc58a290f20a22f6`
- normalized `summary.json` digest: `466ee51b8957657c69b98b0dd2fc8a6d8089ea602ddd217eceff55f23fa10daf`
- pre-endpoint receipt: `4e6eace8f2ef6201a91354a8717d8d9ab8f5a2272176873acc12accf518c96c7`
