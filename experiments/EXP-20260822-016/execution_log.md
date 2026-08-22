# EXP-20260822-016 execution log

## Attempt 001 — 2026-08-22 16:32 +0200

- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-keap1-replication`
- Boundary: implementation commit/module, lockfile, manifest contract, input
  hashes, context ledger, and design receipt completed before KEAP1 endpoint
  parsing. The durable pre-endpoint receipt links the context and design CSV
  hashes.
- Outcome: all five result artifacts published; process exit code `2` because
  the frozen analysis is feasibility-only and nominal gates do not pass.
- Completeness: 1,292 eligible screens, exactly once; 1,290 source/model
  endpoint units; two Avana duplicate-screen models median-collapsed.
- Result: Avana delta `-0.0545454545`, p `0.2320476795`, CI
  `[-0.1791443850, 0.0695187166]`, failed four nominal gates. KY delta
  `-0.2275379230`, p `0.0207097929`, CI `[-0.4095682614, -0.0431738623]`,
  failed lineage consistency due Bone `+1.0`, CNS/Brain `+0.75`, and Lymphoid
  `+0.7777777778`.

## Protocol deviation

The frozen shortlist candidate census recorded approximate outcome-free power
`0.8622` Avana and `0.5699` KY. The executable canonical sorted-roster design
receipt recorded `0.8652` and `0.5875`. The preregistration required the
execution receipt to reproduce the planning draw exactly; it did not.

This discrepancy is outcome-free and does not alter the endpoint, estimator,
inference, or gate thresholds, and KY remains below 0.80 in both receipts.
Nevertheless, it is a real frozen-protocol deviation. EXP016 is therefore
released only as an internally reproducible, non-confirmatory protocol-
deviation artifact; it must not be described as a clean preregistered receipt.
