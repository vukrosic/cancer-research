from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import spearmanr

from .api import BASE_URL, CachedApi, sha256_file
from .smoke import PANEL, fetch_scores, lookup_gene


SEED = 20260823
PRIMARY_FIELDS = ("fc_clean_qn", "bf_scaled")


def paired_by_model(records: list[dict[str, Any]], field: str) -> dict[str, tuple[float, float]]:
    grouped: dict[tuple[str, str], list[float]] = {}
    for record in records:
        attrs = record.get("attributes", {})
        source = attrs.get("source")
        model = record.get("relationships", {}).get("model", {}).get("data", {}).get("id")
        value = attrs.get(field)
        if source not in {"Broad", "Sanger"} or model is None or value is None:
            continue
        if attrs.get("qc_pass") is False:
            continue
        grouped.setdefault((model, source), []).append(float(value))

    by_model: dict[str, dict[str, float]] = {}
    for (model, source), values in grouped.items():
        by_model.setdefault(model, {})[source] = float(np.median(values))
    return {
        model: (values["Broad"], values["Sanger"])
        for model, values in by_model.items()
        if set(values) == {"Broad", "Sanger"}
    }


def rho(values: dict[str, tuple[float, float]], models: list[str]) -> float:
    broad = np.asarray([values[model][0] for model in models], dtype=float)
    sanger = np.asarray([values[model][1] for model in models], dtype=float)
    return float(spearmanr(broad, sanger).statistic)


def bootstrap_delta(
    harmonized: dict[str, tuple[float, float]],
    scaled_bf: dict[str, tuple[float, float]],
    models: list[str],
    seed: int,
    repeats: int,
) -> list[float]:
    rng = np.random.default_rng(seed)
    deltas: list[float] = []
    n = len(models)
    for _ in range(repeats):
        sampled = [models[i] for i in rng.integers(0, n, n)]
        h = rho(harmonized, sampled)
        b = rho(scaled_bf, sampled)
        if np.isfinite(h) and np.isfinite(b):
            deltas.append(h - b)
    return deltas


def summarize_gene(
    symbol: str, records: list[dict[str, Any]], seed: int, repeats: int
) -> dict[str, Any]:
    values = {field: paired_by_model(records, field) for field in (*PRIMARY_FIELDS, "bf")}
    models = sorted(set(values[PRIMARY_FIELDS[0]]) & set(values[PRIMARY_FIELDS[1]]))
    identical_primary_cohort = all(set(values[field]) == set(models) for field in PRIMARY_FIELDS)
    if len(models) < 3:
        return {
            "symbol": symbol,
            "n_identical_paired_models": len(models),
            "identical_primary_cohort": identical_primary_cohort,
            "eligible": False,
        }
    harmonized_rho = rho(values["fc_clean_qn"], models)
    scaled_bf_rho = rho(values["bf_scaled"], models)
    delta = harmonized_rho - scaled_bf_rho
    boot = bootstrap_delta(
        values["fc_clean_qn"], values["bf_scaled"], models, seed, repeats
    )
    bf_models = sorted(set(models) & set(values["bf"]))
    return {
        "symbol": symbol,
        "n_identical_paired_models": len(models),
        "identical_primary_cohort": identical_primary_cohort,
        "eligible": len(models) >= 100 and identical_primary_cohort,
        "spearman_fc_clean_qn": harmonized_rho,
        "spearman_bf_scaled": scaled_bf_rho,
        "delta_rho_fc_clean_qn_minus_bf_scaled": delta,
        "delta_bootstrap_95ci": [
            float(np.quantile(boot, 0.025)),
            float(np.quantile(boot, 0.975)),
        ],
        "descriptive_spearman_bf": rho(values["bf"], bf_models),
        "n_descriptive_bf_pairs": len(bf_models),
    }


def evaluate(genes: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, bool]]:
    eligible = [gene for gene in genes if gene.get("eligible")]
    deltas = [gene["delta_rho_fc_clean_qn_minus_bf_scaled"] for gene in eligible]
    median_delta = float(np.median(deltas)) if deltas else None
    positive_count = sum(delta > 0 for delta in deltas)
    aggregate = {
        "eligible_genes": len(eligible),
        "median_delta_rho": median_delta,
        "genes_with_positive_delta": positive_count,
        "positive_delta_fraction": positive_count / len(eligible) if eligible else None,
    }
    gates = {
        "all_8_genes_have_identical_100_model_cohorts": len(eligible) == 8,
        "median_delta_rho_at_least_0_10": median_delta is not None and median_delta >= 0.10,
        "at_least_6_genes_have_positive_delta": positive_count >= 6,
    }
    return aggregate, gates


def run(root: Path, repeats: int = 2000) -> dict[str, Any]:
    receipt_path = root / "experiments" / "EXP-20260822-001" / "input_receipt.json"
    receipt = json.loads(receipt_path.read_text())
    expected_hashes = {Path(item["path"]).name: item["sha256"] for item in receipt["files"]}
    api = CachedApi(root / "data" / "raw" / "cell_model_passports", expected_hashes=expected_hashes)
    inputs: list[Path] = []
    genes: list[dict[str, Any]] = []
    for offset, symbol in enumerate(PANEL):
        gene_id, paths = lookup_gene(api, symbol)
        records, path = fetch_scores(api, symbol, gene_id)
        inputs.extend(paths + [path])
        summary = summarize_gene(symbol, records, SEED + offset, repeats)
        summary["gene_id"] = gene_id
        genes.append(summary)
    aggregate, gates = evaluate(genes)
    return {
        "experiment_id": "EXP-20260822-002",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"name": "Cell Model Passports API", "base_url": BASE_URL, "api_version": "1.23.0"},
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "seed": SEED,
        "bootstrap_repeats": repeats,
        "input_receipt_sha256": sha256_file(receipt_path),
        "panel": list(PANEL),
        "primary_fields": list(PRIMARY_FIELDS),
        "genes": genes,
        "aggregate": aggregate,
        "preregistered_gates": gates,
        "status": "PASS" if all(gates.values()) else "FAIL",
        "input_files": [
            {"path": str(path.relative_to(root)), "sha256": sha256_file(path)}
            for path in sorted(set(inputs))
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--repeats", type=int, default=2000)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/EXP-20260822-002/results/summary.json"),
    )
    args = parser.parse_args()
    root = args.root.resolve()
    result = run(root, repeats=args.repeats)
    output = args.output if args.output.is_absolute() else root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["aggregate"], indent=2, sort_keys=True))
    print(f"status={result['status']} output={output}")
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()
