# Independent audit — EXP-20260822-005

## Initial verdict

**NO-GO as first implemented; all point estimates reproduced.**

The auditor independently verified:

- exact input hash, full source×tissue denominators, and 17+17 overlap;
- all 34 source percentiles and absolute gaps;
- Large Intestine rho 0.8210784314 and Ovary rho 0.3700980392;
- equal-tissue theta 0.5955882353;
- 12 extreme permutations and plus-one p = 13/100,001;
- 198 concordant, 74 discordant, and 0 tied within-tissue model pairs;
- median gap 0.1750123153, IQR [0.0977011494, 0.2771428571], and 10/34
  fixed-threshold flags;
- correct post-unsealing derived-analysis label and narrow claim.

The blocker was the first bootstrap implementation. It called Spearman on each
resample, which re-ranked duplicated bootstrap observations. The frozen protocol
required retaining the original full-denominator percentiles and not reranking the
bootstrap sample.

## Remediation

- Bootstrap now computes Pearson correlation directly on sampled frozen percentile
  pairs; the primary point estimate remains Spearman on the original paired ranks.
- Added a regression fixture where duplicate resampling produces a different result
  under forbidden reranking.
- Regenerated smoke and full outputs, timing, result narrative, and hashes.
- The implementation failure is preserved here; no gate or cohort changed.

## Re-audit

**GO — scientific and computational remediation verified.**

The same auditor confirmed:

- bootstrap directly correlates sampled frozen percentiles without reranking;
- regenerated CI `[0.3185637150, 0.7869891592]` exactly matches independent
  computation;
- theta, permutation p, tissue correlations, model gaps, Kendall counts, and all
  pass gates are unchanged;
- reruns are byte-identical to the tracked outputs and declared hashes match;
- the duplicate-resample regression distinguishes the compliant statistic from
  forbidden re-ranked Spearman;
- all 26 tests pass;
- the post-unsealing evidence label and maximum claim remain appropriately narrow.

No scientific, computational, or documentation blocker remains for commit/push.
