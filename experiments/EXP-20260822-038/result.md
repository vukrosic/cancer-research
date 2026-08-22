# EXP-20260822-038 result — PTEN proxy status to ICMT dependency

## Terminal claim

**FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE**

This is a **T1 descriptive association only; not T2/confirmatory** result.
`confirmatory_claim` is `false` and `overall_pass` is `false` by the frozen
design contract. Avana and KY remain separate screen families.

## Frozen cohort and endpoint

- eligible screens: `1,292`;
- source/model units: Avana `975`, KY `315`;
- endpoint: `ICMT (23463)` from the frozen DepMap 23Q4 naive CRISPR screen;
- exposure: PTEN damaging-matrix proxy when the matrix value is `1` or `2`;
- reference: PTEN matrix value `0`;
- status counts: Avana `94/881`, KY `38/277` damaging/matrix-intact;
- mixed-lineage counts: Avana `19`, KY `11`;
- canonical roster SHA-256:
  `73222b7a148f333399d580107e1ab64672b0920678f3a2a9789b3440f9c2d953`;
- endpoint SHA-256:
  `e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721`.

The outcome-free planning powers were Avana `0.8579` and KY `0.5297`; the
paired-source contract therefore permanently limits this experiment to
`FEASIBILITY_ONLY`.

The biological motivation is a recent primary study reporting an ICMT
dependency in PTEN-deficient triple-negative breast cancer
([primary PTEN/ICMT study](https://link.springer.com/article/10.1186/s40164-025-00738-0)).
This experiment uses only a damaging PTEN mutation-matrix proxy. It is not
equivalent to PTEN protein loss, PTEN copy loss, PTEN-deficient triple-negative
breast cancer, or ICMT pharmacologic inhibition.

## Source-specific results

| Source | Delta | Pairs | One-sided permutation p | Bootstrap 95% CI | Negative lineages | Max lineage delta | Gate result |
|---|---:|---:|---:|---|---:|---:|---|
| Avana | `+0.1024171443` | 4013 | `0.9149808502` | `[-0.0346374284, +0.2329927735]` | 6 | `+1.0000` | FAIL |
| KY | `-0.0330250991` | 757 | `0.3962160378` | `[-0.2179656539, +0.1545574637]` | 6 | `+1.0000` | FAIL |

Avana is positive in the preregistered dependency direction and fails the
effect, permutation, bootstrap, and no-positive-lineage gates. KY is weakly
negative and passes only the direction gate; it fails the effect, permutation,
bootstrap, and no-positive-lineage gates. No source pooling, post hoc lineage
exclusion, threshold change, or proxy rescue was used.

## Interpretation boundary

The strongest allowed statement is: in these frozen DepMap 23Q4 cohorts, the
PTEN damaging-matrix proxy did not show a robust source-consistent association
with ICMT genetic dependency. The result does not replicate the referenced
PTEN/ICMT hypothesis under this proxy and endpoint contract.

This does not refute PTEN/ICMT biology. The mutation proxy, PTEN protein or
copy-number loss, breast-cancer subtype, ICMT genetic knockout, and ICMT drug
inhibition are not equivalent. The result does not establish mechanism,
pharmacologic response, treatment benefit, patient selection, clinical utility,
or a confirmatory claim.

## Artifact receipts

- `context_ledger.csv`: `48bf8b95574dc6b79acdb31acbb08cbc9166ffd4c04de600142df9c03baaa11b`
- `design_sensitivity.csv`: `5a97a287c00c662c5a4297154d0d66640fbcbc19a6cb42b1659e9d31178dba1e`
- `endpoint_scores.csv`: `a6f3cc20f9608296b18d6fd8e244f3615e94bdc9e1f61640639c5d2e32f4bd6f`
- `inference.csv`: `5d94acd69c367ab5ab6dda90439670fa85a5dc86c236a6c2e69baa72fbd31365`
- normalized `summary.json` digest: `758cbd2c271d1f5e63efe3ec4b138866350ca36c48bf7c972421a1333180ef42`
- `pre_endpoint_receipt.json`: `9193e3e0fddd2409455bcc6ffcb7881e5ecd1a0a8a6b64f9ef1a22473e7f90d2`
