# EXP-20260822-009 preregistration

## Question

Is relative Avana-versus-KY asymmetry in the number of screen sequences eligible
for inclusion associated with absolute WRN dependency-percentile discordance in the
frozen Large Intestine and Ovary model set?

This is a screen-process measurement audit. It is related to, but distinct from,
EXP-006's broad five-metric screen-performance composite. It does not test a
biological WRN mechanism or a causal effect of sequence inclusion.

## Evidence and endpoint boundary

EXP-005 WRN percentiles and gaps were already unsealed. EXP-009 is therefore a
**preregistered derived observational analysis after endpoint unsealing**, not
blinded confirmation.

Before freezing this protocol, the orchestrator and an independent methods critic
inspected field semantics, identities, completeness, raw count distributions, and
exposure discreteness without loading WRN-gap values or computing any
exposure-outcome association. The critic's initial decision was NO-GO as written and
GO after the amendments frozen here.

## Frozen population and identities

- Paired population: exactly the 34 ModelIDs in EXP-007 `cohort.csv`, 17 Large
  Intestine and 17 Ovary.
- Full ranking denominators: the 103 unique model-source screens underlying
  EXP-003/005: Avana 25 / KY 30 Large Intestine and Avana 22 / KY 26 Ovary.
- Screen identity: every QC row must exactly match the frozen ScreenID for its
  ModelID, source, and tissue in EXP-003 `model_scores.csv`.
- Unit of inference: one paired model. Sequences are never inferential units.

## Frozen exposure hierarchy and semantics

Primary field from official DepMap Public 23Q4 `AchillesScreenQCReport.csv`:

1. `nIncludedSequences`.

Prespecified sensitivity field:

2. `nPassingSequences`.

`nIncludedSequences` measures the number of sequences that can be included,
conditional on the release's sequence-level process. The exposure below is a
difference in within-source-by-tissue relative inclusion position, not an absolute
difference in sequence counts and not a causal estimate of inclusion effects.

`nPassingSequences` is a sensitivity exposure, not independent corroboration, and
cannot rescue any primary failure. In the frozen 103-screen denominator, the two raw
fields differ in only three records and their paired-model exposures are nearly
rank-identical. No logical ordering constraint is imposed between the fields:
three frozen records have `nIncludedSequences > nPassingSequences`, and they must
not be repaired, excluded, or reinterpreted.

For field `m`, source `s`, tissue `t`, and full-denominator model `i`, assign
ascending average midranks to the raw integer count and define:

`Q_s,t,m(i) = (midrank_s,t,m(i) - 1) / (n_s,t - 1)`.

For each paired model, define source asymmetry:

`E_m(i) = |Q_Avana,t,m(i) - Q_KY,t,m(i)|`.

Preserve all ties. Rank in full source-by-tissue denominators and never rerank after
restricting to paired models.

## Frozen outcome and primary estimand

Outcome is EXP-005's frozen absolute WRN dependency-percentile gap `D(i)`.

Within each tissue, compute average midranks of primary `E_included` and `D` exactly
once. Spearman rho is Pearson correlation of those frozen ranks. Define:

`theta = (rho_Large_Intestine + rho_Ovary) / 2`.

Do not use a pooled 34-model correlation as primary.

## T0 adequacy gates

Evaluate exposure adequacy before loading WRN-gap values. For both the primary and
sensitivity fields:

1. all 103 mapped counts are finite, nonnegative integers;
2. exact source-by-tissue denominators are 25 / 30 / 22 / 26 and contain 103 unique
   ScreenIDs;
3. every ScreenID exactly matches the frozen upstream model-score identity;
4. each tissue retains exactly 17 paired models;
5. `E_m` has at least five distinct values in each tissue; and
6. the largest tied exposure group contains at most eight of 17 models per tissue.

The outcome-blind exposure audit found six/five distinct primary exposure values in
Large Intestine/Ovary, with largest ties of seven models, so the frozen structure
meets this gate. Stop without association or inference if execution does not
reproduce every adequacy fact.

## Inference

- Seed: 20260829.
- Permutation: 100,000 repeats. Hold WRN-gap ranks fixed and independently permute
  the complete primary exposure-rank vector among ModelIDs within each tissue. Use
  the positive tail and plus-one p-value.
- Bootstrap: 10,000 repeats. Resample paired ModelIDs with replacement separately
  within tissue and correlate sampled values of the originally frozen average-rank
  pairs. Never rerank duplicated bootstrap observations.
- If any bootstrap replicate has zero variance in either sampled rank vector,
  terminate as a T0 integrity failure. Do not discard or redraw it.
- Report the percentile 95% interval.

## Frozen outcome gates

All primary gates must pass:

1. `theta >= 0.40`;
2. one-sided tissue-preserving permutation `p <= 0.05`;
3. 95% bootstrap lower bound `> 0.10`; and
4. neither tissue-specific rho below `-0.20`.

The permutation p-value tests no positive association, not the point target of
0.40. No field, threshold, denominator, cohort, tissue, ranking rule, or direction
may change after outcome computation.

## Sensitivity analysis

Apply the same frozen estimator and inference to `nPassingSequences`, reporting it
as prespecified sensitivity evidence. Its result cannot alter the primary decision.
Also report complete model-level exposures and tied-level counts. No pooled test,
continuous-count rescue, field combination, learned weighting, model exclusion, or
subgroup search is allowed.

## Maximum claim

If all primary gates pass: in this frozen, post-endpoint-unsealing two-tissue
cell-model set, relative source asymmetry in sequence inclusion was descriptively
associated with absolute WRN percentile discordance.

This would not show that sequence loss causes discordance, identify defective
screens, rank either source's quality, generalize beyond these source/tissue
denominators, establish a WRN mechanism, or support therapeutic or clinical claims.
