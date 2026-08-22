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
