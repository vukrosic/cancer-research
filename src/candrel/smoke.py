from __future__ import annotations

import argparse
import json
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from scipy.stats import pearsonr, spearmanr

from .api import BASE_URL, CachedApi, sha256_file


PANEL = ("WRN", "BRAF", "KRAS", "NRAS", "EGFR", "PIK3CA", "CTNNB1", "MDM2")
SEED = 20260822


def lookup_gene(api: CachedApi, symbol: str) -> tuple[str, list[Path]]:
    payload, path = api.get(
        "/genes",
        {
            "filter": json.dumps([{"name": "symbol", "op": "eq", "val": symbol}]),
            "fields[gene]": "symbol,hgnc_id",
            "page[size]": "5",
        },
        f"gene_{symbol}",
    )
    records = payload.get("data", [])
    exact = [r for r in records if r["attributes"].get("symbol") == symbol]
    if len(exact) != 1:
        raise ValueError(f"Expected one exact record for {symbol}, found {len(exact)}")
    return exact[0]["id"], [path]


def fetch_scores(api: CachedApi, symbol: str, gene_id: str) -> tuple[list[dict[str, Any]], Path]:
    payload, path = api.get(
        f"/genes/{gene_id}/datasets/crispr_ko",
        {"page[size]": "2500"},
        f"crispr_full_v2_{symbol}_{gene_id}",
    )
    expected = int(payload.get("meta", {}).get("count", 0))
    records = payload.get("data", [])
    if expected != len(records):
        raise ValueError(f"Partial response for {symbol}: expected {expected}, got {len(records)}")
    return records, path


def paired_scores(records: list[dict[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    grouped: dict[tuple[str, str], list[float]] = {}
    for record in records:
        attrs = record.get("attributes", {})
        source = attrs.get("source")
        score = attrs.get("fc_clean_qn")
        model = record.get("relationships", {}).get("model", {}).get("data", {}).get("id")
        if source not in {"Broad", "Sanger"} or model is None or score is None:
            continue
        if attrs.get("qc_pass") is False:
            continue
        grouped.setdefault((model, source), []).append(float(score))

    by_model: dict[str, dict[str, float]] = {}
    for (model, source), values in grouped.items():
        by_model.setdefault(model, {})[source] = float(np.median(values))
    paired = [values for values in by_model.values() if set(values) == {"Broad", "Sanger"}]
    broad = np.asarray([values["Broad"] for values in paired], dtype=float)
    sanger = np.asarray([values["Sanger"] for values in paired], dtype=float)
    return broad, sanger


def bootstrap_spearman(x: np.ndarray, y: np.ndarray, seed: int, repeats: int = 1000) -> list[float]:
    rng = np.random.default_rng(seed)
    estimates: list[float] = []
    for _ in range(repeats):
        indices = rng.integers(0, len(x), len(x))
        estimate = float(spearmanr(x[indices], y[indices]).statistic)
        if np.isfinite(estimate):
            estimates.append(estimate)
    return estimates


def summarize(
    symbol: str, broad: np.ndarray, sanger: np.ndarray, seed: int, repeats: int = 1000
) -> dict[str, Any]:
    if len(broad) < 3:
        return {"symbol": symbol, "n_paired": int(len(broad)), "eligible": False}
    rho = float(spearmanr(broad, sanger).statistic)
    pearson = float(pearsonr(broad, sanger).statistic)
    boot = bootstrap_spearman(broad, sanger, seed, repeats)
    rng = np.random.default_rng(seed + 10_000)
    null = [float(spearmanr(broad, rng.permutation(sanger)).statistic) for _ in range(repeats)]
    empirical_p = (1 + sum(value >= rho for value in null)) / (len(null) + 1)
    broad_dependency = broad <= -0.5
    sanger_dependency = sanger <= -0.5
    contingency = {
        "both_dependency": int(np.sum(broad_dependency & sanger_dependency)),
        "broad_only": int(np.sum(broad_dependency & ~sanger_dependency)),
        "sanger_only": int(np.sum(~broad_dependency & sanger_dependency)),
        "neither_dependency": int(np.sum(~broad_dependency & ~sanger_dependency)),
    }
    return {
        "symbol": symbol,
        "n_paired": int(len(broad)),
        "eligible": len(broad) >= 100,
        "spearman_rho": rho,
        "spearman_bootstrap_95ci": [float(np.quantile(boot, 0.025)), float(np.quantile(boot, 0.975))],
        "pearson_r": pearson,
        "mae": float(np.mean(np.abs(broad - sanger))),
        "threshold_class_agreement_at_minus_0_5": float(np.mean(broad_dependency == sanger_dependency)),
        "threshold_contingency_counts": contingency,
        "permutation_p_one_sided": float(empirical_p),
    }


def evaluate_gates(genes: list[dict[str, Any]]) -> tuple[dict[str, Any], dict[str, bool]]:
    eligible = [item for item in genes if item.get("eligible")]
    median_rho = float(np.median([item["spearman_rho"] for item in eligible])) if eligible else None
    positive_fraction = float(np.mean([item["spearman_rho"] > 0 for item in eligible])) if eligible else None
    aggregate = {
        "eligible_genes": len(eligible),
        "median_spearman": median_rho,
        "positive_rho_fraction": positive_fraction,
    }
    gates = {
        "at_least_6_genes_with_100_pairs": len(eligible) >= 6,
        "median_spearman_at_least_0_30": median_rho is not None and median_rho >= 0.30,
        "positive_rho_fraction_at_least_0_75": positive_fraction is not None and positive_fraction >= 0.75,
    }
    return aggregate, gates


def run(root: Path, repeats: int = 1000) -> dict[str, Any]:
    cache = root / "data" / "raw" / "cell_model_passports"
    receipt_path = root / "experiments" / "EXP-20260822-001" / "input_receipt.json"
    receipt = json.loads(receipt_path.read_text()) if receipt_path.exists() else {"files": []}
    expected_hashes = {Path(item["path"]).name: item["sha256"] for item in receipt["files"]}
    api = CachedApi(cache, expected_hashes=expected_hashes)
    inputs: list[Path] = []
    genes: list[dict[str, Any]] = []
    for offset, symbol in enumerate(PANEL):
        gene_id, paths = lookup_gene(api, symbol)
        inputs.extend(paths)
        records, path = fetch_scores(api, symbol, gene_id)
        inputs.append(path)
        broad, sanger = paired_scores(records)
        summary = summarize(symbol, broad, sanger, SEED + offset, repeats)
        summary["gene_id"] = gene_id
        genes.append(summary)

    aggregate, gates = evaluate_gates(genes)
    return {
        "experiment_id": "EXP-20260822-001",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": {"name": "Cell Model Passports API", "base_url": BASE_URL, "api_version": "1.23.0"},
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "seed": SEED,
        "input_receipt_sha256": sha256_file(receipt_path) if receipt_path.exists() else None,
        "panel": list(PANEL),
        "score": "fc_clean_qn",
        "genes": genes,
        "aggregate": aggregate,
        "preregistered_gates": gates,
        "status": "PASS" if all(gates.values()) else "FAIL",
        "input_files": [{"path": str(path.relative_to(root)), "sha256": sha256_file(path)} for path in sorted(set(inputs))],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("experiments/EXP-20260822-001/results/rerun_latest.json"),
    )
    args = parser.parse_args()
    result = run(args.root.resolve())
    output = args.output if args.output.is_absolute() else args.root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["aggregate"], indent=2, sort_keys=True))
    print(f"status={result['status']} output={output}")
    raise SystemExit(0 if result["status"] == "PASS" else 2)


if __name__ == "__main__":
    main()
