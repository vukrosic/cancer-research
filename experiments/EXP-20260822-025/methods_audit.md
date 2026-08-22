# EXP-20260822-025 methods audit

## Pre-implementation review target

The frozen direction is damaging-matrix `CDKN2A (1029)` status to `PELO
(53918)` dependency. Selection is outcome-free: no PELO score row or endpoint
value was opened when the candidate census, design receipt, and
preregistration were written.

The primary 2025 Nature study supports PELO dependency in biallelic 9p21.3
deletion and MSI-H contexts and identifies FOCAD loss as the causal 9p21.3
driver. CDKN2A mutation is only a proxy in this experiment and is not
equivalent to 9p21.3 copy-number loss, FOCAD loss, or MSI-H. No claim about
mechanistic causality, drug response, treatment benefit, or clinical utility
is permitted.

## Required audit checks

- verify exact input hashes, headers, screen identity, source/model counts,
  status counts, mixed lineages, and canonical roster before endpoint access;
- verify the sealed candidate census and deterministic planning powers;
- verify the implementation boundary includes the EXP025 wrapper, imported
  engine, historical project-file hash, and `uv.lock`;
- verify the exact PELO header before any value parse;
- independently recompute deltas, p-values, bootstrap intervals, lineage gates,
  artifact hashes, and normalized summary digest;
- require terminal `analysis_label: FEASIBILITY_ONLY`,
  `confirmatory_claim: false`, and `overall_pass: false`.
