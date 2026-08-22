# EXP-20260822-003 preregistration

## Question

Does the known MSI-associated WRN loss-of-fitness signal replicate from Broad
Avana screens to held-out Sanger KY screens when the endpoint is a source-separated,
per-screen naïve gene score and tissue is controlled by within-tissue comparisons?

This is a positive-control recovery experiment for the reliability pipeline, not a
claim that WRN–MSI synthetic lethality is novel.

## Frozen population

- Release: DepMap Public 23Q4, Figshare article `24667905`, version 2.
- Sources: Avana/Broad discovery and KY/Sanger confirmation.
- Tissues: `Large Intestine`, `Ovary`, `Endometrium`, and `Stomach` exactly.
- Labels: `MSI` or `MSS` from the hash-locked Cell Model Passports model list dated
  2026-08-14.
- Include only one-to-one `BROAD_ID == ModelID` mappings and screens with
  `PassesQC == true` and `CanInclude == true`.
- Unit: one biological model in one source. If multiple eligible screens exist,
  collapse their WRN scores by median. The metadata audit found exactly one eligible
  screen per retained model in both libraries.
- No exclusion may depend on a WRN score or effect direction.

Frozen eligible counts before score access:

| Tissue | Avana MSI/MSS | KY MSI/MSS |
|---|---:|---:|
| Endometrium | 5 / 2 | 5 / 3 |
| Large Intestine | 7 / 18 | 10 / 20 |
| Ovary | 5 / 17 | 6 / 20 |
| Stomach | 3 / 12 | 4 / 10 |

Every tissue/source stratum must retain at least 2 MSI and 2 MSS endpoint values,
and at least 80% of label-eligible models in every source must have a finite WRN
score. Otherwise the experiment stops as a T0 availability failure.

## Frozen endpoint and direction

Primary endpoint: `WRN (7486)` from `ScreenNaiveGeneScore.csv`.

The release defines this matrix as log-fold-change scores collapsed by mean of
sequences and median of guides, computed per library-screen type and concatenated.
More negative means stronger loss of fitness. No joint cross-library correction,
quantile normalization, pooled scaling, imputation, or post-outcome calibration is
allowed.

## Primary estimand

Within each tissue, compare every MSI model with every MSS model. For pair
`(MSI, MSS)`, score `-1` if the MSI WRN score is lower, `+1` if it is higher, and
`0` for a tie. Pool only these within-tissue pair scores:

`stratified_delta = sum(pair scores) / number of within-tissue pairs`.

This is a pair-count-weighted, tissue-stratified Cliff-type delta. Negative values
support stronger WRN loss of fitness in MSI models. Cross-tissue pairs never enter
the estimand.

Also report tissue-specific Cliff deltas and the median of all within-tissue
MSI-minus-MSS pair differences.

## Inference

- One-sided permutation test: shuffle MSI/MSS labels within tissue while preserving
  the tissue-specific counts; 100,000 seeded permutations per source. The p-value is
  `(1 + count(delta_perm <= delta_observed)) / (100001)`.
- 95% confidence interval: 10,000 seeded stratified bootstrap resamples, sampling
  models with replacement within every tissue-by-label group.
- Seed: 20260824.

## Frozen gates

Broad/Avana is discovery. KY/Sanger is evaluated as held-out confirmation only if
Avana passes all primary gates. A source passes only if:

1. `stratified_delta < 0`;
2. `stratified_delta <= -0.33`;
3. one-sided permutation `p <= 0.05`;
4. the upper 95% bootstrap bound is below `+0.10`;
5. at least three of four tissue-specific deltas are negative; and
6. no tissue-specific delta is greater than `+0.33`.

Positive-control recovery requires both Avana and KY to pass. If Avana fails, KY
WRN values remain unevaluated by the analysis program and the result is a discovery
failure. If Avana passes and KY fails, the result is non-replication under this
protocol. Sensitivity analyses cannot rescue a failed primary result.

## Negative and integrity controls

- The permutation null is the primary negative control.
- Report released screen QC fields and endpoint completeness.
- Verify the score archive MD5 before parsing.
- Verify that the WRN column name and Entrez identifier are exact.
- Report all retained model IDs, tissues, labels, libraries, screen IDs, and scores
  in a derived audit table after unsealing.

## Blinding boundary

Before freezing this document, MSI/MSS labels, lineages, model identities, screen
libraries, QC flags, and cohort counts were observed. No MSI-conditioned WRN score,
WRN group contrast, WRN tissue effect, or WRN source effect had been read or
computed. The endpoint archive had not been downloaded.

## Maximum claim

If both sources pass: in this frozen public four-tissue cell-model cohort,
source-separated naïve CRISPR scores recovered the known association of MSI status
with stronger WRN knockout loss of fitness in both Broad Avana and Sanger KY screen
families under the preregistered tissue-stratified rule.

The result cannot establish novelty of the biological association, mechanism,
drug efficacy, therapeutic index, patient benefit, or clinical actionability.

