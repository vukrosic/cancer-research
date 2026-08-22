# EXP-20260822-026 result — PTEN proxy status to PAPSS1 dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `PAPSS1 (9061)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: PTEN matrix value `1` or `2`, labeled `damaging`;
- reference: PTEN matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `73222b7a148f333399d580107e1ab64672b0920678f3a2a9789b3440f9c2d953`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and the Nature Cancer
translational dependency map:
[Nature Cancer study](https://doi.org/10.1038/s43018-024-00789-y). That work
supports PAPSS1/PAPSS2 collateral lethality in patient-translational models,
with PAPSS2 loss near PTEN, and reports that the interaction is not detectable
in ordinary DepMap cell lines. This experiment uses a PTEN mutation proxy; it
does not recreate PTEN deletion or PAPSS2 co-deletion.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.03214552703712933 | 4013 | 0.3364666353336467 | [-0.16321953650635435, 0.09744580114627444] | 11 | +1.0 | FAIL |
| KY | +0.2073976221928666 | 757 | 0.9620903790962091 | [0.003963011889035667, 0.40290620871862615] | 3 | +0.9459459459459459 | FAIL |

Avana was near-null and failed the effect-size, permutation, bootstrap, and
lineage-consistency gates. Positive lineage deltas included Liver `+1.0`,
Prostate `+0.7142857142857143`, Breast `+0.43243243243243246`, and Esophagus/
Stomach `+0.30392156862745096`.

KY was positive rather than negative and failed every primary gate. Its largest
positive lineage deltas included Lung `+0.9459459459459459`, Head and Neck
`+0.8125`, and Bowel `+0.552`.

Avana planning power was `0.8526`, but KY planning power was `0.5377`; the
paired experiment is permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix PTEN proxy did not show a reproducible negative association
with source-specific PAPSS1 knockout dependency—Avana was near-null and KY was
positive and heterogeneous—and neither source passed the complete
preregistered gate contract.

This is compatible with, but does not prove, the reported patient-versus-cell-
line transport gap. It does not establish PTEN deletion, PAPSS2 co-deletion,
patient tumor biology, causal collateral lethality, PAPSS1 inhibitor
sensitivity, treatment benefit, patient selection, or clinical utility. No
source pooling, post hoc lineage exclusion, threshold change, or endpoint-
derived rescue was used.

## Artifact receipts

- `context_ledger.csv`: `48bf8b95574dc6b79acdb31acbb08cbc9166ffd4c04de600142df9c03baaa11b`
- `design_sensitivity.csv`: `7cb02134904ee4ecbbb1dce4b72e6c712fcb12ad17ae7d19e0d86ccf239502ed`
- `endpoint_scores.csv`: `b9b0c7003a9a0e635a7998f56865ec389a33a8726629e7986a96238904995005`
- `inference.csv`: `059c58b1ec74981afe6b979365a39ec3849a41d020cda5623d3d5e9f98e88c9a`
- normalized `summary.json` digest: `722cc5130581630c008a74047a2a2f9f84b478ee5aa17df76146e2f82909dc6d`
- pre-endpoint receipt: `761192af9227ae38583d3aa0d21cbbb2236775fb2737d340671b4ff6633100d8`
