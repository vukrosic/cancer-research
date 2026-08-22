# EXP-20260822-007 outcome-blind adequacy protocol

## Question

Is source-specific mutation burden at WRN-targeting guide sites sufficiently present
and variable to test as a technical explanation for WRN ranking discordance?

## Evidence boundary

This is a T0 data-availability and exposure-adequacy audit, not an association test.
The candidate was proposed by a read-only methods scout that did not inspect EXP-006
outcomes. The orchestrator inspected guide maps and mutation matrices using only
ModelID and tissue from the frozen EXP-005 cohort. It did not parse WRN gap values or
compute any exposure-outcome association.

The gate was not committed before exposure inspection, so this is not described as
a repository-preregistered inferential experiment. Its only possible outcomes are
adequate for a later separately preregistered test, or a preserved T0 failure.

## Frozen inputs and population

- DepMap Public 23Q4 Figshare article 24667905 version 2.
- Official `AvanaGuideMap.csv`, `KYGuideMap.csv`,
  `OmicsGuideMutationsBinaryAvana.csv`, and
  `OmicsGuideMutationsBinaryKY.csv` with official MD5 and locally computed SHA-256
  receipts.
- Exactly the 34 EXP-005 paired ModelIDs, 17 Large Intestine and 17 Ovary, copied to
  a dedicated hash-frozen `cohort.csv` containing only `model_id` and `tissue`.
- Only guide-map rows for `WRN (7486)` with `UsedByChronos=True`, one genomic
  alignment, and empty `DropReason`.

## Exposure and gate

For model `i` and source `s`, define mutation burden as the fraction of eligible WRN
guides whose target-location mutation indicator equals one. Candidate source
asymmetry is the absolute Avana-minus-KY burden difference.

Adequacy requires:

1. all hashes and identities match;
2. at least three eligible WRN guides per library;
3. all 34 ModelIDs occur in both mutation matrices;
4. binary complete values for every eligible guide and cohort model;
5. at least 15 models per tissue; and
6. a nonconstant source-asymmetry exposure in each tissue.

If any gate fails, stop without reading WRN gaps, computing a correlation,
permutation, bootstrap, or changing the exposure definition.

## Claim boundary

A constant-zero exposure would show only that the official 23Q4 matrices annotate no
WRN guide-site mutations in these 34 paired models. It would exclude this direct
guide-site-mutation explanation in this dataset, but not guide efficacy, exon/domain
placement, assay duration, cell state, uncalled variants, or other technical causes.
