# EXP039 execution log

## Frozen boundary and correction chain

- selection checkpoint: `037c6d5`;
- initial implementation commit: `3667d50`;
- initial manifest binding: `66a4ba6`;
- attempt 001: T0 screen-map hash stop, `endpoint_opened: false`;
- correction receipt and implementation remediation: `15dd90b`;
- corrected manifest rebind: `2e8a354`;
- post-execution metadata hardening: `24dda7e`;
- final manifest binding: `24dda7e`;
- endpoint target column: `PARP1 (142)`;
- composite status columns: `PBRM1 (55193)`, `ARID2 (196528)`.

## Execution

Attempt 001 returned exit code `2` at the T0 input-hash gate and parsed no
endpoint value. The corrected bound runner then executed exactly once,
completed in approximately `20.0` seconds, and returned exit code `2` as
required by the permanent feasibility-only contract. The pre-endpoint receipt
was written before PARP1 scores were parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

No endpoint rerun was performed during the metadata hardening or independent
audit.

## Result receipts

- context ledger: `4beaa3d4d6b4ede1b27e8dc3ebffb0dd87a454e235513384b182c3ef50e704be`;
- design sensitivity: `cfc878555f978e8fd68e0e7ed9552ff2929121626f6fa656bf6b2be8241b2da3`;
- endpoint scores: `b7c5ef73e3399f8dec2c85f9db126f50fd2cf897cbe6bffa6731881bba907227`;
- inference: `fda19f054f7ed7e6f0feedcf9592e88a779f1ecea4bb8bf7231227342fec49b4`;
- normalized `summary.json`: `4e3b15cdac892e147725eff444b95e1ae9c97bd54c3a42a1a01d79a07d05e992`;
- pre-endpoint receipt: `da8966d3c0901d71413cced694df9044e63674ecc7402d0e4557eb40fe08bb72`;
- preserved attempt-001 receipt: `attempt_001_t0_error_receipt.json`.

## Verification

The independent direct-engine audit returned `GO` and recomputed the same
summary digest and source-specific statistics from the result ledgers and
frozen engine. The heartbeat remains deleted by user request.
