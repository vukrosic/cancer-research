# EXP-20260822-011 result

## Status

**PASS — the sole passing-sequence candidate reconstructed all 103 frozen official
WRN screen scores within the preregistered absolute tolerance.**

Evidence label: post-failure, single-candidate pipeline-semantics audit. The candidate
was selected after observing EXP-010's three baseline mismatches, so this is not
outcome-independent confirmation or a biological result.

## Exact execution order

The protocol was pushed as `dd3e920` and the tested implementation as `3f6c73f`
before execution.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-wrn-sequence-semantics
```

All 55 tests passed. The command completed successfully with status
`PASS_PASSING_SEQUENCE_RECONSTRUCTION`.

## Frozen candidate and result

For each exact frozen `(ScreenID, ModelID, Library)` identity, the implementation:

1. retained sequence rows only when sequence-level `PassesQC=True` and
   `ExcludeFromCRISPRCombined=False`;
2. required the retained count to equal that screen's `nPassingSequences`;
3. averaged LFC values across retained sequences for each frozen eligible guide;
4. took the median across four Avana or five KY WRN guides; and
5. compared the result with the official naïve WRN score using absolute tolerance
   `1e-8` and relative tolerance zero.

All 103 comparisons passed. The maximum absolute discrepancy was
`5.551115123125783e-17`. The ledger contains 103 unique screens, 282 retained
passing sequences, and the expected 47 Avana plus 56 KY source screens.

## Parent comparison

All three EXP-010 mismatch identities were resolved:

- `ACH-000663|Avana`
- `ACH-000680|Avana`
- `ACH-000719|KY`

There were zero persistent and zero newly introduced mismatches. EXP-010 remains an
immutable `FAIL_T0_RECONSTRUCTION`; this child result does not retroactively repair
or alter it.

## Forbidden-analysis receipt

The execution loaded no WRN gap file and computed no ranks, percentiles, guide
omissions, or robustness statistics. There was no fallback candidate. Consequently,
EXP-011 makes no claim about whether the large cross-source WRN gaps survive
single-guide omissions.

## Interpretation and maximum claim

**This passing-sequence rule reconstructs WRN scores in the frozen 103-screen
subset.**

The result does not establish complete DepMap 23Q4 pipeline semantics, generalize to
other genes, screens, or releases, establish a biological mechanism, or support a
therapeutic or clinical claim.

## Artifacts and receipts

- `results/summary.json`: SHA-256
  `f1df2711856ea08ba166c18436ea96c799c6494c5cf069f5cb71c1f6a0ed5b9a`.
- `results/reconstruction_ledger.csv`: SHA-256
  `29eb728f0b05e1ff4838f1a4012a5bf76f577bee92986380c0f9c9d9f7b73354`.
- Avana LFC: 3,173,505,617 bytes, MD5
  `58b1f479091a9f8b3e858d69d55413c4`, SHA-256
  `f018d7ff6820af6d0bb095f1e2b405ec31d7a744a1e4c019cfd9f3509e63bdee`.
- KY LFC: 1,585,769,082 bytes, MD5
  `c711c9413b63fe7c55b734e43cdeca91`, SHA-256
  `5b03df4b4affda1f0ed36f2bd564e1cbd53ec443b20e60295cad577677874767`.

Independent audit reproduced the receipts, identities, counts, implementation rule,
103/103 gate, maximum discrepancy, and test suite, and returned GO with no material
defect.
