# EXP028 execution log

## Frozen boundary

- selection seal commit: `9eb3860`;
- implementation commit: `be99f85`;
- initial manifest binding commit: `7f5ac73`;
- corrected pair-binding manifest commit: `e62c756`;
- endpoint target column: `TIPARP (25976)`;
- runner: `.venv/bin/python -m candrel.tp53_tiparp_replication`;
- endpoint values were not parsed before the sealed pre-endpoint receipt.

## Execution

The authoritative bound runner completed and returned exit code `2`, as
required by the permanent feasibility-only contract. The pre-endpoint receipt
was written before the TIPARP column was parsed. It reports `1,292` eligible
screens, `1,290` source/model values, and `sealed_before_endpoint: true`.

During orchestration, a duplicate status-poll invocation raced with the
authoritative run. The authoritative run published the complete result set;
the duplicate attempted the same atomic directory publish and wrote a stale
`ERROR_INTEGRITY` receipt. That stale receipt was removed after the published
five-file result set, hashes, summary digest, and independent recomputation
were verified. No input, endpoint, or published result artifact was modified.

## Result receipts

- context ledger: `1e0c419228a07a06c56b141a1e4eb44a911ef624d3f476fb97705d9352c6967f`;
- design sensitivity: `b24e122734ed5d68787fed9cd2e49a30afa9a6d0e68fb4b1648a33270fa51637`;
- endpoint scores: `0fe6f5be0e9f4fd79d852038a7ecb36ed4adf188b1c698075162f2b0bf491810`;
- inference: `c2ad9f57fcf78d3c89ee7c56c1e7ab456de40b4de532b798f4fb9dcd9bfaaf87`;
- normalized `summary.json`: `4618dfde63fbc00553835965f3c051f70e12b981467d863033a45287d0fd1fd4`;
- pre-endpoint receipt: `c1d108260fe014335f20ff3e195aa7fa41366ad02950fb26b62a7542c2f745a3`.

## Verification

The full repository suite passed with `144` tests. The independent audit
recomputed the same summary digest and source-specific statistics from the
committed data and frozen engine.
