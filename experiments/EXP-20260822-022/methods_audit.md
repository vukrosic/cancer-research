# EXP-20260822-022 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `EP300 (2033)` status to `CREBBP
(1387)` dependency. Selection is outcome-free: no CREBBP score row or endpoint
value was opened when the candidate census, design receipt, and
preregistration were written.

The biological source supports a CRISPR-observed EP300/CREBBP paralog
interaction. It does not turn the mutation matrix into functional EP300 loss
and does not justify claims about paralog causality, inhibitor response, or
clinical benefit. Lineage, co-mutation, protein state, and assay differences
remain alternative explanations.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP022 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact CREBBP header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.

## Execution receipt

To be completed after the bound runner executes. Preserve any null,
heterogeneous, or feasibility-only outcome without post hoc rescue.
