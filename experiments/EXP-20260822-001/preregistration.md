# EXP-20260822-001 — source-paired API and signal gate

Preregistered before running on 2026-08-22.

## Purpose and tier

T0 engineering gate. Determine whether the official source-tagged API provides enough
paired Broad/Sanger measurements and preserves context-selective dependency signal for
the planned research. This experiment makes no novelty or biological discovery claim.

## Hypothesis

Across the frozen panel `WRN, BRAF, KRAS, NRAS, EGFR, PIK3CA, CTNNB1, MDM2`:

1. At least 6 genes have at least 100 QC-passing cell models measured by both sources.
2. Median gene-wise Broad–Sanger Spearman correlation is at least 0.30.
3. At least 75% of eligible genes have positive correlation.

Failure of any gate rejects the current API/score choice for downstream experiments.

## Frozen analysis

- Source: Cell Model Passports API v1.23.0, observed data version 2.19.0.
- Score: `fc_clean_qn` only.
- Unit: unique model ID and source; duplicates collapse by median.
- Exclusion: missing score, unknown source, explicit `qc_pass=false`, unpaired model.
- Primary: median gene-wise Spearman correlation.
- Secondary: per-gene Pearson correlation, MAE, dependency-sign agreement at -0.5,
  1,000-resample Spearman bootstrap interval, one-sided 1,000-permutation null.
- Seed: 20260822 plus fixed gene offset.
- No panel, threshold, score, or exclusion changes after evaluation.

## Stop rule

One run after tests pass. Network failures may be retried without changing the
analysis. A scientific gate failure creates a new child experiment; it is not tuned
away.

Implementation note recorded before retry: attempt 1 used the API's sparse-field
parameter, which removed `source` and `qc_pass` from every returned record and made
pairing impossible. The attempt is preserved as `results/summary_attempt1.json`.
The retry requests full records; all scientific inputs and gates remain frozen.
