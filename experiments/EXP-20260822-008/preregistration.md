# EXP-20260822-008 preregistration

## Question

Are models with greater general Avana-versus-KY rank discordance across unrelated
control genes also the models with greater source-specific WRN rank discordance?

This is a measurement-reliability audit. It asks whether WRN disagreement is part of
a model-general pattern; it does not test a biological WRN mechanism or causation.

## Evidence and blinding boundary

EXP-005 WRN percentiles and gaps are already unsealed. EXP-008 is therefore a
**preregistered derived observational analysis after endpoint unsealing**, not
blinded confirmation.

Before freezing this protocol, neither the orchestrator nor the outcome-blind critic
computed or inspected any association between a control-panel exposure and a WRN
gap. The critic did not inspect EXP-005 gap values or EXP-006 outcomes. Panel
hierarchy, eligibility, ranking, aggregation, inference, gates, and claim boundaries
below are frozen before model-level control discordance is associated with WRN gaps.

## Frozen population and source identities

- Paired outcome population: the outcome-free 34-model EXP-007 `cohort.csv`, exactly
  17 Large Intestine and 17 Ovary ModelIDs.
- Full source×tissue ranking denominators: the 103 unique source screens underlying
  EXP-003/005: Avana 25 / KY 30 Large Intestine and Avana 22 / KY 26 Ovary.
- Exactly one unique frozen ScreenID per model×source record.
- Source endpoint: official DepMap Public 23Q4 `ScreenNaiveGeneScore.csv`, a
  source/library-specific collapsed LFC matrix.

Raw Avana and KY scores are never compared directly. Stop before association if any
identity, count, receipt, completeness, or nonconstancy invariant fails.

## Frozen control panels and hierarchy

Official hash-frozen lists:

1. **Primary:** `AchillesCommonEssentialControls.csv`;
2. **Corroborative:** `AchillesNonessentialControls.csv`.

WRN (7486) is absent from both. The panels remain separate because nonessential
scores participate in upstream normalization and represent a different measurement
behavior. Never combine panels, select individual genes, learn weights, or run
per-gene WRN-gap tests.

A control is eligible within its panel only if it:

- appears in the official list;
- appears exactly once as a gene-score column;
- is not `WRN (7486)`; and
- has a finite score in all 103 full-denominator source screens.

Header availability is 1,244 common-essential and 730 nonessential controls. Require
at least 996 and 584 fully eligible controls, respectively (80% of those present).
The same frozen eligible genes are used for every model, tissue, and source.

## Source-specific depletion percentiles

For each eligible control gene `g`, source `s`, tissue `t`, and denominator model
`i`, assign ascending average midranks to raw LFC and define:

`P_s,t,g(i) = (n_s,t - midrank(LFC_s,t,g(i))) / (n_s,t - 1)`.

Higher P means stronger relative depletion. Preserve ties. Rank within the full
source×tissue denominator and never rerank after restricting to paired models.

For paired model `i` and gene `g`:

`d_i,g = |P_Avana,t,g(i) - P_KY,t,g(i)|`.

Reduce correlated genes to one model-level exposure per panel:

`E_i,panel = median_g(d_i,g)`.

Genes are not independent inferential units. Require finite, nonconstant exposures
with at least 10 distinct values in each tissue for each panel.

## Frozen outcome and estimand

Outcome is EXP-005's frozen absolute WRN dependency-percentile gap `D(i)`.

Within each tissue and panel, compute average midranks of `E` and `D` once. Spearman
rho is Pearson correlation of those frozen ranks. Define:

`theta_panel = (rho_Large_Intestine + rho_Ovary) / 2`.

Do not pool the 34 models.

## Inference

- Seed: 20260828.
- Permutation: 100,000 repeats per panel. Hold WRN-gap ranks fixed and independently
  permute complete frozen model-level exposure ranks within each tissue. Use the
  positive tail and plus-one p-value.
- Bootstrap: 10,000 repeats per panel. Resample paired ModelIDs with replacement
  separately within each tissue and correlate sampled frozen rank values directly.
  Never rerank duplicated bootstrap observations.
- Report percentile 95% intervals, tissue-specific estimates, model exposures, and
  complete eligible/excluded control ledgers.

## Frozen gates and interpretation hierarchy

Adequacy requires exact population/denominator identities, unique screens, minimum
panel sizes, and finite exposures with at least 10 distinct values per tissue.

Common-essential primary gates all must pass:

1. `theta_essential >= 0.40`;
2. one-sided permutation `p_essential <= 0.05`;
3. 95% bootstrap lower bound `> 0.10`;
4. neither tissue-specific rho below `-0.20`.

The nonessential corroborative panel uses the same gates, but cannot rescue a failed
common-essential primary result.

- Both panels pass: support the narrow model-general control-gene-discordance claim.
- Common-essential only passes: claim only an association with common-essential
  score discordance; do not call it broad model-general evidence.
- Common-essential fails: primary hypothesis fails, regardless of nonessential result.

No threshold, panel, gene, denominator, aggregation, cohort, or tissue may change
after outcome association.

## Maximum claim

If both panels pass: in this specific 23Q4 Avana/KY colorectal–ovarian overlap,
models with greater general cross-source control-gene rank discordance also had
greater WRN rank discordance.

This would not establish causality, a WRN mechanism, source superiority, cell-line
identity drift, therapeutic actionability, patient benefit, or clinical relevance.
