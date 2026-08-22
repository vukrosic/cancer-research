# EXP-20260822-019 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `PTEN (5728)` status to `PIK3CB
(5291)` dependency. Selection is outcome-free: no PIK3CB score row or endpoint
value was opened when the candidate census, design receipt, and preregistration
were written.

The primary biological motivation is a 2008 genetic study reporting that
PTEN-deficient cancer models depended on the p110-beta isoform encoded by
PIK3CB. The proxy risk is substantial: a damaging matrix call does not prove
biallelic PTEN loss, absent PTEN protein or phosphatase activity, copy-number
loss, pathway state, or the absence of PIK3CA/RAS co-alterations. The endpoint
is CRISPR knockout dependency, not response to a selective PI3K-beta inhibitor.

## Required audit checks

- verify exact hashes and headers for the four metadata inputs and endpoint file;
- verify exact ScreenID-to-ModelID identity, eligible source/model counts, and
  nonblank lineages before endpoint access;
- verify PTEN matrix domain `{0,1,2}`, exact exposed/reference counts, mixed
  lineages, and canonical roster hash;
- verify the sealed candidate census and deterministic planning powers before
  endpoint access;
- verify the implementation boundary includes the EXP019 wrapper, imported
  analysis engine, project entrypoint, and `uv.lock`;
- verify the endpoint hash and exact PIK3CB header before any value parse;
- independently recompute delta, permutation p-values, bootstrap intervals,
  lineage gates, artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

The frozen question, candidate census, thresholds, and claim boundary must not
be rewritten after endpoint access. Any implementation deviation must be
recorded as a deviation and cannot be silently repaired by changing the
preregistration.

## Implementation receipt

The runner is bound by manifest `experiments/EXP-20260822-019/manifest.json`.
The implementation commit is `98a9ee33a7346175f3354b7f304b9542e0c20269`, based
on the outcome-blind selection seal commit
`d061a93c239e48944e8fec3d54f6b4ae0460224c`. The independent pre-endpoint audit
returned **GO** at manifest commit
`776d4564b46cf64a436abd2c5ea53647e4ba1e8c`; no endpoint values were opened by
that audit.

## Execution receipt

The bound runner completed the frozen protocol with `1292` eligible screens and
`1290` source/model units. The complete result bundle is in `results/`; endpoint
access occurred only after the sealed context and design receipts. The terminal
result is `FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`, with
`confirmatory_claim: false` and `overall_pass: false`. Avana failed lineage
consistency despite a negative aggregate delta; KY was near zero and failed
effect, permutation, bootstrap, and lineage gates. Exact receipt and artifact
hashes are in `execution_log.md` and `result.md`.
