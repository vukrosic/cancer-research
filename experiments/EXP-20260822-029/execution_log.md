# EXP029 execution log

## Frozen boundary

- selection seal commit: `43bb802`;
- implementation commit: `9d58fbc`;
- manifest binding commit: `c508088`;
- endpoint target column: `POLQ (10721)`;
- composite status columns: `BRCA1 (672)`, `BRCA2 (675)`;
- runner: `.venv/bin/python -m candrel.brca12_polq_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The bound runner completed in approximately `19` seconds and returned exit
code `2`, as required by the permanent feasibility-only contract. The
pre-endpoint receipt was written before the POLQ column was parsed. It reports
`1,292` eligible screens, `1,290` source/model values, and
`sealed_before_endpoint: true`.

## Result receipts

- context ledger: `34c142633cd4f9070a062ab6a501da5e575e555e9aa19f078120d0756153cb70`;
- design sensitivity: `4727e363ec72681f7a63c6870f99d5e06bd24573c91efe2bbf178753d4a8d0ce`;
- endpoint scores: `5acafcf780f13029203cc7b14b865be6f7685254721f0622e9048899845081f1`;
- inference: `9209cb6bd7b25de299cde230ae0304690dd17d29cc97d473b6f17de93df5b61c`;
- normalized `summary.json`: `32dc58f9f25927cf0b3c31fdcba0acea23883f528ceeccebdb8b5f71b679108d`;
- pre-endpoint receipt: `19dfacfe10b64e9e9ef57b593f7b055876cb2d3e51ad3c35fba5bb3653e88927`.

## Verification

The full repository suite passed with `148` tests before execution. The
independent audit recomputed the same summary digest and source-specific
statistics from the committed data and frozen engine.
