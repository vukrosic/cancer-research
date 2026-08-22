# Source and cohort provenance audit — 2026-08-22

## Purpose

This audit was performed before any MSI-stratified WRN outcome analysis. It decides
whether the next biological positive-control experiment can honestly be described as
an independent Broad-to-Sanger replication.

## Frozen official sources

- Cell Model Passports API: `https://api.cellmodelpassports.sanger.ac.uk`, API
  version 1.23.0 and observed data version 2.19.0.
- Model annotation: `model_list_20260814.csv`, timestamped 2026-08-14 by the
  official download index, SHA-256
  `eb43e92042ab430adabbbcf65e577459ac52d57df802eb388aea5865ff9b49aa`.
- Project Score 2 combined archive: indexed 2025-06-24. Its remote ZIP central
  directory contains combined fold-change, Bayesian-factor, scaled-Bayesian-factor,
  and binary matrices. The archive is not an untouched held-out source.
- Sanger raw-count archive: 2,848,002,413 bytes, last modified 2025-06-20. Its
  central directory contains 1,125 entries, principally per-screen gzipped sgRNA
  count files.

Official processing documentation states that Broad and Sanger corrected fold
changes were batch-corrected using overlapping cell lines for combined analysis.
Therefore `fc_clean_qn` is not accepted as final independent-replication evidence.
The API's source-labelled `bf` and `bf_scaled` values are retained for a separate
processing-sensitivity audit; their source labels alone are not treated as proof of
raw-data independence.

## Exploratory label-only cohort audit

The cohort was defined without reading WRN score values:

- `model_type == "Cell Line"`
- `tissue == "Large Intestine"`
- `cancer_type == "Colorectal Carcinoma"`
- `msi_status` exactly `MSI` or `MSS`
- one Cell Model Passports `model_id`
- API CRISPR record with `qc_pass == true`

Observed counts:

| Source | MSI | MSS | Total |
| --- | ---: | ---: | ---: |
| Broad | 7 | 12 | 19 |
| Sanger | 10 | 19 | 29 |
| Shared Broad/Sanger models | 6 | 7 | 13 |

An independent methods critic proposed a minimum of 8 MSI and 8 MSS models in each
source before these counts were reported. The historical Broad cohort therefore
fails that proposed adequacy gate. No threshold will be relaxed and no missing MSI
labels will be imputed after observing outcomes.

## Decision

Do not unseal the MSI–WRN effect test on this historical API cohort. First quantify
processing sensitivity in EXP-20260822-002, then either obtain a current Broad-native
release with adequate frozen labels or reconstruct source-separated scores under a
new preregistered child experiment.

## Preserved operational result

A slow download of the 199 MB combined archive was stopped at 68 MB after its remote
central directory established that it contained combined products. The incomplete
archive was moved to macOS Trash as
`Project_Score2_fitness_scores_Sanger_v2_Broad_21Q2_20250624.partial.zip`; it is
recoverable until Trash is emptied. The current model annotation was retained.
