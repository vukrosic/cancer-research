# EXP-20260822-016 preregistration — predeclared feasibility-only audit

This experiment is **FEASIBILITY_ONLY from the protocol freeze**. The frozen
outcome-free KY design-sensitivity power is approximately 0.5699, below the
0.80 confirmatory threshold. No endpoint result can upgrade this experiment to
a confirmatory two-source claim.

## Question and prior art

Does matrix-defined damaging `ARID1A` mutation status predict stronger
source-specific `KEAP1` knockout dependency in Avana and KY cancer cell-line
screens?

This is a replication/reliability audit of a recent primary CRISPR study, not a
novelty or treatment claim. The study reported KEAP1 perturbation as a
vulnerability of ARID1A-deficient cells and validated the effect in clear-cell
ovarian cancer models and edited primary endometrial epithelial cells:

- https://pmc.ncbi.nlm.nih.gov/articles/PMC11394604/

The result, if positive, would test whether that context-dependent relationship
survives the frozen DepMap source-specific screen cohorts. It would not prove
that KEAP1 is a universal ARID1A dependency or a clinical target.

## Outcome-free candidate selection

The following alternatives were inspected using only eligibility metadata and
the damaging-status matrix, without parsing any target endpoint values:

- EP300 status → CREBBP dependency: 61/914 Avana and 34/281 KY damaging/intact
  models, but outcome-free simulated power approximately 0.7324/0.4798.
- SMARCA4 status → SMARCA2 dependency: 51/924 Avana and 13/302 KY, failing the
  minimum 20-damaging-model context gate in KY.
- MTAP status → PRMT5 dependency: 2/973 Avana and 1/314 KY under the frozen
  damaging mutation matrix, failing context adequacy despite strong literature
  interest.
- ARID1A status → KEAP1 dependency: 101/874 Avana and 43/272 KY, with 19/11
  mixed lineages. This is the selected direction because it is adequately
  represented in both sources and is directly motivated by recent primary
  CRISPR evidence. Its KY power remains below the confirmatory threshold, so
  the label is frozen as feasibility-only.

The complete shortlist, eligibility rule, input receipts, literature search
date, target-header identities, counts, and outcome-free power receipts are
sealed in `candidate_census.json` (SHA-256
`27c24b951e4e213dc44e371b6d2b4595b2530de504e60920d715fc496f657bbe`). This is
the candidate universe for this selection round; it is not a claim that every
possible cancer dependency pair was exhaustively enumerated.

## Frozen release, source, unit, and joins

- Release: DepMap Public 23Q4, Figshare article `24667905`, version 2.
- Sources: `Avana` and `KY` exactly. They are source-specific corroboration
  cohorts from one release, not biologically independent cohorts.
- Eligibility: `PassesQC == True`, `CanInclude == True`, and `Library` exactly
  `Avana` or `KY` in `AchillesScreenQCReport.csv`.
- `ScreenID` must be unique among eligible QC rows and must join exactly once to
  `CRISPRScreenMap.csv` with the same `ModelID`. Each joined ModelID must occur
  exactly once in `Model.csv` and have a nonblank `OncotreeLineage`; unrelated
  metadata rows may be blank, but an eligible blank lineage is an integrity
  stop.
- Unit: one `(source, ModelID)`. Multiple eligible screens within that unit are
  collapsed by the median KEAP1 score, preserving all screen IDs in the ledger.
- The damaging matrix joins by exact ModelID, with values restricted to
  `{0,1,2}` and status defined as value `>=1`.
- The endpoint joins by exact ScreenID. Duplicate eligible endpoint rows,
  non-finite values, or missing source/model completeness are integrity/T0
  stops; no imputation, exclusion, or threshold rescue is allowed.

Exact columns:

- exposure: `ARID1A (8289)` in `OmicsSomaticMutationsMatrixDamaging.csv`;
- endpoint: `KEAP1 (9817)` in `ScreenNaiveGeneScore.csv`.

## Frozen input receipts

