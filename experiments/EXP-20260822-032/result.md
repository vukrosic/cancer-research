# EXP032 result — SMAD4 damaging proxy to AURKA dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `AURKA (6790)` / aurora kinase A from the frozen DepMap 23Q4 naive
  CRISPR screen;
- exposure: SMAD4 damaging proxy when the matrix value is `1` or `2`;
- reference: SMAD4 matrix value `0`;
- canonical roster SHA-256:
  `3532122677a66a5fedbd664cb452d7dcd7ea6d179556ca4df1d1dbe4a81cef62`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from a study reporting SMAD4-loss
and AURKA-inhibitor sensitivity in colorectal cancer models
([Oncogene study](https://www.nature.com/articles/s41388-022-02293-y)). EXP032
tests only a SMAD4 damaging-matrix proxy against genetic AURKA knockout
dependency; it is not a pharmacology experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `+0.0952890792` | 1868 | 0.8276317237 | `[-0.1038811563, 0.2912205567]` | 6 | `+1.0` | FAIL |
| KY | `+0.1196319018` | 652 | 0.8237517625 | `[-0.1288343558, 0.3588957055]` | 3 | `+0.552` | FAIL |

Avana was positive rather than negative, with broad uncertainty and lineage
heterogeneity. KY was also positive rather than negative, with only three
negative lineage estimates and a maximum positive lineage delta of `+0.552`.
Both sources failed the direction, effect-size, permutation, bootstrap, and
no-positive-lineage gates; KY also failed the minimum negative-lineage gate.

Both source planning powers were below the frozen confirmatory threshold:
Avana `0.6502`, KY `0.4713`.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
SMAD4 damaging-matrix proxy did not show a robust negative or source-consistent
association with genetic AURKA dependency. This does not refute
SMAD4-loss/AURKA-inhibitor biology; the proxy, endpoint, cell-line composition,
and genetic-versus-drug mechanism are not equivalent.

This does not establish functional SMAD4 loss, AURKA-inhibitor efficacy,
spindle-checkpoint mechanism, causal synthetic lethality, treatment benefit,
patient selection, clinical utility, or a confirmatory claim. No source pooling,
post hoc lineage exclusion, threshold change, or proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `c1305ac91f5d1cd9064a3c00cb2980dac77b2fbf99990381ac34d25cf5d33b1e`
- `design_sensitivity.csv`: `36f1f123cba85cbccc6d673de64a80c40ad2024fc080f450c8459e8831ec24ad`
- `endpoint_scores.csv`: `18d0f2b12209e22c08f34998d13d0574bfae9b8dccad512aff3506715eafe6a5`
- `inference.csv`: `27101607c73a62ec8a92c7004516c06140efb1ee4248891c318bae63d4cd969f`
- normalized `summary.json` digest: `8d66542d4c6c07529ffcaed68e1ebb93c3b9a09734bff4ec9b268665949488aa`
- pre-endpoint receipt: `3be8e09e1f6e5bcf6bb23c70067aa624f1ef666a0ed2fa436d08e2aeeff172e5`
