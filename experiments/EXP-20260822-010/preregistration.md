# EXP-20260822-010 preregistration

## Question

Are the 10 EXP-005 models with absolute Avana-versus-KY WRN dependency-percentile
gaps at least 0.25 robust to removing any one eligible WRN guide from either source
library?

This is an exhaustive endpoint-aggregation robustness audit. It directly tests
sensitivity to one-guide omission and is intentionally derived from the same raw
assay data as the frozen naïve WRN endpoint. It is not independent replication, a
causal guide-effect test, or a new biological dependency test.

## Evidence and endpoint boundary

EXP-005 WRN scores, percentiles, gaps, and the 10 flagged ModelIDs were already
unsealed. EXP-010 is therefore a **preregistered exhaustive derived robustness audit
after endpoint unsealing**.

Before freezing this protocol, the orchestrator and an independent methods critic
inspected official schemas, guide identities, sequence mappings, file availability,
and adequacy only. No leave-one-guide-out score, percentile, gap, transition, or
robustness result was computed. The critic's initial decision was NO-GO as written
and GO after the operational amendments frozen here.

## Frozen inputs, population, and eligible guides

- DepMap Public 23Q4 Figshare article 24667905 version 2.
- Pre-Chronos `AvanaLogfoldChange.csv` and `KYLogfoldChange.csv`, official file IDs,
  byte sizes, and MD5 receipts frozen in the manifest.
- Official guide maps, screen-sequence map, screen QC report, source-specific naïve
  gene-score matrix, EXP-003 denominator identities, and EXP-005 gap file are
  SHA-256 frozen.
- Full ranking denominators are exactly 103 unique source screens: Avana 25 / KY 30
  Large Intestine and Avana 22 / KY 26 Ovary.
- Paired set is exactly the 34 EXP-005 ModelIDs, 17 per tissue.
- Primary flagged set is exactly the 10 rows in the hash-frozen EXP-005 gap file
  where `discordant_ge_0_25=True`.

Eligible guide rule is `Gene == "WRN (7486)"`, `UsedByChronos=True`, one genomic
alignment, and blank `DropReason`. It must yield exactly the four frozen Avana and
five frozen KY guide sequences listed in the manifest. No guide may be added,
removed, selected, or reclassified after execution begins.

## Frozen raw reconstruction

For source `s`, eligible guide `g`, and frozen screen `j`, let `Q_s,j` be the exact
`ScreenSequenceMap.csv` rows that:

- match the frozen ScreenID and source library;
- have `ExcludeFromCRISPRCombined=False`; and
- map to a unique finite column in the source LFC matrix.

The count of `Q_s,j` must equal `nIncludedSequences` in the exact frozen QC row.
Reject duplicate screen/model/source/sequence joins, missing matrix columns, missing
guide rows, and nonfinite retained values.

Define guide mean and reconstructed screen score:

`G_s,g,j = mean_q in Q_s,j LFC_s,g,q`

`W_s,j = median_g in eligible_guides_s G_s,g,j`.

Each of the 103 denominator model-source records is required to have exactly one
frozen screen. If this identity contract drifts, stop; do not introduce a new screen
or model collapse rule.

## Baseline no-drift gate

Before any omission, reconstruct all 103 WRN screen scores and compare them with the
official source-specific `ScreenNaiveGeneScore.csv` values. Require:

- exactly 103 comparisons;
- `abs(reconstructed - official) <= 1e-8` for every record with `rtol=0`;
- finite scores and unchanged identities.

Record the maximum absolute discrepancy. Any failure stops EXP-010. Do not tune the
sequence filter, joins, guide rule, aggregation, or tolerance after seeing a
discrepancy.

## Nine frozen global perturbations

After the baseline gate passes, create exactly nine configurations:

1. omit each of the four Avana guides in turn from every Avana denominator screen,
   retaining three Avana guides and leaving KY at baseline;
2. omit each of the five KY guides in turn from every KY denominator screen,
   retaining four KY guides and leaving Avana at baseline.

Each omission is global and library-specific. No screen-specific guide selection,
sequence deletion, guide pair omission, two-library simultaneous omission, or
outcome-based perturbation is allowed.

Every configuration must preserve all 103 source-screen identities and finite guide
means/scores. Stop on any missing value or identity drift.

## Full-denominator percentiles and gaps

For each baseline or perturbed source `s`, tissue `t`, and model `i`, recompute the
dependency percentile from the complete frozen source-by-tissue denominator:

`P_s,t(i) = (n_s,t - ascending_average_midrank(W_s,t(i))) / (n_s,t - 1)`.

More negative WRN scores therefore receive higher dependency percentiles. Never rank
only the 34 pairs, jitter ties, or change the four denominator sizes.

For each paired model and configuration, define
`D(i) = abs(P_Avana,t(i) - P_KY,t(i))`. Apply the flag threshold as exact
`D(i) >= 0.25`; do not add a numerical tolerance.

## Frozen primary criterion

For each of the 10 baseline-flagged models, define **fully robust** as retaining
`D(i) >= 0.25` under all nine single-guide omissions.

EXP-010 passes the descriptive robustness criterion only if at least **8 of the 10**
baseline-flagged models are fully robust. No secondary result can rescue failure.

## Frozen secondary reporting

- Cohort fraction retaining the flag under every Avana omission (4/4).
- Cohort fraction retaining the flag under every KY omission (5/5).
- Per-model Avana, KY, and all-nine robustness indicators for the locked 10 models.
- Per-model minimum, median, and maximum gap across all 10 configurations (baseline
  plus nine omissions), clearly labeled as such.
- Baseline equal-tissue ordering theta and the minimum/maximum theta across the nine
  omissions, using EXP-005's equal-tissue frozen-percentile correlation.
- Unique baseline-unflagged models becoming flagged at least once.
- Total unflagged-to-flagged model-configuration transitions out of `24 * 9 = 216`.

The nine perturbations are dependent deterministic stress tests, not independent
tests. No p-value, bootstrap interval, multiplicity correction, guide ranking,
subgroup rescue, or post hoc combined perturbation will be computed.

## Median-parity limitation

Avana changes from a four-guide median (mean of the middle two) to a three-guide
median. KY changes from a five-guide median to a four-guide median (mean of the
middle two). Source-specific omission magnitudes therefore are not directly
comparable estimates of guide influence. The locked binary stress test remains
valid, but guide-level causal language is forbidden.

## Maximum claim

If the primary criterion passes: in this frozen two-tissue, full-denominator
reconstruction, at least 8 of 10 previously gap-flagged models remained flagged
after every eligible single-guide omission.

This would not establish independence, causality, a specific bad guide, immunity to
multi-guide omissions, exclusion of library-design effects, a WRN biological
mechanism, therapeutic actionability, patient benefit, or clinical relevance.
