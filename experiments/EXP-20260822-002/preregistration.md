# EXP-20260822-002 preregistration

## Question

On a frozen eight-gene panel and identical paired Broad/Sanger models, does the
derived `fc_clean_qn` representation materially increase measured cross-source rank
agreement relative to source-labelled `bf_scaled`?

## Hypothesis and falsification

The hypothesis is that processing represented by `fc_clean_qn` increases apparent
agreement. It passes only if both are true:

1. the median across-gene difference
   `Spearman(fc_clean_qn) - Spearman(bf_scaled)` is at least 0.10; and
2. at least six of eight genes have a positive difference.

The hypothesis is falsified if either condition fails. A failed result will be
preserved and will not be rescued by changing the panel, paired cohort, score field,
or threshold.

## Frozen data and unit

- API and immutable normalized responses are exactly those hash-locked by
  `EXP-20260822-001/input_receipt.json`.
- Panel: `WRN, BRAF, KRAS, NRAS, EGFR, PIK3CA, CTNNB1, MDM2`.
- Unit: one Cell Model Passports model within one gene.
- Duplicate records within a model/source/field are collapsed by the median.
- Include only `qc_pass != false`, non-null field values, and models present in both
  Broad and Sanger for both fields.
- Each gene must have at least 100 identical paired models under both fields; all
  eight genes must pass this data-integrity gate.

## Endpoints

Primary:

- gene-wise Broad/Sanger Spearman correlation for `fc_clean_qn`;
- gene-wise Broad/Sanger Spearman correlation for `bf_scaled`;
- paired difference and its median across genes.

Secondary, non-rescuing:

- fraction of genes with a positive paired difference;
- 2,000 deterministic model-level bootstrap resamples per gene and a 95% interval
  for each correlation difference;
- source-labelled unscaled `bf` correlation as a descriptive sensitivity analysis.

The eight genes are a fixed panel, not a random sample of the genome. No population-
wide p-value or biological generalization will be made.

## Blinding boundary

Before freezing this document, `fc_clean_qn` results from EXP-001 were known. Panel-
level `bf_scaled` or `bf` correlations had not been computed. Non-panel probes on
POLR2A, RPL3, and FOXA1 were used only to verify score direction and field
availability. The MSI–WRN contrast remains sealed.

## Seed, budget, and stopping

- Seed: 20260823.
- Bootstrap resamples: 2,000.
- Mac budget: under 10 minutes and no new bulk download.
- Stop on receipt drift, partial API responses, non-identical paired cohorts, fewer
  than 100 pairs for any gene, or non-finite correlations.

## Maximum claim

If the gates pass: within this fixed panel and historical API snapshot,
`fc_clean_qn` produced materially higher Broad/Sanger rank agreement than
source-labelled `bf_scaled`. This would demonstrate processing sensitivity, not prove
that any specific correction is invalid or that raw screens disagree biologically.
