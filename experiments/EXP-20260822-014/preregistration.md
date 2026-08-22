# EXP-20260822-014 preregistration

## Question

Does matrix-defined damaging `STAG2` mutation status predict stronger
source-specific `STAG1` knockout dependency in Avana and KY cancer cell-line
screens?

This is a replication-first positive-control audit of a published paralog-loss
interaction, not a novelty or treatment claim. A predeclared secondary pair,
`PDS5B` matrix-defined damaging status → `PDS5A` dependency, is analyzed separately and cannot rescue the
primary STAG result.

The primary interaction has prior experimental and DepMap support in the
literature, including genome-wide CRISPR evidence and isogenic validation:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC8408347/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7266993/

The secondary pair has been reported in combinatorial CRISPR and DepMap
paralog-compensation analyses:

- https://link.springer.com/article/10.1038/s44320-025-00122-4

## Frozen release, source, and unit

- Release: DepMap Public 23Q4, Figshare article `24667905`, version 2.
- Sources: `Avana` and `KY` exactly, treated as separate source-specific
  corroboration cohorts from the same public release. They are not assumed to be
  independent biological cohorts, and no raw score comparison across sources is
  made.
- Screen eligibility: `PassesQC == true`, `CanInclude == true`, and `Library` in
  `{Avana, KY}` from `AchillesScreenQCReport.csv`.
- Unit: one `ModelID` within one source. If multiple eligible screens exist for a
  source/model, collapse the target-gene score by the median, preserving all
  eligible screen IDs in the derived ledger.
- Lineage: `OncotreeLineage` from the hash-locked `Model.csv`, used only for
  within-lineage comparisons. No lineage is selected after seeing target scores.

The exact target columns in the source-specific endpoint are:

- `STAG1 (10274)` for the primary target;
- `PDS5A (23244)` for the secondary target.

## Frozen inputs and receipts

