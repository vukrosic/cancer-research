# EXP-20260822-021 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `NF1 (4763)` status to `PTPN11 (5781)`
dependency. Selection is outcome-free: no PTPN11 score row or endpoint value
was opened when the candidate census, design receipt, and preregistration were
written.

The biological source reports a genetic dependency involving the NF1-loss
context and PTPN11/SHP2. That evidence motivates the direction but does not
turn the matrix proxy into functional NF1 loss. The proxy does not establish
allele state, protein state, RAS-pathway activity, or the absence of co-mutation
and lineage confounding. The endpoint is PTPN11 CRISPR knockout dependency, not
SHP2 inhibitor response.

## Required audit checks

- verify exact hashes and headers for the four metadata inputs and endpoint
  file;
- verify exact ScreenID-to-ModelID identity, eligible source/model counts, and
  nonblank lineages before endpoint access;
- verify NF1 matrix domain `{0,1,2}`, exact exposed/reference counts,
  mixed-lineage counts, and canonical roster hash;
- verify the sealed candidate census and deterministic planning powers before
  endpoint access;
- verify the implementation boundary includes the EXP021 wrapper, imported
  analysis engine, project entrypoint boundary, and `uv.lock`;
- verify the endpoint hash and exact PTPN11 header before any value parse;
- independently recompute delta, permutation p-values, bootstrap intervals,
  lineage gates, artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

The frozen question, candidate census, thresholds, and claim boundary must not
be rewritten after endpoint access. Any implementation deviation must be
recorded as a deviation and cannot be silently repaired by changing the
preregistration.

## Execution receipt

To be completed after the bound runner executes. The result bundle must remain
source-separated and preserve any null, heterogeneity, or feasibility-only
outcome without post hoc rescue.
