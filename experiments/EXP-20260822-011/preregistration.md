# EXP-20260822-011 preregistration

## Question

Does a single, post-failure passing-sequence aggregation rule exactly reconstruct
official DepMap 23Q4 WRN naïve scores in the frozen 103-screen subset?

EXP-011 is a **post-failure, single-candidate pipeline-semantics audit**. Its sole
candidate was motivated by EXP-010's three baseline mismatches. It is not blinded
confirmation, a second attempt inside EXP-010, or a guide-robustness experiment.

## Immutable parent boundary

EXP-010 remains immutable `FAIL_T0_RECONSTRUCTION`. Its preregistration, failure
receipt, result, and committed parent revision are hash-frozen in the EXP-011
manifest. No EXP-010 code, filter, artifact, status, or claim may change.

EXP-011 cannot authorize guide omissions. A passing result would justify only a
future, separately preregistered robustness experiment with a newly frozen baseline
rule.

## Frozen inputs and identities

- Same official DepMap Public 23Q4 version-2 Avana/KY pre-Chronos LFC matrices,
  exact byte sizes, MD5s, and SHA-256 receipts as audited in EXP-010.
- Same hash-frozen Avana/KY guide maps, sequence map, screen QC report, official
  naïve gene-score matrix, and 103-row EXP-003 denominator extract.
- Exactly 103 unique frozen `(ScreenID, ModelID, Library)` identities:
  Avana/KY 25/30 Large Intestine and 22/26 Ovary.
- Exactly four frozen Avana and five frozen KY eligible WRN guides under the EXP-010
  guide rule.

The execution code must have no EXP-005 gap-file argument, no gap loader, no ranking
or percentile function, and no guide-omission path.

## Exact joins and canonical fields

Join both `ScreenSequenceMap.csv` and `AchillesScreenQCReport.csv` to each frozen
record by exact `(ScreenID, ModelID, Library/source)`.

Reject any duplicate, missing, contradictory, or blank identity. Boolean sequence
fields must be exactly the canonical strings `True` or `False`; do not silently
coerce case variants or missing values. QC counts must be finite nonnegative integer
strings.

Do not filter on the screen-level QC report's `PassesQC` field. That file supplies
only the exact-row `nPassingSequences` and contextual `nIncludedSequences` counts.

## Sole frozen candidate rule

For each frozen screen, retain a sequence row if and only if all conditions hold:

1. exact `(ScreenID, ModelID, Library)` match;
2. sequence-level `PassesQC == True`; and
3. `ExcludeFromCRISPRCombined == False`.

Require the retained row count to equal that exact screen's integer
`nPassingSequences`. No alternate candidate, fallback, sequence repair, or filter
change is allowed if this rule fails.

Every retained `SequenceID` must be unique and map to one unique finite LFC matrix
column in its source. Every frozen eligible guide row and every retained guide by
sequence value must be present and finite.

## Frozen reconstruction and gate

For source `s`, guide `g`, and screen `j`, define:

`G_s,g,j = mean LFC across retained passing sequences`

`W_s,j = median G across the four Avana or five KY eligible WRN guides`.

Extract the official `WRN (7486)` value for every exact frozen ScreenID from
`ScreenNaiveGeneScore.csv`. Require:

- exactly 103 finite reconstructed/official pairs;
- unchanged 103 identities and denominator counts;
- `abs(W_reconstructed - W_official) <= 1e-8` for every screen with `rtol=0`.

EXP-011 passes only if all 103 comparisons pass. On any failure, stop with no second
candidate.

## Frozen ledger and parent comparison

Emit a 103-row ledger containing:

- ScreenID, ModelID, source, tissue;
- `nPassingSequences`;
- `nIncludedSequences` as context only;
- retained sequence count;
- reconstructed score;
- official score;
- absolute discrepancy; and
- gate pass/fail.

Compare only aggregate discrepancy identities against the immutable EXP-010 receipt:
prior mismatch count 3, new mismatch count, resolved mismatch count, persistent
mismatch count, and newly introduced mismatch count. Do not load WRN gaps or compute
any omission, rank, percentile, transition, or robustness statistic.

## Maximum claim

If all 103 pass: **This passing-sequence rule reconstructs WRN scores in the frozen
103-screen subset.**

This would not establish complete DepMap 23Q4 pipeline semantics, prove a rule for
other genes/screens/releases, retroactively repair EXP-010, authorize guide
omissions, establish a biological mechanism, or support therapeutic or clinical
claims.
