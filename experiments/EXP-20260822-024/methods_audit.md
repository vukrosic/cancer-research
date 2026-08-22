# EXP-20260822-024 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `KMT2D (8085)` status to `KMT2C
(58508)` dependency. Selection is outcome-free: no KMT2C score row or endpoint
value was opened when the candidate census, design receipt, and
preregistration were written.

The primary 2026 AACR report supports a KMT2D-null/KMT2C CRISPR dependency in
DLBCL and KMT2D isogenic models. This is emerging evidence, not a license to
generalize across all cancers. The mutation matrix does not establish
functional KMT2D loss, and no claim about lymphoma-specific causality, drug
response, or clinical benefit is permitted. Lineage, co-mutation, protein
state, and assay differences remain alternative explanations.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP024 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact KMT2C header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Execution receipt

To be completed after the bound runner executes. Preserve any null,
heterogeneous, or feasibility-only outcome without post hoc rescue.
