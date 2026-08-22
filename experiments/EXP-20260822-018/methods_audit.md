# EXP-20260822-018 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `CDKN2A (1029)` status to `TYMS (7298)`
dependency. Selection is outcome-free: no TYMS score row or endpoint value was
opened when the candidate census and preregistration were written.

The primary risk is biomarker semantics. The matrix is not a deletion or
biallelic-functional-loss assay, and the literature indicates that TYMP
expression and tissue context can sharpen the CDKN2A/TYMS relationship. The
primary analysis therefore remains the simpler, fully available matrix-defined
contrast; TYMP-high and tissue rescue are not permitted after endpoint access.

Required checks before execution:

- freeze the canonical roster and exact design receipt, including lineage counts,
  critical values, RNG/order, and hashes;
- bind all input, candidate-census, design-receipt, implementation, and `uv.lock`
  hashes in the manifest;
- classify metadata failures into the preregistered T0 labels;
- check endpoint hash and exact TYMS header before any value parse;
- independently recompute all artifact hashes, delta/p/bootstrap receipts,
  lineage gates, and terminal T1/feasibility-only labels.

## Implementation receipt

The runner is bound by manifest `experiments/EXP-20260822-018/manifest.json`.
The implementation commit is `efc6ac57720a1a0c9d63b1168bfedec6535c507c`, based
on protocol commit `7fd110353d8e310948e16dc5245f3d87f5b8c5f4`. The independent
pre-endpoint audit returned **GO** at manifest commit
`d92eb0656d46c514b4954e9232bd9bf11b48be86`; no endpoint values were opened by
that audit.

## Execution receipt

The bound runner completed the frozen protocol with `1292` eligible screens and
`1290` source/model units. The complete result bundle is in `results/`; endpoint
access occurred only after the sealed context and design receipts. The terminal
result is `FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`, with
`confirmatory_claim: false` and `overall_pass: false`. KY planning power was
`0.5364`, below the frozen `0.80` confirmatory threshold, and both sources
failed at least one nominal gate. Exact receipt and artifact hashes are in
`execution_log.md` and `result.md`.
