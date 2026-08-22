# EXP-20260822-013 result

## Decision

**Primary association failed.** The preregistered efficacy-rank discordance did
not meet the positive-association gates in the frozen two-tissue cohort.

This is an assay-process reliability result, not a biological cancer discovery.

## Question and protocol status

The experiment asked whether source-relative Chronos-inferred model-efficacy
discordance was positively associated with the frozen EXP-005 WRN percentile gap
between Avana and KY.

The source-specific coverage contract was amended before execution in commit
`07976d9`: all 103 source-specific denominator records had to map to their own
finite source value, while both source values were required for each of the 34
paired models. Opposite-source blanks for the 35 unpaired records were expected
and unused. The runner fix making adequacy one observation per paired ModelID was
committed in `51a2874` before the final run.

Outcome access occurred only after the complete 103-row parameter ledger and
both tissue-level adequacy gates were written. The final run used:

- `uv run candrel-wrn-process-association`;
- code commit `51a2874`;
- seed `20260830`, 100,000 within-tissue permutations, and 10,000 paired
  ModelID bootstraps;
- 17 paired models per tissue, 34 total;
- efficacy and growth values ranked within the complete source×tissue
  denominators; raw source units were never compared.

The four hash-locked inputs matched their preregistered receipts, including the
EXP-005 outcome hash loaded after adequacy:

| Input | SHA-256 |
|---|---|
| efficacy | `a64065456d8d1e83d2fac94fc7e3ae28e65272cd2a45c3fa969848555f0b7aa0` |
| growth rate | `4f2f4a9f80af1e9862319156f9a8de38d677797074823bebec7853060550f29c` |
| denominator | `072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654` |
| EXP-005 WRN gap outcome | `f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a` |

## Primary result

| Gate | Observed | Frozen criterion | Result |
|---|---:|---:|---|
| Equal-tissue efficacy theta | 0.2071078431 | ≥ 0.40 | Fail |
| One-sided permutation p | 0.1220187798 | ≤ 0.05 | Fail |
| Bootstrap 95% interval | [-0.1697118656, 0.5334215543] | lower > 0.10 | Fail |
| Minimum tissue rho | -0.0637254902 | ≥ -0.20 | Pass |

Tissue-specific efficacy Spearman correlations were `-0.0637254902` for Large
Intestine and `0.4779411765` for Ovary. The plus-one permutation receipt implies
12,201 extreme permutations and p = `12,202 / 100,001`.

Outcome-blind adequacy passed in both tissues for both tracked parameters:
17 paired observations, 17 distinct exposure values, and largest tied level 1.

## Descriptive growth companion

Growth-rate discordance was descriptive only. Its equal-tissue theta was
`0.1139705882`, with tissue correlations `0.0318627451` (Large Intestine) and
`0.1960784314` (Ovary). No growth p-value or confidence interval was computed,
and growth cannot rescue, reinterpret, or combine with the failed efficacy
result.

## Claim boundary

The frozen data do not support the preregistered positive association claim.
This does not show that no assay-process association exists elsewhere. It is
limited to this two-tissue cell-model set, the hash-locked parameter files, and
the already-unsealed EXP-005 WRN endpoint. The analysis cannot establish
causality, source superiority, a WRN mechanism, a new dependency, therapeutic
relevance, patient benefit, or clinical utility.

## Tracked artifacts

| Artifact | SHA-256 |
|---|---|
| `parameter_ledger.csv` | `384c906eb35d2c4a52411e5db1ac2919e67918f87b7a8113ee966b4cdfd1d470` |
| `paired_exposure_outcome.csv` | `49a2b9b2271ebc9f1042743928bfa45e44c6e9978c6d24e06dd5f67971c00d49` |
| `inference.csv` | `1bb0297c5f27627ccf5397dcece2abbbece493ac62208bda271df846a1e4c984` |
| `summary.json` raw file | `ede9c3f7e8c3c3e6a095a8cae29639cf659f1447263480694d79da96d71f9f9c` |
| `summary.json` normalized self-digest | `4d1a513ddad967cdb71dfe4b4d514d8d5e8165e1d608f2a9965b3ad48e621f5c` |

The machine-readable receipt is
[`summary.json`](results/summary.json). The complete protocol is in
[`preregistration.md`](preregistration.md), and the independent audit is in
[`audit.md`](audit.md).
