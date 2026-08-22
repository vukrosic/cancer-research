# EXP034 execution log

## Frozen boundary

- selection seal commit: `7a37a23`;
- implementation commit: `cbec294`;
- manifest binding commit: `8417224`;
- endpoint target column: `TDG (6996)`;
- status column: `TP53 (7157)`;
- runner: `.venv/bin/python -m candrel.tp53_tdg_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `22` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. The pre-endpoint
receipt was written before TDG scores were parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

## Result receipts

- context ledger: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`;
- design sensitivity: `27bd90078c4818c9aa73fe7b9e8ac5a450eb68e47e771510a304e11684e397f9`;
- endpoint scores: `edafcd0ca1e447ce853283bb6f3497b4dd961a421061cd3ceb9092f713806da1`;
- inference: `62e88924779766e3933400cd3a323e1c0797c3d184a2303efc6f0aee279e0dca`;
- normalized `summary.json`: `69fdc4222e745c80245bc752b181259d731bf03669190201769d36677644d20c`;
- pre-endpoint receipt: `d15ac4493f852ea5113acfad4970ace2f4111c37a52ba9e98ec98f354e0f6be7`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the committed data and
frozen engine.
