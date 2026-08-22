# EXP-20260822-015 preregistration — predeclared feasibility-only audit

This experiment is **FEASIBILITY_ONLY from the protocol freeze** because the
outcome-free KY design-sensitivity power is 0.5636, below the frozen 0.80
confirmatory threshold. No observed endpoint result, nominal p-value, interval,
or gate pass can upgrade this experiment to a confirmatory two-source claim.

## Question

Does matrix-defined damaging `ARID1A` mutation status predict stronger
source-specific `ARID1B` knockout dependency in Avana and KY cancer cell-line
screens?

This is a replication-first audit of a published SWI/SNF paralog vulnerability,
not a novelty or treatment claim. The primary interaction was reported as an
ARID1B dependency in ARID1A-mutant cancer cell lines, with experimental
validation in mutant and wild-type models:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC3954704/
- https://pmc.ncbi.nlm.nih.gov/articles/PMC5643100/

## Frozen release, source, and unit

- Release: DepMap Public 23Q4, Figshare article `24667905`, version 2.
- Sources: `Avana` and `KY` exactly, treated as source-specific corroboration
  cohorts from the same public release. They are not assumed to be independent
  biological cohorts, and no raw score comparison across sources is made.
- Screen eligibility: `PassesQC == true`, `CanInclude == true`, and `Library` in
  `{Avana, KY}` from `AchillesScreenQCReport.csv`.
- Unit: one `ModelID` within one source. If multiple eligible screens exist for a
  source/model, collapse the ARID1B score by the median, preserving all eligible
  screen IDs in the derived ledger.
- Lineage: `OncotreeLineage` from the hash-locked `Model.csv`, used only for
  within-lineage comparisons. No lineage is selected after target-score access.

## Frozen join and identity contract

- `AchillesScreenQCReport.csv` is the eligibility table. `ScreenID` must be
  unique among eligible rows; `Library` must be exactly `Avana` or `KY`, and
  `PassesQC` and `CanInclude` must each be the literal string `True`.
- Each eligible QC `ScreenID` must occur exactly once in
  `CRISPRScreenMap.csv`, and its mapped `ModelID` must equal the QC row's
  `ModelID`. Each joined `ModelID` must occur exactly once in `Model.csv` and
  have a nonblank `OncotreeLineage`; a blank or unrecognized model/lineage is
  an integrity stop, never an exclusion.
- The damaging matrix is joined by exact `ModelID` in its first column. Its
  `ARID1A (8289)` header must occur exactly once, values must be in `{0,1,2}`,
  and every eligible ModelID must have one value. A matrix row for an
  unrecognized model is ignored only after duplicate-row validation.
- The endpoint is joined by exact `ScreenID` in its first column. An eligible
  screen may contribute one finite ARID1B value; duplicate endpoint rows are
  an integrity stop. Missing/blank screen values are not imputed, and a
  source/model is complete only when at least one of its eligible screens has
  a finite value; otherwise the preregistered endpoint stop fires.
- A contributing lineage is defined before endpoint access as a lineage with
  at least one damaging-status and at least one intact ModelID within the same
  source. The permutation scope is exactly these predeclared mixed lineages.

The exact columns are:

- exposure: `ARID1A (8289)` in the damaging-status matrix;
- endpoint: `ARID1B (57492)` in `ScreenNaiveGeneScore.csv`.

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
value `>=1`; it is not assumed to prove functional or biallelic ARID1A loss. No
mutation class, threshold, or gene filter may change after endpoint access.

## Outcome-blind adequacy and execution order

Before opening or parsing the ARID1B endpoint column, verify all input hashes,
exact headers, unique screen/model identities, eligible source/model coverage,
finite damaging states, and the exact ARID1A matrix column. Write a complete
context ledger containing every eligible source/model, lineage, matrix value,
status, and eligible screen IDs before reading ARID1B scores.

The pre-outcome context gate requires, for each source:

- at least 20 matrix-damaging-status models;
- at least 50 intact models; and
- at least 5 lineages containing both damaging-status and intact models.

The outcome-free candidate census measured 101 damaging-status and 874 intact
Avana models across 19 mixed lineages, and 43 damaging-status and 272 intact KY
models across 11 mixed lineages. These counts are frozen before endpoint access.

If any context gate fails, stop as `T0_CONTEXT_ADEQUACY` without opening the
ARID1B endpoint. After the context ledger is sealed, open the endpoint only to run
a sealed completeness gate: every predeclared eligible source/model must have one
finite ARID1B score after the frozen median collapse, and every required
lineage×status group must remain nonempty. This gate emits no group summary or
effect. If it fails, stop as `T0_ENDPOINT_COMPLETENESS` with no imputation,
model exclusion, or threshold rescue. Only after it passes may contrasts or
inference be computed.

