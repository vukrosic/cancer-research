# EXP-20260822-004 preregistration and design gate

## Question

Among the models present in both Broad Avana and Sanger KY within the four EXP-003
tissues, is source-specific WRN dependency ordering reproducible within tissue?

This asks about model-level measurement reliability. It is distinct from EXP-003's
group-level MSI–MSS contrast.

## Outcome blinding boundary

Before this design gate was frozen, EXP-003's group effects and model-score table
were public. The orchestrator had not computed any cross-source model-level WRN rank
correlation, percentile gap, or outlier ordering. The methods critic was explicitly
forbidden to inspect or compute those outcomes.

Model identity, tissue, label, source availability, and overlap counts were known:

| Tissue | Distinct overlapping models |
|---|---:|
| Endometrium | 5 |
| Large Intestine | 17 |
| Ovary | 17 |
| Stomach | 8 |
| Total | 47 |

The 47 are distinct ModelIDs available in both sources, not model–tissue duplicates.

## Frozen endpoint and rank definition

If the adequacy gate passes, use only the EXP-003 source-separated
`ScreenNaiveGeneScore.csv` WRN endpoint. For model `i` in source `s`, tissue `t`,
define stronger-dependency percentile using all eligible models in that source×tissue
cohort:

`P_s,t(i) = (n_s,t - ascending_midrank(score_s,t,i)) / (n_s,t - 1)`.

Higher percentile means stronger WRN loss of fitness. Ties receive average midranks.
One endpoint per model/source/tissue is allowed; multiple eligible screens would be
collapsed by median exactly as in EXP-003.

## Intended primary estimand

Compute Spearman correlation of the paired percentiles separately in each tissue,
then take the equal-tissue mean of the four correlations. A pooled model-weighted
correlation is secondary only.

The intended inference is 100,000 one-sided permutations of KY percentiles within
tissue and 10,000 paired-model bootstraps within tissue, seed 20260825.

## Adequacy and pass gates

The independent outcome-blind methods review froze these minimums:

- at least 40 distinct overlap models overall;
- at least 8 paired models in **every** tissue;
- no constant source rank vector within any tissue;
- complete finite endpoints for the pre-frozen cohort;
- no post-outcome cohort repair.

Only if those pass may the outcome gates be evaluated:

- equal-tissue mean Spearman correlation at least 0.50;
- one-sided stratified permutation p at most 0.05;
- 95% bootstrap lower bound greater than 0.20;
- no tissue-specific correlation below -0.20.

## Stop condition

If any adequacy criterion fails, stop as `FAIL_T0_ADEQUACY`. Do not compute the
cross-source rank outcomes, remove a tissue, pool tissues, or lower the minimum inside
this experiment. A narrower population requires a new child experiment.

## Maximum claim

If all gates pass: in this frozen four-tissue overlap set, source-specific CRISPR WRN
dependency rankings showed reproducible within-tissue ordering across Avana and KY.

This would be a measurement-agreement result conditional on shared cell models, not a
new biological mechanism, therapeutic result, clinical claim, or proof of complete
source independence.

