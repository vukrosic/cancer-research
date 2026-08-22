# EXP-20260822-001 result

Status: **PASS with a documented protocol deviation**  
Claim tier: **T0 engineering**  
Run date: 2026-08-22

## Outcome

All preregistered gates passed on the official Cell Model Passports API data:

- 8/8 panel genes had 177 paired Broad/Sanger model measurements (gate: >=6 genes
  with >=100 pairs).
- Median gene-wise Spearman rho was 0.4222 (gate: >=0.30).
- 8/8 eligible genes had positive rho (gate: >=75%).

Per-gene rho ranged from 0.1475 for BRAF to 0.6345 for PIK3CA. The BRAF bootstrap
interval crossed zero; therefore this result does not say every individual dependency
profile is stable. Threshold-class agreement at -0.5 ranged from 0.723 to 0.944,
but this unbalanced metric is dominated by joint non-dependencies for some genes and
is not evidence of dependency-class concordance by itself.

## Attempt history

Attempt 1 returned zero pairs because sparse-field API selection omitted `source` and
`qc_pass`. Its output is preserved in `results/summary_attempt1.json`. The implementation
was corrected to request full records with a new cache key. No panel, score, threshold,
exclusion, seed, or gate changed. This was an implementation error, not the only retry
type explicitly permitted by the frozen stop rule, so the retry is a **protocol
deviation** even though an independent audit confirmed scientific invariance. The
final machine-readable result is
`results/summary.json`, including SHA-256 hashes for every cached response.
The post-audit recomputation with corrected threshold terminology and full 2x2 counts
is `results/audit_verification.json`.

## Interpretation

The data-access and pairing approach is viable on the target Mac and retains enough
cross-source signal to proceed. This is not a new cancer finding and not evidence that
any gene is a therapeutic target.

The `fc_clean_qn` score is a harmonized, quantile-normalized field in the Sanger-hosted
cross-study resource. It is appropriate for this engineering gate but cannot serve as
the final independent-replication endpoint because harmonization may improve agreement.
Later experiments must preserve source-separated processing or use independently
processed release matrices before evaluating a biomarker claim.

## Limitations

- Cell Model Passports currently incorporates a historical Broad release rather than
  the current DepMap 26Q1 matrix; release stability remains untested.
- The eight-gene panel was hand-picked and is not a random or comprehensive gene sample.
- The experiment did not use lineage, mutation, MSI, expression, or copy-number labels.
- Correlation and threshold-class agreement do not demonstrate a mechanism, druggability,
  tumour selectivity, safety, or patient relevance.

## Decision

Proceed to a separate data-provenance and cohort-size gate for source-separated MSI
colorectal models. Do not unseal the WRN effect test until MSI/MSS counts, identifier
mapping, and source-specific score provenance are frozen and adequate.
