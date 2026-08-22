# EXP-20260822-010 independent audit

## Decision

**GO to preserve the T0 reconstruction failure; NO-GO for every guide omission.**

The frozen gate correctly fails, the implementation stops in the required order,
and EXP-010 supports no guide-robustness claim. Do not modify or rescue this
experiment.

## Reproduced provenance and adequacy

- Preregistration is pinned at `996a866`; implementation files match cleanly to
  `d37e714`.
- Avana LFC: 3,173,505,617 bytes, MD5
  `58b1f479091a9f8b3e858d69d55413c4`.
- KY LFC: 1,585,769,082 bytes, MD5
  `c711c9413b63fe7c55b734e43cdeca91`.
- All seven frozen small-file SHA-256 receipts match.
- Eligible guide rule yields exactly four Avana and five KY WRN guides.
- Identity reconstruction yields 103 denominator records, 103 unique screens, 103
  valid joins, and 285 unique included sequences, with denominators 25/30 Large
  Intestine and 22/26 Ovary for Avana/KY.

## Reproduced gate failure

Under the literal frozen `ExcludeFromCRISPRCombined=False` and
`nIncludedSequences` rule, 100/103 scores match within `1e-8`. Exactly three fail:

| Model | Source | Screen | Passing / included | Absolute discrepancy |
|---|---|---|---:|---:|
| ACH-000680 | Avana | SC-000680.AV01 | 1 / 2 | 0.575461258572683 |
| ACH-000663 | Avana | SC-000663.AV01 | 2 / 3 | 0.0060110288685546465 |
| ACH-000719 | KY | SC-000719.KY01 | 2 / 3 | 0.0401273285009779 |

Each and only these three screens has included count above passing count and exactly
one retained `PassesQC=False` sequence. This is a mismatch pattern, not proof that a
passing-only reconstruction is correct.

## Stop verification

The code calls the baseline verifier before loading the gap file and before the
omission loop. On failure it writes `ERROR_INTEGRITY` and exits 1. No omission,
configuration, model-robustness, or guide-mean result artifacts exist. The
cache-disabled test suite has 51 passing tests.

## Required next boundary

A separately frozen child pipeline-semantics audit may identify and document the
official aggregation behavior. EXP-010 itself must remain stopped, and guide
omissions must not proceed unless a new preregistered reconstruction rule passes all
103 baseline comparisons.
