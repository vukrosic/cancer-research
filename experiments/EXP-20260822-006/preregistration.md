# EXP-20260822-006 preregistration

## Question

Are source-specific screen-QC-rank asymmetries associated with source-specific WRN
rank discordance in the frozen Large Intestine and Ovary overlap set?

This is an observational measurement audit. It does not test whether QC asymmetry
causes or biologically explains WRN disagreement.

## Evidence and blinding boundary

EXP-005 WRN percentiles, gaps, and outlier identities were already unsealed. EXP-006
is therefore a **preregistered derived observational analysis after endpoint
unsealing**, not blinded confirmation.

Before freezing this protocol, neither the orchestrator nor the outcome-blind critic
computed or inspected any association between a WRN gap and a QC metric or composite.
All thresholds, metrics, transformations, and inferential rules below were fixed from
provenance and availability only.

## Frozen population, units, and independence gate

- Outcome population: exactly the 34 paired EXP-005 ModelIDs: 17 Large Intestine and
  17 Ovary.
- QC percentile denominators: all eligible source×tissue records from EXP-003,
  including source-only models: Avana 25 / KY 30 Large Intestine and Avana 22 / KY
  26 Ovary, 103 model-source records total.
- Unit: one `ModelID × tissue × source` screen record.
- Each of the 103 records maps to exactly one unique ScreenID; no ScreenID or
  model-source record is shared, so model-pair inference does not duplicate a QC
  cluster.
- All five metrics below are finite for all 103 records.
- The complete denominators and 34-pair population are immutable.

Stop before association analysis if any count, identity, uniqueness, hash,
completeness, or nonconstancy invariant fails.

## Frozen QC metrics and circularity audit

Primary composite metrics from `AchillesScreenQCReport.csv`:

1. `ScreenNNMD`;
2. `ScreenROCAUC`;
3. `ScreenFPR`;
4. `ScreenMedianEssentialDepletion`;
5. `ScreenMedianNonessentialDepletion`.

These are pre-Chronos screen-level control-separation/depletion metrics. The official
23Q4 common-essential and nonessential control lists were hash-verified, and `WRN
(7486)` is absent from both. The exposure therefore does not directly include the
WRN endpoint. No jointly corrected or WRN-containing score is used.

The five-metric equal-weight composite is an unvalidated descriptive index. The
metrics are correlated and equal weighting is not asserted to be optimal.

## Source-specific quality percentiles

Transform each raw metric so higher means conventionally better screen quality:

- NNMD: `-ScreenNNMD` (more negative raw NNMD is better);
- ROCAUC: `ScreenROCAUC`;
- FPR: `-ScreenFPR` (lower raw FPR is better);
- essential depletion: `-ScreenMedianEssentialDepletion` (more negative is better);
- nonessential depletion: `-abs(ScreenMedianNonessentialDepletion)` (closer to zero
  is better).

Within every source×tissue full denominator, assign ascending average midranks and
define `Q = (midrank - 1) / (n - 1)`. Higher Q means better relative QC. Never jitter
ties; FPR ties receive average midranks.

For paired model `i` and metric `m`, define source-rank asymmetry:

`A_m(i) = |Q_Avana,m(i) - Q_KY,m(i)|`.

Primary exposure:

`A_composite(i) = mean_m A_m(i)` over the five metrics with equal weights.

Require the final composite to be finite and nonconstant within each tissue.

## Frozen outcome and primary estimand

Outcome is EXP-005's frozen absolute WRN dependency-percentile gap `D(i)`.

Within each tissue, compute average midranks of `A_composite` and `D` exactly once.
Spearman rho is Pearson correlation of those frozen ranks. Define the equal-tissue
mean:

`theta = (rho_Large_Intestine + rho_Ovary) / 2`.

Do not use a pooled 34-model correlation as primary.

## Inference

- Seed: 20260827.
- Permutation: 100,000 repeats. Hold WRN-gap ranks fixed and independently permute
  composite-QC-asymmetry ranks among ModelIDs within each tissue. Use the positive
  tail and plus-one p-value `(1 + count(theta_perm >= theta_obs)) / 100001`.
- Bootstrap: 10,000 repeats. Resample paired ModelIDs with replacement separately
  within each tissue. Correlate the already-frozen rank pairs directly. Never rerank
  duplicated bootstrap observations.
- Report the percentile 95% interval.

## Frozen adequacy and pass gates

Adequacy requires all identity/completeness gates above, at least 30 total paired
models, at least 15 in each tissue, and finite nonconstant primary vectors.

All outcome gates must pass:

1. point-target gate `theta >= 0.40`;
2. one-sided within-tissue permutation `p <= 0.05`, testing no positive association;
3. separate positive practical-bound gate: 95% bootstrap lower bound `> 0.10`;
4. neither tissue-specific rho below `-0.20`.

The permutation p-value does not test theta >= 0.40. No threshold, metric, weight,
transformation, cohort, or tissue may change after outcome computation.

## Secondary analyses

The five individual metric asymmetry correlations are descriptive only, with no
p-values and no ability to alter the composite or primary interpretation. Also report
composite distributions for EXP-005 gap-flagged versus unflagged models and a model-
level audit table. No PCA, learned weights, metric exclusion, or secondary rescue is
allowed.

## Maximum claim

If all gates pass: source-specific QC-rank asymmetry was positively associated with
WRN-rank discordance in this frozen two-tissue cell-model set.

This would not show causation, explain a biological mechanism, validate the composite
as a general QC score, establish a new dependency, or support therapeutic or clinical
claims.