## Pre-outcome design sensitivity

Before endpoint access, compute a design-sensitivity receipt from the exact context
roster. Under the frozen sensitivity model, intact and damaging-status scores are
independent Normal variables with common unit variance and a common mean shift
calibrated so the expected pairwise direction statistic is `delta=-0.20`; the
observed lineage group sizes are held fixed. Generate the frozen 100,000-label-
permutation null distribution once for each source and use its empirical lower-
tail 5% critical value, then simulate 10,000 alternative datasets and count the
fraction below that critical value.

The alternative is explicit: intact scores are independent `Normal(0, 1)` and
damaging-status scores are independent `Normal(-0.358286909243, 1)`, with the
shift defined as `-sqrt(2) * Phi^-1(0.60)` so the expected pairwise direction
statistic is approximately `delta=-0.20`. Use NumPy's default PCG64 generator,
seed `20260830` for Avana and `20260930` for KY, with no shared RNG state.
Use NumPy's `method="linear"` empirical quantile for the 5% critical value and
count a simulated rejection when `alternative_delta <= critical_delta`.

Because KY is below 80% under this frozen design, the experiment is permanently
`FEASIBILITY_ONLY`. The inferential run still uses the frozen estimator and
thresholds, but its final claim-eligibility Boolean must remain false even if
both observed source-specific gate sets pass. This design label cannot change
after endpoint access.

The outcome-free census predicted approximate power of 0.8651 for Avana and
0.5636 for KY under this exact design-sensitivity model. These are planning
receipts, not endpoint results.

## Frozen estimand

For loss-status model `i`, intact model `j`, source `s`, and lineage `l`, compare
the ARID1B target score `Y`:

`c(i,j) = -1` if `Y_damaging < Y_intact`, `+1` if `Y_damaging > Y_intact`, and `0`
for a tie. More negative log-fold-change means stronger loss of fitness. The
source estimand is the pair-count-weighted, within-lineage direction statistic:

`delta_s = sum(c(i,j)) / number of within-lineage damaging×intact pairs`.

No cross-lineage or cross-source pair enters the estimand. The median scores, pair
counts, and lineage-specific deltas are descriptive receipts only.

## Inference

- One-sided within-lineage permutation: independently shuffle damaging/intact
  labels within each lineage while preserving that lineage's observed damaging
  count and compute `delta_s`; only the pre-endpoint mixed lineages enter the
  permutation. Use 100,000 repeats and the lower-tail plus-one p-value
  `(1 + count(delta_perm <= delta_observed)) / 100001`, with the direct IEEE
  floating-point `<=` comparison and no tolerance or tie randomization.
- Bootstrap: 10,000 source-specific resamples with replacement at the collapsed
  ModelID unit within every lineage×status group. Recompute the same delta and
  report the percentile 95% interval using NumPy's default linear quantile method
  (`method="linear"`). A zero comparison denominator is an implementation
  integrity failure; never discard or redraw a replicate.
- Seeds: `20270830` for the Avana inferential stream and `20270930` for KY;
  these are separate from the design-sensitivity streams and are not advanced
  by another analysis.

## Frozen gates

Both Avana and KY must independently pass all six primary gates:

1. `delta_s < 0`;
2. `delta_s <= -0.20`;
3. one-sided permutation `p <= 0.05`;
4. bootstrap 95% upper bound `< 0`;
5. at least five contributing lineages have negative lineage-specific delta; and
6. no contributing lineage has delta `> +0.20`.

The primary confirmatory claim is permanently disabled for this experiment by
the frozen KY power of 0.5636. The six gates remain a nominal feasibility and
robustness receipt only. No source weighting, pooled source analysis, FDR
adjustment, composite, regression, subgroup rescue, or post-outcome threshold
change is allowed.

## Claim boundary

The strongest permitted conclusion, even if both source cohorts pass all six
nominal gates, is: the frozen data provide a feasibility/robustness receipt for
the predeclared matrix-defined ARID1A-status versus ARID1B-dependency direction.
No confirmatory two-source replication sentence is permitted because KY fails
the frozen design-sensitivity threshold.

This would corroborate a known SWI/SNF genetic-dependency relationship in public
cell-line data. It would not establish novelty, functional or biallelic ARID1A
loss, causality in tumors, a druggable ARID1B inhibitor, therapeutic selectivity,
patient benefit, or clinical utility. Failure means only that this frozen
endpoint/cohort/protocol did not reproduce the predeclared direction.
