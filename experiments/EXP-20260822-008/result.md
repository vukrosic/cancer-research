# EXP-20260822-008 result

## Status

**FAIL — model-general control-gene rank discordance did not positively track the
frozen WRN percentile gaps.**

Evidence label: preregistered derived observational analysis after EXP-005 endpoint
unsealing. This is not blinded confirmation or a causal mechanism test.

## Exact execution

The protocol was pushed at `f49eec8`, and the missing explicit outcome receipt was
added and pushed at `208a803`, before any control exposure or association was
computed.

```bash
uv sync --extra dev --locked
uv run pytest
uv run candrel-control-discordance --smoke \
  --output experiments/EXP-20260822-008/results/smoke_summary.json \
  --model-output experiments/EXP-20260822-008/results/smoke_model_exposures.csv \
  --gene-output experiments/EXP-20260822-008/results/smoke_gene_eligibility.csv
uv run candrel-control-discordance
```

Forty tests pass in the final suite, including a regression proving that failed
exposure adequacy prevents even hashing or loading the WRN-gap outcome. Both smoke
and full runs returned expected scientific-failure exit code 2.

## Outcome-sequential adequacy

All pre-outcome hashes, cohort identities, screen identities, and denominator counts
matched. Control eligibility was frozen across all 103 source screens:

| Panel | Official list | In score header | Finite in all 103 | Frozen minimum |
|---|---:|---:|---:|---:|
| Common essential (primary) | 1,247 | 1,244 | **1,227** | 996 |
| Nonessential (corroborative) | 781 | 730 | **618** | 584 |

For common essentials, 3 controls were absent from the score header and 17 otherwise
present controls had at least one nonfinite denominator value. For nonessentials,
the corresponding counts were 51 and 112. WRN was absent from both panels.

The full-denominator source×tissue ranks produced adequate model-level exposures:

| Panel | Large Intestine distinct / n | Ovary distinct / n |
|---|---:|---:|
| Common essential | 16 / 17 | 16 / 17 |
| Nonessential | 17 / 17 | 17 / 17 |

Only after these gates passed did the code verify and load the frozen WRN-gap
outcome.

## Primary common-essential result

| Estimand | Result | Frozen gate | Pass? |
|---|---:|---:|:---:|
| Equal-tissue mean Spearman `theta` | **0.1147** | >= 0.40 | No |
| One-sided tissue-preserving permutation p | **0.2614** | <= 0.05 | No |
| Fixed-rank paired-bootstrap 95% CI | **[-0.2422, 0.4396]** | lower > 0.10 | No |
| Lowest tissue rho | **0.0478** | >= -0.20 | Yes |

Tissue estimates were weakly positive but small: Large Intestine rho 0.0478 and
Ovary rho 0.1815. Three of four primary gates failed.

## Corroborative nonessential result

The separately frozen corroborative panel also failed:

| Estimand | Result | Same frozen gate | Pass? |
|---|---:|---:|:---:|
| Equal-tissue mean Spearman `theta` | **-0.1078** | >= 0.40 | No |
| One-sided tissue-preserving permutation p | **0.7272** | <= 0.05 | No |
| Fixed-rank paired-bootstrap 95% CI | **[-0.4717, 0.2683]** | lower > 0.10 | No |
| Lowest tissue rho | **-0.1544** | >= -0.20 | Yes |

Large Intestine rho was -0.0613 and Ovary rho was -0.1544. The nonessential panel
cannot rescue the failed primary panel under the frozen hierarchy.

## Interpretation

The simple model-general explanation is not supported: models with larger WRN
source gaps were not consistently the same models with greater median cross-source
rank disagreement across 1,227 common-essential controls or 618 nonessential
controls. The common-essential estimate is imprecise but far below the frozen point
target; the corroborative estimate points slightly negative.

Together with EXP-006, this narrows the technical search. The observed WRN ranking
gaps are not captured by either broad screen-QC asymmetry or broad control-gene
discordance summaries in this cohort. This does not prove that the gaps are
WRN-specific biology; gene-specific guide behavior, assay kinetics, cell state,
source-specific model drift, and measurement noise remain possible.

## Claim boundary

Maximum supported claim: in the frozen 23Q4 Large Intestine and Ovary overlap,
neither the primary common-essential nor the corroborative nonessential model-level
cross-source discordance summary positively tracked WRN rank gaps under the frozen
gates.

This does not establish causality, source superiority, absence of technical effects,
a WRN mechanism, therapeutic actionability, patient benefit, or clinical relevance.

## Artifacts

- `results/summary.json`: SHA-256
  `7326ed2a0604052e990c01b22579aaa173d22048f3874819c99de2895ba69237`.
- `results/model_exposures.csv`: SHA-256
  `fc8050dcd7b414c16b92e5c4c742c210a0ad0339bd6ef483e54a26b83cd86c7e`.
- `results/gene_eligibility.csv`: SHA-256
  `c41a3a86bdb9371874719977186ea300daa522c16ae1ecde421b183e05a07369`.
- `results/smoke_summary.json`: SHA-256
  `9a3c4a2de65b90d7227c63dcaa7a1539eb104573d27e01e2ecba6afa6cdf306d`.
- Smoke and full model/gene tables are byte-identical because smoke changes only
  inferential repeat counts.

Independent audit verified all six input receipts, 103 screen identities, denominator
counts, control eligibility, model exposures, exact outcome join, both panel
correlations, inference implementations, gate hierarchy, outcome sequencing, all
artifact hashes, and 40 tests. It returned GO for commit and push.
