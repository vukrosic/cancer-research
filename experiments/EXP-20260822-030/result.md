# EXP030 result — composite BRCA1/2 damaging proxy to CIP2A dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate source families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `CIP2A (57650)` / cancerous inhibitor of PP2A from the frozen DepMap
  23Q4 naive CRISPR screen;
- exposure: composite damaging proxy when BRCA1 or BRCA2 matrix value is `1` or
  `2`;
- reference: both BRCA1 and BRCA2 matrix values are `0`;
- canonical roster SHA-256:
  `058842fec2d6750661de8d3109950f7e6376456baa564b5bd3cb49697fa3d083`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The candidate was selected outcome-blind from the BRCA–CIP2A/TOPBP1 literature.
The primary study reports CIP2A dependence in BRCA1- and BRCA2-deficient
isogenic cells and identifies the CIP2A–TOPBP1 axis:
[Nature Cancer study](https://www.nature.com/articles/s43018-021-00266-w).
EXP030 tests only a composite BRCA1-or-BRCA2 damaging-matrix proxy against a
genetic CIP2A screen endpoint; it does not recreate biallelic BRCA loss, HRD, or
functional BRCA status.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | -0.3196480938416422 | 1705 | 0.0005899941000589994 | [-0.45102639296187685, -0.18237536656891537] | 11 | +1.0 | FAIL |
| KY | -0.2144212523719165 | 527 | 0.06156938430615694 | [-0.46110056925996207, 0.03984819734345351] | 5 | +1.0 | FAIL |

Avana met the delta, permutation, bootstrap, and negative-lineage gates but
failed the no-positive-lineage gate. Its positive lineages included Testis
`+1.0`, Head and Neck `+0.23076923076923078`, and Pancreas
`+0.21052631578947367`.

KY met the effect-size and negative-lineage gates but failed permutation,
bootstrap, and no-positive-lineage gates. Its positive lineages included
Prostate `+1.0` and Uterus `+0.6666666666666666`.

Both source planning powers were below the frozen confirmatory threshold:
Avana `0.6686`, KY `0.4355`. The corrected pre-endpoint planning receipt is
documented separately and does not change the terminal claim.

## Interpretation boundary

The strongest allowed statement is: in the frozen DepMap 23Q4 cohorts, the
composite BRCA1-or-BRCA2 damaging-matrix proxy was negatively associated with
CIP2A dependency in both source families, but both source analyses were
lineage-heterogeneous under the preregistered gates. This does not establish a
robust two-source BRCA1/2–CIP2A dependency.

This does not establish biallelic BRCA1/2 loss, HRD, functional BRCA status,
causal synthetic lethality, pharmacologic CIP2A inhibition, inhibitor response,
treatment benefit, patient selection, clinical utility, or a confirmatory claim.
No source pooling, post hoc lineage exclusion, threshold change, or proxy rescue
was used.

## Artifact receipts

- `context_ledger.csv`: `34c142633cd4f9070a062ab6a501da5e575e555e9aa19f078120d0756153cb70`
- `design_sensitivity.csv`: `638c33df6c667698b771c4eea4f7b3d66868b80efd29fa936a9b221f511b33a2`
- `endpoint_scores.csv`: `f429f097a4211f5f852c00d75228b2652156d466ffd4aa4ec418456a06395702`
- `inference.csv`: `900e5acb2920ee0d8c0c93d1a5610fde4870f1dd16ec747161bc609612f23c0d`
- normalized `summary.json` digest: `4dca3f078addb236a98dcda123073a41b5d4cbbd58e97649b2f207ce5a5fe2af`
- pre-endpoint receipt: `c3e674ab7debc991c01ea3f8cf0c5b6ef9431b7aa902ea740b44434c8e9730e9`
