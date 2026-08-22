# EXP-20260822-018 execution log

## Run

- Result bundle mtime: `2026-08-22T17:39:25+0200`.
- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-cdkn2a-tyms-replication`.
- Exit code: `2`, expected because the runner permanently labels this
  feasibility-only and sets `overall_pass: false`.
- Endpoint parsing occurred only after the implementation boundary, endpoint
  hash, context ledger, design sensitivity, and pre-endpoint receipt passed.
- The runner wrote the complete five-file result bundle atomically.

## Receipts

- Eligible screens: `1292`; canonical source/model units: `1290` (`975` Avana,
  `315` KY).
- Canonical roster SHA-256:
  `df50a72ac86b161e16ebc5a2eb2b2f5c8d35151d94da4046c375f5ab0f603bb5`.
- Pre-endpoint receipt SHA-256:
  `0881b51c26325027bbb68a78f4b6c0991f375ae36b14571d833eaa46642febfd`.
- Endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.
- Summary normalized self-digest:
  `520a1c9bc1115fab92f080c1b98ab07242c80939e67e753a1414709622027c81`.

## Claim safety

The terminal summary contains `analysis_label: FEASIBILITY_ONLY`,
`confirmatory_claim: false`, and `overall_pass: false`. The KY planning power
was `0.5364`, below the frozen `0.80` confirmatory threshold, so no
two-source confirmatory claim is permitted regardless of endpoint direction.
