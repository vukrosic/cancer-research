# EXP-20260822-020 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `TP53 (7157)` status to `WEE1 (7465)`
dependency. Selection is outcome-free: no WEE1 score row or endpoint value was
opened when the candidate census, design receipt, and preregistration were
written.

The biological motivation is deliberately narrower than the proxy label.
Primary studies report TP53-associated WEE1 vulnerability, including p53-inactive
cell-line evidence and restricted KRAS-mutant NSCLC CRISPR/functional-genomic,
siRNA, and WEE1-inhibitor evidence. A damaging matrix call does not prove a pathogenic
biallelic TP53 alteration, loss of transcriptional function, absent TP53
protein, KRAS co-mutation, or replication stress. The endpoint is CRISPR
knockout dependency, not response to a selective WEE1 inhibitor.

## Required audit checks

- verify exact hashes and headers for the four metadata inputs and endpoint
  file;
- verify exact ScreenID-to-ModelID identity, eligible source/model counts, and
  nonblank lineages before endpoint access;
- verify TP53 matrix domain `{0,1,2}`, exact exposed/reference counts,
  mixed-lineage counts, and canonical roster hash;
- verify the sealed candidate census and deterministic planning powers before
  endpoint access;
- verify the implementation boundary includes the EXP020 wrapper, imported
  analysis engine, project entrypoint, and `uv.lock`;
- verify the endpoint hash and exact WEE1 header before any value parse;
- independently recompute delta, permutation p-values, bootstrap intervals,
  lineage gates, artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

The frozen question, candidate census, thresholds, and claim boundary must not
be rewritten after endpoint access. Any implementation deviation must be
recorded as a deviation and cannot be silently repaired by changing the
preregistration.

## Biological-source boundary

Fukuda et al. (PMID 38776912) report CRISPR screening and TP53-context WEE1
vulnerability in KRAS-mutated NSCLC; Joshi et al. (PMID 28978051) report
TP53-mutant versus TP53-wild-type context for a WEE1 inhibitor in KRAS-mutant
NSCLC; Pappano et al. (PMID 24927813) report p53-inactive cell-line evidence.
These sources justify testing the direction, not interpreting a matrix-defined
result as a treatment or clinical claim.

## Implementation receipt

The runner will be bound by manifest `experiments/EXP-20260822-020/manifest.json`.
The implementation boundary must be created after the outcome-free selection
seal and must bind the wrapper, imported engine, project entrypoint, and lock
file. The independent pre-endpoint audit must return **GO** before endpoint
values are parsed.

## Execution receipt

The bound runner completed with `1,292` eligible screens and `1,290`
source/model units. The terminal result is
`FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`, with `confirmatory_claim: false` and
`overall_pass: false`. Avana had a near-zero aggregate delta and failed its
effect, permutation, bootstrap, and no-positive-lineage gates. KY had a
negative aggregate delta and passed its effect, permutation, and bootstrap
gates, but failed the no-positive-lineage gate. The complete source-separated
result bundle, receipts, and audit are in this experiment directory.
