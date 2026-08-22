# EXP-20260822-005 preregistration

## Question

In the two adequately sized overlap strata—Large Intestine and Ovary—do
source-specific WRN dependency rankings agree across Broad Avana and Sanger KY?

This is a distinct two-tissue child of the failed four-tissue EXP-004 design. It does
not replace or rescue EXP-004.

## Blinding and evidence boundary

EXP-003's source-specific WRN scores and group effects were already unsealed and
public before this child was designed. Therefore EXP-005 is a **preregistered derived
analysis after endpoint unsealing**, not pristine data-blind confirmation.

Before freezing this protocol, neither the orchestrator nor the outcome-blind methods
critic had computed any cross-source model-level WRN rank correlation, percentile
gap, Kendall concordance, or outlier ordering. The tissue restriction and all gates
were selected from model/source availability counts, not those derived outcomes.

## Frozen population and adequacy

- Input: EXP-003's hash-locked 147-row model-score table.
- Tissues: exactly `Large Intestine` and `Ovary`.
- Unit: one distinct ModelID represented exactly once in each source within one
  tissue.
- Frozen overlap: 17 models per tissue, 34 total.
- Use all eligible EXP-003 models within each source×tissue as rank denominators,
  including source-only models.
- Endpoint coverage must remain 100% for those full source×tissue denominators.
- Multiple eligible screens are already collapsed by the EXP-003 median rule.
- Reject duplicate model×source×tissue rows; never choose records by score or
  agreement.

Adequacy requires at least 30 overlap models total, at least 15 in each tissue,
complete finite endpoints, and nonconstant percentile vectors in both sources and
tissues. Failure stops before inference.

## Source-specific dependency percentiles

For source `s`, tissue `t`, and model `i`, compute ascending average midrank of the
raw WRN score among **all** eligible source×tissue models. Define:

`P_s,t(i) = (n_s,t - midrank_ascending(score_s,t,i)) / (n_s,t - 1)`.

Higher percentile means stronger WRN loss of fitness. Never jitter ties. Do not rerank
after restricting to overlap models.

## Primary estimand

For each tissue, compute Spearman correlation between paired Avana and KY dependency
percentiles among its 17 overlapping ModelIDs. Define the equal-tissue estimand:

`theta = (rho_Large_Intestine + rho_Ovary) / 2`.

This is not a pooled or model-count-weighted correlation.

## Inference

- Seed: 20260826.
- Permutation: 100,000 repeats. Hold Avana percentiles fixed and independently
  permute KY percentile values among the 17 overlap IDs within each tissue. Preserve
  tissue membership and ties. One-sided p-value is
  `(1 + count(theta_perm >= theta_observed)) / 100001`.
- Bootstrap: 10,000 repeats. Resample paired ModelIDs with replacement separately
  within each tissue, retain the original full-denominator percentiles, and recompute
  the equal-tissue mean. Do not rerank bootstrap samples. Report the percentile 95%
  interval.
- Any nonfinite primary estimate is an integrity failure.

## Frozen pass gates

All must pass:

1. adequacy gates above;
2. `theta >= 0.50`;
3. one-sided stratified permutation `p <= 0.05`;
4. 95% bootstrap lower bound `> 0.20`;
5. neither tissue-specific Spearman correlation is below `-0.20`.

No threshold, tissue, model, denominator, endpoint, or statistic may change after
computing the outcome.

## Secondary analyses

None can rescue the primary result:

- model-level absolute percentile gap
  `d_i = |P_Avana,t(i) - P_KY,t(i)|`;
- median and interquartile range of `d_i`;
- fixed discordance flag `d_i >= 0.25`;
- exploratory five largest gaps, expanding ties at the fifth-model cutoff;
- tissue-specific correlations;
- pooled within-tissue Kendall pair concordance, labelled descriptive;
- gap summaries by MSI/MSS label, with no secondary p-values.

## Maximum claim

If all gates pass: in the preregistered Large Intestine and Ovary overlap set,
source-specific WRN dependency rankings showed positive within-tissue agreement
across Avana and KY.

This is conditional measurement/ranking agreement in shared cell models. It does not
establish a new cancer dependency, mechanism, universal reproducibility, therapeutic
effect, patient benefit, or clinical relevance.

