# EXP-20260822-015 execution log

## Attempt 001 — 2026-08-22 15:59:54 +0200

- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-replication`
- Outcome: `ERROR_INTEGRITY`; no result directory was published.
- Durable error: `error_receipt.json` reported `invalid Model.csv identity:
  ACH-003132`.
- Endpoint boundary: `endpoint_opened=false` in substance. The stop occurred
  while loading hash-locked `Model.csv`, before context completion, before the
  pre-endpoint receipt, and before `load_endpoint` could open
  `ScreenNaiveGeneScore.csv`; no ARID1B score was parsed.
- Cause: the first implementation treated any blank lineage anywhere in
  `Model.csv` as invalid. The offending model is a non-eligible non-cancer
  model; the preregistered contract requires nonblank lineage for joined
  eligible models, not for unrelated rows in the full metadata table.
- Correction: allow blank lineage in unrelated metadata rows, then reject it
  when an eligible QC/model join selects that model. This preserves the exact
  eligible-model identity gate without excluding unrelated metadata.

## Attempt 002 — 2026-08-22 16:01–16:02 +0200

- Command: `UV_CACHE_DIR=/tmp/cancer-research-uv-cache uv run candrel-arid1a-replication`
- Outcome: published the complete result directory; process exit code `2` is
  the preregistered non-confirmatory outcome, not an integrity failure.
- Endpoint boundary: context and design receipts were written and hashed before
  ARID1B loading; 1,292 eligible screens and 1,290 source/model units passed
  endpoint completeness, with median collapse for duplicate source/model
  screens.
- Execution design receipt: Avana power `0.8642`, KY power `0.5787`; these are
  the realized seeded Monte Carlo receipt. The separate manifest values
  Avana `0.8651` and KY `0.5636` are frozen outcome-free planning estimates
  from the candidate census and are not expected to be byte-identical to a new
  finite simulation draw. KY remains below `0.80` in both receipts.
- Scientific result: Avana delta `-0.4582887701` passed all six nominal gates.
  KY delta `-0.2158693116` passed direction, effect-size, permutation, and
  negative-lineage gates but failed the bootstrap-upper-bound gate (upper
  bound `0.0058343057`) and lineage-consistency gate (Bone `+1.0`, Pancreas
  `+0.2666666667`).
- Claim: `FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE`; confirmatory eligibility and
  overall pass are both false by protocol.
