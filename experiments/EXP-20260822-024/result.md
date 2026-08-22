# EXP-20260822-024 result — KMT2D damaging status to KMT2C dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `KMT2C (58508)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: KMT2D matrix value `1` or `2`, labeled `damaging`;
- reference: KMT2D matrix value `0`, labeled `matrix_intact`;
- canonical roster SHA-256:
  `e8f440a118065e4fc23535dca196c03b8c9a08b9a4f4348516f214d19b2e9164`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from metadata and an emerging 2026
AACR CRISPR report of KMT2C dependency in KMT2D-null lymphoma:
[AACR abstract 7060](https://doi.org/10.1158/1538-7445.AM2026-7060). That
report does not convert this damaging matrix into functional KMT2D loss or
justify pan-cancer generalization.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.1779171894604768 | 3985 | 0.00977990220097799 | [-0.3259723964868256, -0.024843161856963614] | 10 | +1.0 | FAIL |
| KY | +0.10040160642570281 | 747 | 0.7971520284797152 | [-0.14330655957161975, 0.3413654618473896] | 5 | +1.0 | FAIL |

Avana passed the directional, permutation, and bootstrap gates but missed the
frozen effect-size threshold (`delta <= -0.20`) and failed lineage consistency.
Positive lineage deltas included Ampulla of Vater `+1.0`, Bone
`+0.8571428571428571`, and Breast `+0.7142857142857143`.

KY was positive rather than negative and failed the directional, effect-size,
permutation, bootstrap, and lineage-consistency gates. Bone and Pancreas were
both `+1.0`; Bowel was `+0.45454545454545453`.

The sources therefore do not provide a clean replication. Avana planning power
was `0.8433`, but KY planning power was `0.5120`; the paired experiment is
permanently feasibility-only.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
damaging-matrix KMT2D proxy showed a heterogeneous, source-specific
association with KMT2C knockout dependency—negative in Avana but positive and
uncertain in KY—and failed the complete preregistered gate contract.

This does not establish functional KMT2D loss, KMT2D-null biology,
lymphoma-specific causality, paralog causality, KMT2C inhibitor sensitivity,
treatment benefit, patient selection, or clinical utility. No source pooling,
post hoc lineage exclusion, threshold change, or endpoint-derived rescue was
used.

## Artifact receipts

- `context_ledger.csv`: `95af290eb5384cf360156709c42087e3c5013ca9087b617f48dde3ec15ee0c49`
- `design_sensitivity.csv`: `e33a2556ac46ca617749095e8d78f8bc6210a2c62ed9349f9fb4c0125fdeb4e8`
- `endpoint_scores.csv`: `f91af4e96a2b0598249cbce23fb4d84dc6dd5c71210472c37232681d6a96baf7`
- `inference.csv`: `46b6e6778098baf5486112f5817df1133f718386f6dfb5876d95176c1674c235`
- normalized `summary.json` digest: `4efb6a9fec2a73e25e133c29d8abd7540af0c6868e535270d63e3e5f2703c4ab`
- pre-endpoint receipt: `9d6543bc1457eea3741b4eda3c947b3de20de743908126a63e0fb1d00c6948d1`
