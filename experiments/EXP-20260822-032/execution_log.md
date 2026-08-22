# EXP032 execution log

## Frozen boundary

- selection seal commit: `f248a25`;
- implementation commit: `8d3a697`;
- manifest binding commit: `4f80c21`;
- post-execution wrapper-isolation hardening: `cc9aa4a`;
- corrected manifest rebinding: `7f8c6a8`;
- endpoint target column: `AURKA (6790)`;
- status column: `SMAD4 (4089)`;
- runner: `.venv/bin/python -m candrel.smad4_aurka_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `19` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. The pre-endpoint
receipt was written before AURKA scores were parsed. It reports `1,292`
eligible screens, `1,290` source/model values, and
`sealed_before_endpoint: true`.

## Result receipts

- context ledger: `c1305ac91f5d1cd9064a3c00cb2980dac77b2fbf99990381ac34d25cf5d33b1e`;
- design sensitivity: `36f1f123cba85cbccc6d673de64a80c40ad2024fc080f450c8459e8831ec24ad`;
- endpoint scores: `18d0f2b12209e22c08f34998d13d0574bfae9b8dccad512aff3506715eafe6a5`;
- inference: `27101607c73a62ec8a92c7004516c06140efb1ee4248891c318bae63d4cd969f`;
- normalized `summary.json`: `8d66542d4c6c07529ffcaed68e1ebb93c3b9a09734bff4ec9b268665949488aa`;
- pre-endpoint receipt: `3be8e09e1f6e5bcf6bb23c70067aa624f1ef666a0ed2fa436d08e2aeeff172e5`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the committed data and
frozen engine. The post-execution hardening commit only restores shared module
globals after wrapper calls; it does not change the numerical analysis. The
published result remains the single execution from `8d3a697`, while the
manifest now binds the corrected reproducibility implementation at `cc9aa4a`.
