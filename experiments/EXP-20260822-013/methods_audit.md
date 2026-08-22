# EXP-20260822-013 pre-execution methods audit

## Decision

**GO after amendments, now frozen.** The independent critic approved this as a
narrow model-parameter association audit, not a novel biological cancer finding.

## Amendments frozen

- The claim is association, never explanation or causality.
- Avana and KY map only to the exact frozen ModelID columns
  `Achilles-Avana-2D` and `Achilles-KY-2D`; these are ModelID-level parameters, not
  ScreenID measurements.
- Raw source units are never compared. Full source×tissue average-midranks produce
  the primary efficacy and descriptive growth exposures.
- Both parameter files, all 103 source-specific denominator identities, domains,
  finite own-source values, both-source coverage for the 34 paired models,
  nonconstant exposures, distinct-level counts, and tied-level limits are checked
  before the EXP-005 outcome file is opened or hashed. Opposite-source blanks for
  the 35 unpaired records are expected and unused.
- The EXP-005 gap file is the sole hash-locked outcome; EXP-011/012 outputs are not
  reconstructed or substituted.
- Inference uses one paired ModelID per observation, equal tissue weighting, fixed
  rank pairs, 100,000 within-tissue permutations, and 10,000 paired bootstraps with
  a zero-variance hard stop.
- Primary gates are theta `>=0.40`, permutation p `<=0.05`, bootstrap lower bound
  `>0.10`, and tissue rho `>=-0.20`.
- Growth rate is descriptive only and cannot rescue efficacy. Composites,
  adjustments, model exclusions, subgroup tests, alternate denominators, raw-unit
  comparisons, and cross-experiment rescue are prohibited.

No WRN-gap association, rank correlation, p-value, confidence interval, or outcome
was computed during the review.
