# EXP030 execution log

## Frozen boundary

- selection seal protocol commit: `bfebf4b`;
- initial implementation commit: `90cc823`;
- pre-endpoint planning correction commit: `d29e368`;
- corrected manifest binding commit: `595a9a1`;
- endpoint target column: `CIP2A (57650)`;
- composite status columns: `BRCA1 (672)`, `BRCA2 (675)`;
- runner: `.venv/bin/python -m candrel.brca12_cip2a_replication`;
- endpoint values were not parsed before the corrected pre-endpoint receipt.

## T0 correction

The first single runner invocation returned exit code `2` at
`T0_CONTEXT_ADEQUACY` because the sealed receipt expected the previous
experiment's planning powers despite using EXP030 seeds. It preserved context
and design provenance under `t0_provenance/` and wrote `error_receipt.json` with
`endpoint_opened: false` in `t0_error_receipt.json`. The correction is documented in
`selection_correction.md`; no endpoint value was inspected or used.

## Valid execution

After the correction and manifest rebinding, the runner was invoked exactly once.
It completed in approximately `21` seconds and returned exit code `2`, as
required by the permanent feasibility-only contract. The pre-endpoint receipt
was written before CIP2A scores were parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

## Result receipts

- context ledger: `34c142633cd4f9070a062ab6a501da5e575e555e9aa19f078120d0756153cb70`;
- design sensitivity: `638c33df6c667698b771c4eea4f7b3d66868b80efd29fa936a9b221f511b33a2`;
- endpoint scores: `f429f097a4211f5f852c00d75228b2652156d466ffd4aa4ec418456a06395702`;
- inference: `900e5acb2920ee0d8c0c93d1a5610fde4870f1dd16ec747161bc609612f23c0d`;
- normalized `summary.json`: `4dca3f078addb236a98dcda123073a41b5d4cbbd58e97649b2f207ce5a5fe2af`;
- pre-endpoint receipt: `c3e674ab7debc991c01ea3f8cf0c5b6ef9431b7aa902ea740b44434c8e9730e9`.

## Verification

The independent audit returned `GO` and recomputed the same summary digest and
source-specific statistics from the committed data and frozen engine.
