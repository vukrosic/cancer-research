# EXP-20260822-013 preregistration

## Question

Within the frozen 23Q4 two-tissue paired-model cohort, is source-relative Chronos-
inferred model-efficacy discordance positively associated with the frozen WRN
percentile gap between Avana and KY?

This is a narrow assay-reliability association audit, not a biological discovery.
The efficacy and growth-rate parameters are inferred from the same CRISPR data
family as the WRN endpoint, so shared-input and mechanical association are possible.
The result cannot show that assay efficacy causes WRN discordance.

## Evidence and lineage boundary

- EXP-005's 34 WRN percentile gaps and selected paired models were already unsealed;
  EXP-013 is a preregistered derived observational analysis after endpoint unsealing.
- EXP-006, EXP-008, EXP-009, and EXP-012 remain separate negative or bounded audits.
  No result from those experiments may be combined with EXP-013 or used as a rescue.
- No efficacy/growth association with the WRN gap has been computed before this
  protocol is frozen.

## Frozen inputs and exact source mapping

- DepMap Public 23Q4 local `CRISPRInferredModelEfficacy.csv`, SHA-256
  `a64065456d8d1e83d2fac94fc7e3ae28e65272cd2a45c3fa969848555f0b7aa0`.
- DepMap Public 23Q4 local `CRISPRInferredModelGrowthRate.csv`, SHA-256
  `4f2f4a9f80af1e9862319156f9a8de38d677797074823bebec7853060550f29c`.
- Hash-frozen EXP-003 model/source/tissue denominator table, SHA-256
  `072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654`.
- Hash-frozen EXP-005 `model_percentile_gaps.csv`, SHA-256
  `f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a`.

Exact source mapping is fixed:

- Avana → `Achilles-Avana-2D`;
- KY → `Achilles-KY-2D`.

Join inferred parameters only by exact `ModelID`. The upstream model-score table
establishes the 103 source/tissue denominator identities and the 34 paired models;
the inferred parameter files are ModelID-level inputs, not ScreenID-level
measurements.

Expected full denominators are Avana/KY 25/30 in Large Intestine and 22/26 in
Ovary, with exactly 17 paired models per tissue and 34 total.

## Outcome-blind adequacy and execution order

Before opening or hashing the EXP-005 gap file, verify both parameter-file hashes,
headers, unique ModelIDs, exact source columns, finite values, and domains:

- efficacy: finite `0 < value <= 1`;
- growth rate: finite `value > 0`.

Require all 103 frozen source-specific denominator records to map exactly once to a
finite value in their own source column. The 34 paired models must have both source
values; the 35 unpaired denominator records are not required to have an
opposite-source value, and an opposite-source blank is expected and unused. Require
each tissue's paired efficacy exposure to be finite, nonconstant, have at least 10
distinct values, and have no tied exposure level containing more than 8 of 17 paired
models. Stop without association or inference on any failure.

Write the complete 103-row pre-outcome parameter ledger before loading the outcome,
including ModelID, source, tissue, raw efficacy, raw growth rate, and each
full-denominator within-source×tissue percentile. The ledger is source-specific for
unpaired records and contains both source rows for each paired model.

Only after all these gates pass may the implementation hash and load the EXP-005 gap
file. Use its stored 34 WRN gaps as the sole outcome. Do not reconstruct or replace
the outcome from EXP-011 or EXP-012.

## Frozen exposure construction

For parameter `x`, source `s`, tissue `t`, and model `i`, assign ascending average
midranks within the complete source×tissue denominator:

`Q_s,t,x(i) = (midrank_s,t,x(i) - 1) / (n_s,t - 1)`.

Never compare raw efficacy or growth-rate units across sources, jitter ties, rank only
the 34 paired models, or rerank after restricting to paired models.

Primary exposure:

`E_eff(i) = abs(Q_Avana,t,efficacy(i) - Q_KY,t,efficacy(i))`.

Prespecified descriptive companion exposure:

`E_growth(i) = abs(Q_Avana,t,growth(i) - Q_KY,t,growth(i))`.

Growth rate has no p-value, confidence interval, threshold, pass/fail status, or
ability to rescue or reinterpret the efficacy result. The two parameters are related
Chronos-derived quantities, not independent corroboration.

## Frozen outcome and primary estimand

Outcome is the frozen EXP-005 absolute WRN percentile gap `D(i)`.

Within each tissue, compute Spearman rho between the frozen primary efficacy
exposure and `D(i)`. Spearman rho is Pearson correlation of the two average-midranks
after each vector is ranked exactly once. Define the equal-tissue estimand:

`theta = (rho_Large_Intestine + rho_Ovary) / 2`.

Inference uses one paired ModelID per observation. Never treat the 103 source records,
individual guides, or both source values as independent observations.

## Inference and gates

- Seed: `20260830`.
- Permutation: 100,000 repeats. Hold frozen efficacy-exposure ranks fixed and
  independently permute frozen WRN-gap values among ModelIDs within each tissue.
  Use the positive tail and plus-one p-value
  `(1 + count(theta_perm >= theta_observed)) / 100001`.
- Bootstrap: 10,000 paired-ModelID resamples with replacement separately within each
  tissue. Correlate the already-frozen rank pairs directly; never rerank duplicated
  bootstrap rows. If any replicate has zero variance in either vector, stop as a T0
  integrity failure; do not discard or redraw it.
- Report the percentile 95% interval for theta.

All four primary gates must pass:

1. `theta >= 0.40`;
2. one-sided permutation `p <= 0.05`;
3. bootstrap 95% lower bound `> 0.10`; and
4. neither tissue-specific rho `< -0.20`.

The permutation p-value tests no positive association; it does not test the point
target `theta >= 0.40`. No threshold, parameter, denominator, tissue, outcome,
direction, or estimator may change after outcome computation.

## Descriptive outputs

- Complete 103-row parameter ledger with efficacy and growth values/percentiles;
- complete 34-row paired exposure/outcome ledger;
- primary efficacy tissue correlations, theta, permutation p, bootstrap interval,
  and gate receipt;
- descriptive growth-rate tissue/equal-tissue correlations without inference;
- tied-level counts, exposure summaries, and model identities.

No composite, regression adjustment, model exclusion, subgroup test, alternate
denominator, raw-unit comparison, or post hoc combination with another experiment is
allowed. A primary failure cannot be rescued by growth rate.

## Maximum claim

If all primary gates pass: **source-relative Chronos-inferred model-efficacy
discordance was positively associated with WRN-rank discordance in this frozen
two-tissue cell-model set.**

This would not establish causality, source superiority, model drift, a WRN mechanism,
a new dependency, therapeutic relevance, patient benefit, or clinical utility.
