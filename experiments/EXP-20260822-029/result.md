# EXP029 result — composite BRCA1/2 damaging proxy to POLQ dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `POLQ (10721)` / DNA polymerase theta from the frozen DepMap 23Q4
  naive CRISPR screen;
- exposure: composite damaging proxy when BRCA1 or BRCA2 matrix value is `1` or
  `2`;
- reference: both BRCA1 and BRCA2 matrix values are `0`;
- canonical roster SHA-256:
  `058842fec2d6750661de8d3109950f7e6376456baa564b5bd3cb49697fa3d083`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from the BRCA1/2 synthetic-lethal
literature and frozen metadata. The SYLVER study describes BRCA1/2 synthetic
lethal genes including POLQ and corroborates the direction with isogenic
screens: [Nature Genetics study](https://www.nature.com/articles/s41588-025-02108-2).
This experiment tests only a composite damaging-matrix proxy against a genetic
POLQ screen endpoint; it does not recreate biallelic BRCA loss, HRD, functional
BRCA status, or a pharmacologic POLQ experiment.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.07683284457478005 | 1705 | 0.22189778102218977 | [-0.23870967741935484, 0.08504398826979472] | 8 | +1.0 | FAIL |
| KY | -0.3738140417457306 | 527 | 0.003109968900310997 | [-0.6091081593927894, -0.10815939278937381] | 6 | +0.025974025974025976 | PASS |

Avana was weakly negative but uncertain. It failed the effect-size,
permutation, bootstrap, and no-positive-lineage gates; its positive lineage
effects included Lung `+0.48623853211009177`, Testis `+1.0`, and Pancreas
`+0.21052631578947367`.

KY was strongly negative under the frozen estimator and passed all five nominal
gates. That source-specific result cannot upgrade the paired experiment: the
Avana result failed, and both source planning powers were below the frozen
confirmatory threshold.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
composite BRCA1-or-BRCA2 damaging-matrix proxy showed source-discordant POLQ
associations—strong and internally consistent in KY, but weak and
lineage-heterogeneous in Avana. This does not establish a robust two-source
BRCA1/2–POLQ dependency.

This does not establish biallelic BRCA1/2 loss, HRD, functional BRCA status,
causal synthetic lethality, pharmacologic POLQ inhibition, inhibitor response,
treatment benefit, patient selection, or clinical utility. No source pooling,
post hoc lineage exclusion, threshold change, or proxy rescue was used.

## Artifact receipts

- `context_ledger.csv`: `34c142633cd4f9070a062ab6a501da5e575e555e9aa19f078120d0756153cb70`
- `design_sensitivity.csv`: `4727e363ec72681f7a63c6870f99d5e06bd24573c91efe2bbf178753d4a8d0ce`
- `endpoint_scores.csv`: `5acafcf780f13029203cc7b14b865be6f7685254721f0622e9048899845081f1`
- `inference.csv`: `9209cb6bd7b25de299cde230ae0304690dd17d29cc97d473b6f17de93df5b61c`
- normalized `summary.json` digest: `32dc58f9f25927cf0b3c31fdcba0acea23883f528ceeccebdb8b5f71b679108d`
- pre-endpoint receipt: `19dfacfe10b64e9e9ef57b593f7b055876cb2d3e51ad3c35fba5bb3653e88927`
