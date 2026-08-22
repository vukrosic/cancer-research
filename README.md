# Cancer Dependency Reliability Lab

An open, falsification-first computational cancer-research program.

## North star

Identify genetic-vulnerability hypotheses that remain stable across independently
generated cancer CRISPR screens, survive artifact checks, and are documented well
enough for another researcher or AI agent to reproduce or refute.

The project nominates hypotheses for experimental validation. It does **not**
establish treatments, therapeutic windows, patient benefit, or clinical utility.

## Why this question

Broad and Sanger have independently screened many of the same cancer cell models.
Overall agreement is established, but rare lineage- or biomarker-defined effects can
still be unstable. The unresolved target is claim-level reliability: which specific
context-dependent vulnerabilities survive a held-out screen family with honest
uncertainty and artifact controls?

## Current phase

`EXP-20260822-001` is an engineering and positive-control gate. It tests whether the
official Cell Model Passports API provides sufficient paired Broad/Sanger records and
enough cross-source variation for the planned reliability analyses. It does not test
a molecular context and is not a novelty claim.

```bash
uv sync
uv run pytest
uv run candrel-smoke  # writes rerun_latest.json and stops if the API inputs drift
```

Raw API responses are cached under `data/raw/` and excluded from Git. Every run
writes hashes and a machine-readable result under its experiment directory.

## Repository map

- `AGENTS.md` — mandatory operating rules for human and AI contributors.
- `docs/` — research charter, question selection, prior art, datasets, claim policy.
- `protocols/` — preregistration and experiment lifecycle.
- `experiments/` — immutable experiment records and tracked results.
- `state/` — compact continuation state for fresh agents.
- `logs/` — append-only decision and orchestration logs.
- `src/` and `tests/` — reproducible acquisition and analysis code.

## Scientific contract

1. Freeze hypotheses and thresholds before inspecting test results.
2. Keep discovery and independent screen-family evaluation separate.
3. Preserve negative and failed runs.
4. Record exact source versions, URLs, hashes, code commit, and environment.
5. Label claims by evidence tier and never imply clinical actionability from cell lines.
6. Treat “not found in our search” as uncertainty, not proof of novelty.

See [docs/RESEARCH_CHARTER.md](docs/RESEARCH_CHARTER.md) for the full contract.