- `ScreenNaiveGeneScore.csv`: SHA-256
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`, official
  MD5 `265f8372e9cd0fad56c1a6b66b8a783d`;
- `AchillesScreenQCReport.csv`: SHA-256
  `fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407`;
- `CRISPRScreenMap.csv`: SHA-256
  `1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad`;
- `Model.csv`: SHA-256
  `6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341`;
- `OmicsSomaticMutationsMatrixDamaging.csv`: SHA-256
  `aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3`.

## Outcome-blind adequacy and execution order

Before opening or parsing `KEAP1 (9817)`, verify all hashes, exact headers,
identity joins, eligible source/model counts, finite matrix states, and the
exact ARID1A status column. Write the complete context ledger before endpoint
access. The context gate requires, per source, at least 20 damaging models, 50
intact models, and 5 mixed lineages. Frozen counts are Avana 101/874/19 and KY
43/272/11.

If context adequacy fails, stop as `T0_CONTEXT_ADEQUACY` without opening the
endpoint. After the ledger is sealed, compute and hash the design-sensitivity
receipt. Write the pre-endpoint receipt durably before opening the endpoint.
Then run the sealed completeness gate; only after it passes may any contrast or
inference be computed. If completeness fails, stop as
`T0_ENDPOINT_COMPLETENESS` and preserve the staged context/design artifacts.

Named pre-endpoint stops are: `T0_INPUT_HASH`, `T0_SCHEMA_HEADER`,
`T0_IDENTITY_JOIN`, `T0_MATRIX_COVERAGE`, `T0_CONTEXT_ADEQUACY`, and
`T0_IMPLEMENTATION_BOUNDARY`. Any of these stops prohibits endpoint access.
`T0_ENDPOINT_COMPLETENESS` is the only named stop after the endpoint is opened;
it emits no effect or group summary and preserves the pre-endpoint artifacts.

Before endpoint access, verify that the manifest's required base commit is
resolvable and an ancestor of the checkout, that the implementation commit is
resolvable and its module SHA-256 matches the manifest, and that `uv.lock` and
the manifest's frozen identifiers/hashes match the runner. A mismatch stops as
`T0_IMPLEMENTATION_BOUNDARY`.

## Pre-outcome design sensitivity

Hold the observed lineage group sizes fixed. Intact scores are independent
`Normal(0,1)` and damaging-status scores are independent
`Normal(-0.358286909243,1)`, using the shift `-sqrt(2) * Phi^-1(0.60)` so the
expected pairwise direction statistic is approximately `-0.20`.

Use NumPy PCG64 with separate design seeds `20261630` for Avana and `20261730`
for KY. Generate 100,000 within-lineage label-permutation null draws, use the
linear empirical 5% lower critical value, then generate 10,000 alternatives and
count rejection with `alternative_delta <= critical_delta`. The outcome-free
planning power from these exact seeds is approximately 0.8622 Avana and 0.5699
KY; the realized finite execution receipt must reproduce this outcome-free
design draw before endpoint loading and use the frozen label rule.

Because KY is below 0.80, the experiment is permanently `FEASIBILITY_ONLY`.
The final claim Boolean must remain false even if nominal gates pass.

## Estimand and inference

For each source and mixed lineage, compare KEAP1 target scores pairwise:
`c=-1` when damaging is lower, `c=+1` when damaging is higher, and `c=0` for
a tie. The source estimand is exactly
`delta_s = sum(c(i,j)) / number_of_within_lineage_damaging×intact_pairs`.
No cross-lineage or cross-source pair enters.

Use 100,000 independent within-lineage permutations with direct floating-point
`<=` lower-tail counting and p-value exactly
`(1 + count(delta_perm <= delta_observed)) / 100001`. Use 10,000 bootstrap
resamples at the collapsed `(source, ModelID)` unit within every lineage×status
group and NumPy linear percentile intervals; a zero denominator is an integrity
stop with no redraw. Use inference seeds `20271630` Avana and `20271730` KY.

Both sources must nominally pass: delta `<0`; delta `<=-0.20`; p `<=0.05`;
bootstrap upper bound `<0`; at least five negative lineage deltas; and no
lineage delta `>+0.20`. These are feasibility receipts only; no pooling,
source weighting, subgroup rescue, FDR, regression, or post-outcome threshold
change is permitted.

Every terminal summary must contain `analysis_label: FEASIBILITY_ONLY` and
`confirmatory_claim: false`, including if both nominal source gate sets pass.

## Claim boundary

The strongest permitted conclusion is a feasibility/robustness receipt for the
matrix-defined ARID1A-status versus KEAP1-dependency direction in these frozen
cell-line screen cohorts. It cannot establish novelty, causality, functional
or biallelic ARID1A loss, universal dependency, druggability, patient benefit,
or clinical utility.
