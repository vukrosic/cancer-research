# EXP031 execution log

## Frozen boundary

- selection seal commit: `2d4be10`;
- implementation commit: `be2b241`;
- manifest binding commit: `d27e4a7`;
- endpoint target column: `BRD4 (23476)`;
- status column: `SMAD4 (4089)`;
- runner: `.venv/bin/python -m candrel.smad4_brd4_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `19` seconds and returned exit code
`2`, as required by the permanent feasibility-only contract. The pre-endpoint
receipt was written before BRD4 scores were parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

## Result receipts

- context ledger: `c1305ac91f5d1cd9064a3c00cb2980dac77b2fbf99990381ac34d25cf5d33b1e`;
- design sensitivity: `6a0d1e9605c928060aed9884d82b99b235351bdf5617df6abf8e85191b6311d1`;
- endpoint scores: `0832a49757dc75736b9f4a59bb85a88d702138e7cce233611c3936253edacac8`;
- inference: `2504a691f67580f51ad844fb99c462111d6717be97e96f4acc58a290f20a22f6`;
- normalized `summary.json`: `466ee51b8957657c69b98b0dd2fc8a6d8089ea602ddd217eceff55f23fa10daf`;
- pre-endpoint receipt: `4e6eace8f2ef6201a91354a8717d8d9ab8f5a2272176873acc12accf518c96c7`.

## Verification

The independent audit returned `GO` and recomputed the same summary digest and
source-specific statistics from the committed data and frozen engine.