- `data/raw/depmap/23q4/ScreenNaiveGeneScore.csv`, SHA-256
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`, official
  MD5 `265f8372e9cd0fad56c1a6b66b8a783d`;
- `data/raw/depmap/23q4/AchillesScreenQCReport.csv`, SHA-256
  `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407`;
- `data/raw/depmap/23q4/CRISPRScreenMap.csv`, SHA-256
  `1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad`;
- `data/raw/depmap/23q4/Model.csv`, SHA-256
  `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341`;
- `data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv`, SHA-256
  `aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3`.

The damaging matrix is the official 23Q4 genotyped matrix where `0` means no
damaging mutation, `1` means one or more damaging mutations with summed allele
frequency at most 0.95, and `2` means summed allele frequency above 0.95. The
exposure is called **matrix-defined damaging mutation status**, frozen as matrix
value `>=1`; it is not assumed to prove functional or biallelic loss. No mutation
class, threshold, or gene filter may change after endpoint access.

## Outcome-blind adequacy and execution order

Before opening or parsing either target-gene score column, verify all input
hashes, exact headers, unique screen/model identities, eligible source/model
coverage, finite damaging states, and exact loss-status columns. Write a complete
context ledger containing each eligible source/model, lineage, loss status, and
eligible screen IDs before reading target-gene scores.

The pre-outcome context gate requires, for each pair and each source:

- at least 8 loss models;
- at least 50 intact models;
- at least 5 lineages containing both damaging-status and intact models.

The outcome-free matrix audit measured the following candidate loss counts in the
eligible source-specific model populations before this protocol was frozen:

| Pair | Avana loss | KY loss |
|---|---:|---:|
| STAG2 → STAG1 | 31 | 9 |
| PDS5B → PDS5A | 23 | 12 |

If any pre-outcome context gate fails, stop as T0 without parsing target scores or
computing dependency contrasts. After the context ledger is sealed, open the two
target columns only to run a sealed endpoint-completeness gate: every predeclared
eligible source/model must have one finite target score after the frozen median
collapse, and every required lineage×status group must remain nonempty. This gate
emits no group summary or effect. If it fails, stop as a non-evaluable T0 without
imputation, model exclusion, or threshold rescue. Only after it passes may any
dependency contrast or inference be computed.

Before target-score access, compute a design-sensitivity receipt from the exact
context roster. Under the frozen sensitivity model, intact and damaging-status
scores are independent Normal variables with common unit variance and a common
mean shift calibrated so the expected pairwise direction statistic is `delta =
-0.20`; the observed lineage group sizes are held fixed. Generate the frozen
100,000-label-permutation null distribution once for each source and use its
empirical lower-tail 5% critical value, then simulate 10,000 alternative datasets
and count the fraction below that critical value. If either source has less than
80% simulated power, label the experiment `FEASIBILITY_ONLY` and do not
make a two-source replication claim, even if observed gates pass. The inferential
run still uses the frozen estimator and thresholds; this design receipt cannot be
changed after target-score access.

## Frozen estimand

For pair `L → T`, source `s`, lineage `l`, loss model `i`, and intact model `j`,
compare the target score `Y` from `ScreenNaiveGeneScore.csv`:

`c(i,j) = -1` if `Y_loss < Y_intact`, `+1` if `Y_loss > Y_intact`, and `0` for a
tie. More negative log-fold-change means stronger loss of fitness. The source
estimand is the pair-count-weighted, within-lineage direction statistic:

`delta_s = sum(c(i,j)) / number of within-lineage loss×intact pairs`.

No cross-lineage or cross-source pair enters the estimand. The median target score
in loss and intact models, the number of contributing pairs, and every
lineage-specific delta are descriptive receipts only.

## Inference

- One-sided within-lineage permutation: independently shuffle loss/intact labels
  within each lineage while preserving that lineage's observed loss count and
  compute `delta_s`. Use 100,000 repeats and the lower-tail plus-one p-value
  `(1 + count(delta_perm <= delta_observed)) / 100001`.
- Bootstrap: 10,000 source-specific resamples with replacement at the collapsed
  ModelID unit within every lineage×matrix-status group. Recompute the same
  pair-count-weighted delta and report the percentile 95% interval using NumPy's
  default linear quantile method (`method="linear"`). If a replicate has no valid
  comparison or a zero denominator, treat it as an implementation integrity
  failure; do not discard or redraw it.
- Seed: `20260830`.

## Frozen gates

For the primary STAG2 → STAG1 pair, **both Avana and KY must independently pass**:

1. `delta_s < 0`;
2. `delta_s <= -0.20`;
3. one-sided permutation `p <= 0.05`;
4. bootstrap 95% upper bound `< 0`;
5. at least five contributing lineages have negative lineage-specific delta; and
6. no contributing lineage has delta `> +0.20`.

The secondary PDS5B → PDS5A pair uses the same frozen estimator and nominal gates
for descriptive corroboration only. It has no confirmatory claim, no multiplicity-
adjusted claim, and cannot rescue or reinterpret a primary STAG2 failure. The
primary STAG2 pair is the sole confirmatory hypothesis. No FDR adjustment, pooled
pair panel, composite, regression, subgroup rescue, source weighting, or
post-outcome threshold change is allowed.

## Claim boundary

If both source cohorts pass the primary gates and both meet the pre-outcome 80%
design-sensitivity requirement: matrix-defined damaging STAG2 mutation status was
associated with a stronger STAG1 source-specific knockout dependency in both
frozen 23Q4 Avana and KY model populations under the lineage-stratified estimator.

This would corroborate a known genetic-dependency relationship in public cell-line
data. It would not establish novelty, causality in tumors, a druggable STAG1
inhibitor, therapeutic selectivity, patient benefit, or clinical utility. Failure
means only that this frozen endpoint/cohort/protocol did not reproduce the
predeclared direction.
