# EXP-20260822-009 outcome-blind methods audit

## Decision

**GO after amendments.** The independent critic's initial decision was NO-GO as
written because the proposed sensitivity field was incorrectly framed as
corroboration and the highly discrete exposure lacked an explicit adequacy gate.

## Amendments applied before outcome access

- `nIncludedSequences` remains the sole primary exposure.
- `nPassingSequences` is labeled a near-duplicate prespecified sensitivity exposure
  that cannot rescue a primary failure.
- Field semantics distinguish relative within-source inclusion position from an
  absolute count difference or causal effect.
- Counts must be finite nonnegative integers; 103 exact ScreenIDs and frozen
  25/30/22/26 denominators are enforced.
- Each tissue requires at least five exposure levels and no tied level larger than
  eight of 17 models.
- The three records where included exceeds passing are preserved; no ordering repair
  or exclusion is permitted.
- Permutation preserves tissue and tied frozen ranks.
- Bootstrap samples frozen ranks without reranking and terminates rather than
  discarding or redrawing a zero-variance replicate.
- The maximum claim is descriptive, cohort-specific, noncausal, and nonclinical.

## Outcome-blind adequacy facts

The 103 screen identities and all counts were complete. Primary exposure had six
distinct levels in Large Intestine and five in Ovary; the largest tie was seven of
17 in both tissues. Sensitivity exposure had the same numbers of distinct levels and
largest tie. The sensitivity and primary exposure Spearman correlations were 1.0000
in Large Intestine and 0.9805 in Ovary, confirming that sensitivity is not
independent corroboration.

No WRN-gap value, exposure-outcome correlation, permutation, bootstrap, or outcome
gate was computed during this audit.
