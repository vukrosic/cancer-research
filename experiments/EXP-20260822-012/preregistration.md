# EXP-20260822-012 preregistration

## Question

Under the passing-sequence WRN reconstruction validated in EXP-011, do the 10
EXP-005 models with absolute Avana-versus-KY dependency-percentile gaps at least
0.25 remain flagged after every eligible global single-guide omission?

This is a deterministic same-assay stress test. EXP-005's endpoints and selected
models were already unsealed, and EXP-011's sequence rule was selected after
EXP-010's baseline failure. EXP-012 is therefore not independent confirmation or a
new biological dependency test. However, no guide-omission score, rank, gap, or
robustness outcome has yet been computed.

## Immutable lineage

- EXP-010 remains immutable `FAIL_T0_RECONSTRUCTION`; it performed zero omissions.
- EXP-011 remains the separately audited 103/103 passing-sequence reconstruction.
- EXP-012 is a new child of EXP-011. It does not edit, rerun, or rescue EXP-010.
- EXP-011's protocol, implementation, ledger, summary, result, audit, and public
  commit are hash-frozen in the manifest.

The nine perturbations and the `>=8/10` descriptive criterion were specified in
EXP-010 before its baseline stopped. They are carried forward unchanged, not chosen
after observing omission outcomes.

## Frozen inputs, identities, and guides

- Same official DepMap Public 23Q4 version-2 Avana/KY pre-Chronos LFC matrices and
  exact byte, MD5, and SHA-256 receipts as EXP-011.
- Same hash-frozen guide maps, sequence map, screen QC report, official naïve
  gene-score matrix, EXP-003 denominator table, EXP-005 gap table, and EXP-011
  reconstruction artifacts.
- Exactly 103 unique `(ScreenID, ModelID, Library)` identities: Avana/KY 25/30 Large
  Intestine and 22/26 Ovary.
- Exactly 34 paired EXP-005 ModelIDs, 17 per tissue.
- Exactly the ten rows already marked `discordant_ge_0_25=True` in the frozen
  EXP-005 gap file. Do not re-select models from reconstructed outcomes.

Eligible guides must use EXP-011's strict fields: `Gene == "WRN (7486)"`, exact
`UsedByChronos == "True"`, finite `nAlignments == 1.0`, and exact blank
`DropReason`. This must yield exactly the frozen four Avana and five KY guide
sequences. Do not lowercase or otherwise coerce guide fields.

## Frozen passing-sequence reconstruction

Join both sequence and QC rows by exact `(ScreenID, ModelID, Library)`. Retain a
sequence if and only if sequence-level `PassesQC == True` and
`ExcludeFromCRISPRCombined == False`; booleans must be the exact canonical strings
`True` or `False`. Require retained count to equal the exact screen's finite
nonnegative integer `nPassingSequences`.

Reject every blank, duplicate, contradictory, missing, noncanonical, or nonfinite
identity, guide, sequence, count, or value.

For source `s`, guide `g`, and screen `j`:

`G_s,g,j = mean LFC across retained passing sequences`

`W_s,j = median G across all retained eligible guides`.

For an even number of guides, median means the arithmetic mean of the two middle
values after numerical sorting. Thus baseline Avana uses the middle-two mean across
four guides, baseline KY uses the middle guide across five, Avana omissions use the
middle guide across three, and KY omissions use the middle-two mean across four.

## Sequential baseline gates

Before loading the EXP-005 gap file or entering any omission loop:

1. reconstruct all 103 baseline scores;
2. reproduce all official WRN naïve scores with absolute discrepancy `<=1e-8` and
   relative tolerance zero;
3. reproduce the hash-frozen EXP-011 103-row ledger identities, retained counts,
   reconstructed values, official values, and gate flags within `1e-8`; and
4. stop immediately if any comparison or receipt fails.

Only after those gates pass may the implementation load the EXP-005 gap file.
Before omissions, recompute the 34 paired-model baseline percentiles and gaps and
require every frozen EXP-005 percentile and gap to agree within `1e-8`. Require the
CSV's flagged set to contain exactly ten rows whose stored boolean is
`discordant_ge_0_25=True`, and independently verify each stored boolean equals the
exact comparison `stored_gap >= 0.25`. Do not replace that locked set from a newly
computed selection.

## Nine frozen global perturbations

Run exactly nine configurations:

1. omit each of the four Avana guides in turn from every Avana denominator screen,
   retaining three Avana guides while every KY score stays at baseline; and
2. omit each of the five KY guides in turn from every KY denominator screen,
   retaining four KY guides while every Avana score stays at baseline.

Configuration names and order are source plus lexicographically sorted omitted guide
sequence. Every omission is global and library-specific. No screen-specific choice,
pair omission, simultaneous two-library omission, sequence deletion, guide
replacement, or fallback configuration is allowed. Preserve all 103 identities and
finite scores in every configuration.

## Full-denominator percentiles and gaps

For every baseline or perturbed source `s`, tissue `t`, and model `i`, compute
ascending average midrank across the complete frozen source-by-tissue denominator:

`P_s,t(i) = (n_s,t - midrank_ascending(W_s,t(i))) / (n_s,t - 1)`.

More negative scores receive higher dependency percentiles. Never rank only the 34
paired models or the ten selected models, jitter ties, change denominator sizes, or
reuse a baseline percentile for a perturbed source.

For each paired model and configuration:

`D(i) = abs(P_Avana,t(i) - P_KY,t(i))`.

Apply the flag as exact `D(i) >= 0.25` without numerical tolerance.

## Frozen primary criterion

For each of the ten locked baseline-flagged models, define **fully robust** as
retaining `D(i) >= 0.25` under all four Avana-only and all five KY-only omissions.

EXP-012 passes the descriptive criterion only if at least **8 of 10** locked models
are fully robust. No secondary output can rescue failure.

## Frozen descriptive outputs

- Per-model gap and binary flag in baseline plus all nine configurations.
- Per-model Avana-all-four, KY-all-five, and all-nine robustness indicators.
- Per-model minimum, median, and maximum gap across the ten configurations.
- Number of the ten locked models robust to all Avana, all KY, and all nine
  omissions.
- Baseline equal-tissue ordering theta and minimum/maximum theta across omissions,
  using the same frozen full-denominator percentile correlation as EXP-005.
- Unique baseline-unflagged models becoming flagged at least once.
- Total unflagged-to-flagged model-configuration transitions out of `24 * 9 = 216`.

The perturbations are dependent deterministic transforms of the same assay screens.
Compute no p-value, confidence interval, bootstrap, multiplicity correction, guide
ranking, subgroup test, or post hoc combined perturbation.

## Interpretation hazards

The ten models were selected for large baseline discordance, so movement toward the
threshold is not evidence for a biological subtype. Avana changes from a four-guide
median to three guides while KY changes from five guides to four; do not compare
source-specific failure counts as estimates of guide quality or causal influence.

## Maximum claim

If the criterion passes: **In this frozen 103-screen, passing-sequence
reconstruction, at least X of the ten previously flagged cross-source WRN
percentile gaps remained flagged under every eligible single-guide omission.**

This cannot establish a causal bad guide, independent replication, robustness to
multi-guide, library, model-state, or pipeline changes, a WRN biological mechanism,
therapeutic relevance, patient benefit, or clinical utility.
