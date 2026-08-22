from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

import numpy as np
from scipy.stats import rankdata

from candrel.wrn_qc_asymmetry import (
    bootstrap_interval,
    estimate_from_arrays,
    permutation_pvalue,
)


EXPERIMENT_ID = "EXP-20260822-008"
TISSUES = ("Large Intestine", "Ovary")
SOURCES = ("Avana", "KY")
PANELS = ("common_essential", "nonessential")
EXPECTED_HASHES = {
    "cohort_file": "2bc84868962b35c55e456aeb953429206e97c9b25f648b5deabe5a1488e60b67",
    "denominator_file": "072dd2775d4e3bfaa480cd70639cc799c1e5914b2e9cc5213328383557680654",
    "score_file": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "essential_file": "496c5ec9eaa2f4c13dc00fd15a8e24df253afcc5a969d3956b7dd3d987640084",
    "nonessential_file": "2aacca44b6a79e7240518e6adbd89c70d7d895da91cd4c8b4d380529bc5b8e5e",
}
EXPECTED_OUTCOME_HASH = (
    "f2dc22d9c26f937413b612ae4924f1965c837e480a805c1ff0b7b0c5d8b3cd4a"
)
EXPECTED_DENOMINATORS = {
    ("Avana", "Large Intestine"): 25,
    ("KY", "Large Intestine"): 30,
    ("Avana", "Ovary"): 22,
    ("KY", "Ovary"): 26,
}
EXPECTED_HEADER_PRESENT = {"common_essential": 1244, "nonessential": 730}
MINIMUM_ELIGIBLE = {"common_essential": 996, "nonessential": 584}


class IntegrityError(RuntimeError):
    """Raised when frozen identities, provenance, or analysis invariants drift."""


@dataclass(frozen=True)
class DenominatorRecord:
    model_id: str
    tissue: str
    source: str
    screen_id: str


@dataclass(frozen=True)
class GeneEligibility:
    panel: str
    gene: str
    header_count: int
    finite_all_103: bool
    eligible: bool
    exclusion_reason: str


@dataclass(frozen=True)
class ExposureRecord:
    model_id: str
    tissue: str
    common_essential_exposure: float
    nonessential_exposure: float


@dataclass(frozen=True)
class AnalysisRecord:
    model_id: str
    tissue: str
    common_essential_exposure: float
    nonessential_exposure: float
    wrn_percentile_gap: float
    exp005_gap_flag: bool


def sha256(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_pre_outcome_hashes(args: argparse.Namespace) -> dict[str, str]:
    receipt = {}
    for argument, expected in EXPECTED_HASHES.items():
        actual = sha256(Path(getattr(args, argument)))
        if actual != expected:
            raise IntegrityError(
                f"{argument} SHA-256 drift: expected {expected}, got {actual}"
            )
        receipt[f"{argument}_sha256"] = actual
    return receipt


def load_cohort(path: Path) -> dict[str, str]:
    cohort: dict[str, str] = {}
    counts: Counter[str] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != ["model_id", "tissue"]:
            raise IntegrityError("cohort must contain only model_id,tissue")
        for row in reader:
            model_id = row["model_id"].strip()
            tissue = row["tissue"].strip()
            if model_id in cohort or tissue not in TISSUES:
                raise IntegrityError(f"invalid cohort row: {model_id} {tissue}")
            cohort[model_id] = tissue
            counts[tissue] += 1
    expected = {tissue: 17 for tissue in TISSUES}
    if len(cohort) != 34 or dict(counts) != expected:
        raise IntegrityError(f"cohort drift: expected {expected}, got {dict(counts)}")
    return cohort


def load_denominators(path: Path) -> list[DenominatorRecord]:
    records = []
    seen: set[tuple[str, str]] = set()
    screens: set[str] = set()
    counts: Counter[tuple[str, str]] = Counter()
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            tissue = row["tissue"].strip()
            source = row["library"].strip()
            if tissue not in TISSUES or source not in SOURCES:
                continue
            model_id = row["model_id"].strip()
            key = (model_id, source)
            if key in seen:
                raise IntegrityError(f"duplicate denominator model-source: {key}")
            screen_parts = [part for part in row["screen_ids"].split(";") if part]
            if len(screen_parts) != 1:
                raise IntegrityError(f"expected one frozen screen for {key}")
            screen_id = screen_parts[0]
            if screen_id in screens:
                raise IntegrityError(f"shared denominator ScreenID: {screen_id}")
            seen.add(key)
            screens.add(screen_id)
            counts[(source, tissue)] += 1
            records.append(DenominatorRecord(model_id, tissue, source, screen_id))
    if dict(counts) != EXPECTED_DENOMINATORS or len(records) != 103:
        raise IntegrityError(
            f"denominator drift: expected {EXPECTED_DENOMINATORS}, got {dict(counts)}"
        )
    return sorted(records, key=lambda row: (row.source, row.tissue, row.model_id))


def load_control_list(path: Path) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        genes = [row["Gene"].strip() for row in csv.DictReader(handle)]
    if len(genes) != len(set(genes)):
        raise IntegrityError(f"duplicate genes in control list: {path}")
    if "WRN (7486)" in genes:
        raise IntegrityError(f"WRN present in control list: {path}")
    return genes


def load_control_scores(
    path: Path,
    denominators: Sequence[DenominatorRecord],
    panels: dict[str, list[str]],
) -> tuple[np.ndarray, list[str], list[GeneEligibility]]:
    required_screens = {row.screen_id for row in denominators}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            header = next(reader)
        except StopIteration as exc:
            raise IntegrityError("empty gene-score matrix") from exc
        header_counts = Counter(header[1:])
        present_by_panel = {
            panel: sum(header_counts[gene] == 1 for gene in genes)
            for panel, genes in panels.items()
        }
        if present_by_panel != EXPECTED_HEADER_PRESENT:
            raise IntegrityError(
                f"control header drift: expected {EXPECTED_HEADER_PRESENT}, "
                f"got {present_by_panel}"
            )
        selected_genes = sorted(
            {
                gene
                for genes in panels.values()
                for gene in genes
                if header_counts[gene] == 1
            }
        )
        indices = [header.index(gene) for gene in selected_genes]
        screen_values: dict[str, np.ndarray] = {}
        for row in reader:
            if not row:
                continue
            screen_id = row[0].strip()
            if screen_id not in required_screens:
                continue
            if screen_id in screen_values:
                raise IntegrityError(f"duplicate score-matrix ScreenID: {screen_id}")
            values = np.full(len(indices), np.nan)
            for output_index, source_index in enumerate(indices):
                if source_index >= len(row) or not row[source_index].strip():
                    continue
                try:
                    value = float(row[source_index])
                except ValueError as exc:
                    raise IntegrityError(
                        f"non-numeric control score: {screen_id} "
                        f"{selected_genes[output_index]}"
                    ) from exc
                if math.isfinite(value):
                    values[output_index] = value
            screen_values[screen_id] = values
    if set(screen_values) != required_screens:
        missing = sorted(required_screens - set(screen_values))
        raise IntegrityError(f"missing denominator score screens: {missing}")
    matrix = np.vstack([screen_values[row.screen_id] for row in denominators])
    finite = np.all(np.isfinite(matrix), axis=0)
    gene_index = {gene: index for index, gene in enumerate(selected_genes)}
    ledger = []
    for panel, genes in panels.items():
        for gene in genes:
            count = header_counts[gene]
            finite_all = bool(finite[gene_index[gene]]) if count == 1 else False
            eligible = count == 1 and finite_all
            if count == 0:
                reason = "absent_from_score_header"
            elif count > 1:
                reason = "duplicate_score_header"
            elif not finite_all:
                reason = "nonfinite_in_full_103_denominator"
            else:
                reason = ""
            ledger.append(
                GeneEligibility(panel, gene, count, finite_all, eligible, reason)
            )
    eligible_genes = [gene for gene, keep in zip(selected_genes, finite, strict=True) if keep]
    return matrix[:, finite], eligible_genes, ledger


def depletion_percentiles(
    matrix: np.ndarray, denominators: Sequence[DenominatorRecord]
) -> np.ndarray:
    percentiles = np.full_like(matrix, np.nan, dtype=float)
    for source, tissue in EXPECTED_DENOMINATORS:
        indices = [
            index
            for index, row in enumerate(denominators)
            if row.source == source and row.tissue == tissue
        ]
        if not indices:
            continue
        values = matrix[indices, :]
        ranks = rankdata(values, method="average", axis=0)
        n = len(indices)
        percentiles[indices, :] = (n - ranks) / (n - 1)
    if not np.all(np.isfinite(percentiles)):
        raise IntegrityError("nonfinite depletion percentiles")
    return percentiles


def build_exposures(
    cohort: dict[str, str],
    denominators: Sequence[DenominatorRecord],
    percentiles: np.ndarray,
    eligible_genes: Sequence[str],
    ledger: Sequence[GeneEligibility],
) -> list[ExposureRecord]:
    row_index = {
        (row.model_id, row.source): index for index, row in enumerate(denominators)
    }
    gene_index = {gene: index for index, gene in enumerate(eligible_genes)}
    panel_columns = {
        panel: [gene_index[row.gene] for row in ledger if row.panel == panel and row.eligible]
        for panel in PANELS
    }
    output = []
    for model_id, tissue in cohort.items():
        avana = percentiles[row_index[(model_id, "Avana")], :]
        ky = percentiles[row_index[(model_id, "KY")], :]
        gap = np.abs(avana - ky)
        exposures = {
            panel: float(np.median(gap[panel_columns[panel]])) for panel in PANELS
        }
        output.append(
            ExposureRecord(
                model_id=model_id,
                tissue=tissue,
                common_essential_exposure=exposures["common_essential"],
                nonessential_exposure=exposures["nonessential"],
            )
        )
    return output


def assess_adequacy(
    exposures: Sequence[ExposureRecord], ledger: Sequence[GeneEligibility]
) -> dict[str, object]:
    eligible_counts = {
        panel: sum(row.panel == panel and row.eligible for row in ledger)
        for panel in PANELS
    }
    panel_results = {}
    for panel in PANELS:
        field = f"{panel}_exposure"
        by_tissue = {}
        for tissue in TISSUES:
            values = [getattr(row, field) for row in exposures if row.tissue == tissue]
            by_tissue[tissue] = {
                "n": len(values),
                "finite": all(math.isfinite(value) for value in values),
                "distinct_values": len(set(values)),
                "adequate": (
                    len(values) == 17
                    and all(math.isfinite(value) for value in values)
                    and len(set(values)) >= 10
                ),
            }
        panel_results[panel] = {
            "eligible_genes": eligible_counts[panel],
            "minimum_eligible_genes": MINIMUM_ELIGIBLE[panel],
            "gene_count_adequate": eligible_counts[panel] >= MINIMUM_ELIGIBLE[panel],
            "by_tissue": by_tissue,
            "adequate": (
                eligible_counts[panel] >= MINIMUM_ELIGIBLE[panel]
                and all(result["adequate"] for result in by_tissue.values())
            ),
        }
    return {
        "panels": panel_results,
        "overall_adequate": all(result["adequate"] for result in panel_results.values()),
    }


def load_outcome(path: Path, cohort: dict[str, str]) -> dict[str, tuple[float, bool]]:
    output = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            model_id = row["model_id"].strip()
            if model_id not in cohort:
                continue
            if row["tissue"].strip() != cohort[model_id] or model_id in output:
                raise IntegrityError(f"outcome identity drift: {model_id}")
            value = float(row["absolute_percentile_gap"])
            if not math.isfinite(value):
                raise IntegrityError(f"nonfinite WRN gap: {model_id}")
            output[model_id] = (
                value,
                row["discordant_ge_0_25"].strip().lower() == "true",
            )
    if set(output) != set(cohort):
        raise IntegrityError("WRN outcome cohort mismatch")
    return output


def combine_analysis_rows(
    exposures: Sequence[ExposureRecord], outcome: dict[str, tuple[float, bool]]
) -> list[AnalysisRecord]:
    return [
        AnalysisRecord(
            **asdict(row),
            wrn_percentile_gap=outcome[row.model_id][0],
            exp005_gap_flag=outcome[row.model_id][1],
        )
        for row in exposures
    ]


def frozen_arrays(
    rows: Sequence[AnalysisRecord], panel: str
) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    field = f"{panel}_exposure"
    output = {}
    for tissue in TISSUES:
        selected = sorted(
            (row for row in rows if row.tissue == tissue), key=lambda row: row.model_id
        )
        x = rankdata([getattr(row, field) for row in selected], method="average")
        y = rankdata([row.wrn_percentile_gap for row in selected], method="average")
        if np.all(x == x[0]) or np.all(y == y[0]):
            raise IntegrityError(f"constant inference ranks: {panel} {tissue}")
        output[tissue] = (np.asarray(x), np.asarray(y))
    return output


def analyze_panel(
    rows: Sequence[AnalysisRecord],
    panel: str,
    seed: int,
    permutations: int,
    bootstraps: int,
) -> dict[str, object]:
    arrays = frozen_arrays(rows, panel)
    theta, tissue = estimate_from_arrays(arrays)
    p_value = permutation_pvalue(
        arrays, theta, permutations, np.random.default_rng(seed)
    )
    ci_low, ci_high = bootstrap_interval(
        arrays, bootstraps, np.random.default_rng(seed)
    )
    gates = {
        "point_target_theta_at_least_0_40": theta >= 0.40,
        "permutation_p_at_most_0_05": p_value <= 0.05,
        "practical_ci_lower_above_0_10": ci_low > 0.10,
        "no_tissue_below_minus_0_20": min(tissue.values()) >= -0.20,
    }
    return {
        "theta_equal_tissue_mean_spearman": theta,
        "tissue_spearman": tissue,
        "permutation_p_one_sided": p_value,
        "bootstrap_ci_95": [ci_low, ci_high],
        "gates": gates,
        "passed_all_gates": all(gates.values()),
    }


def write_dataclasses(path: Path, rows: Sequence[object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise IntegrityError(f"refusing to write empty table: {path}")
    fields = list(rows[0].__dataclass_fields__)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def run(args: argparse.Namespace) -> dict[str, object]:
    receipt = verify_pre_outcome_hashes(args)
    cohort = load_cohort(Path(args.cohort_file))
    denominators = load_denominators(Path(args.denominator_file))
    panels = {
        "common_essential": load_control_list(Path(args.essential_file)),
        "nonessential": load_control_list(Path(args.nonessential_file)),
    }
    matrix, eligible_genes, ledger = load_control_scores(
        Path(args.score_file), denominators, panels
    )
    percentiles = depletion_percentiles(matrix, denominators)
    exposures = build_exposures(
        cohort, denominators, percentiles, eligible_genes, ledger
    )
    adequacy = assess_adequacy(exposures, ledger)
    write_dataclasses(
        Path(args.gene_output), sorted(ledger, key=lambda row: (row.panel, row.gene))
    )
    if not adequacy["overall_adequate"]:
        write_dataclasses(
            Path(args.model_output),
            sorted(exposures, key=lambda row: (row.tissue, row.model_id)),
        )
        return {
            "experiment_id": EXPERIMENT_ID,
            "status": "FAIL_T0_CONTROL_EXPOSURE_ADEQUACY",
            "analysis_type": "outcome_sequential_preregistered_derived_analysis",
            "input_receipt": receipt,
            "adequacy": adequacy,
            "outcome_hash_verified": False,
            "outcome_values_loaded": False,
            "association_computed": False,
            "overall_pass": False,
        }
    outcome_hash = sha256(Path(args.gap_file))
    if outcome_hash != EXPECTED_OUTCOME_HASH:
        raise IntegrityError(
            f"gap_file SHA-256 drift: expected {EXPECTED_OUTCOME_HASH}, got {outcome_hash}"
        )
    receipt["gap_file_sha256"] = outcome_hash
    outcome = load_outcome(Path(args.gap_file), cohort)
    rows = combine_analysis_rows(exposures, outcome)
    panel_results = {
        panel: analyze_panel(
            rows, panel, args.seed, args.permutations, args.bootstraps
        )
        for panel in PANELS
    }
    primary_pass = panel_results["common_essential"]["passed_all_gates"]
    corroborative_pass = panel_results["nonessential"]["passed_all_gates"]
    if primary_pass and corroborative_pass:
        status = "PASS_BOTH_MODEL_GENERAL_DISCORDANCE"
    elif primary_pass:
        status = "PASS_COMMON_ESSENTIAL_ONLY"
    else:
        status = "FAIL_PRIMARY_CONTROL_DISCORDANCE"
    write_dataclasses(
        Path(args.model_output), sorted(rows, key=lambda row: (row.tissue, row.model_id))
    )
    return {
        "experiment_id": EXPERIMENT_ID,
        "status": status,
        "analysis_type": "preregistered_derived_observational_analysis_after_endpoint_unsealing",
        "input_receipt": receipt,
        "adequacy": adequacy,
        "outcome_hash_verified": True,
        "outcome_values_loaded": True,
        "association_computed": True,
        "seed": args.seed,
        "permutation_repeats_per_panel": args.permutations,
        "bootstrap_repeats_per_panel": args.bootstraps,
        "panel_results": panel_results,
        "primary_common_essential_pass": primary_pass,
        "corroborative_nonessential_pass": corroborative_pass,
        "broad_model_general_claim_supported": primary_pass and corroborative_pass,
        "overall_pass": primary_pass,
        "claim_boundary": "model-level observational control-gene discordance association only",
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--cohort-file", default="experiments/EXP-20260822-007/cohort.csv"
    )
    parser.add_argument(
        "--denominator-file",
        default="experiments/EXP-20260822-003/results/model_scores.csv",
    )
    parser.add_argument(
        "--score-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv"
    )
    parser.add_argument(
        "--essential-file",
        default="data/raw/depmap/23q4/AchillesCommonEssentialControls.csv",
    )
    parser.add_argument(
        "--nonessential-file",
        default="data/raw/depmap/23q4/AchillesNonessentialControls.csv",
    )
    parser.add_argument(
        "--gap-file",
        default="experiments/EXP-20260822-005/results/model_percentile_gaps.csv",
    )
    parser.add_argument(
        "--output", default="experiments/EXP-20260822-008/results/summary.json"
    )
    parser.add_argument(
        "--model-output",
        default="experiments/EXP-20260822-008/results/model_exposures.csv",
    )
    parser.add_argument(
        "--gene-output",
        default="experiments/EXP-20260822-008/results/gene_eligibility.csv",
    )
    parser.add_argument("--seed", type=int, default=20260828)
    parser.add_argument("--permutations", type=int, default=100000)
    parser.add_argument("--bootstraps", type=int, default=10000)
    parser.add_argument("--smoke", action="store_true")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.smoke:
        args.permutations = 200
        args.bootstraps = 200
    output = Path(args.output)
    try:
        result = run(args)
    except IntegrityError as exc:
        result = {
            "experiment_id": EXPERIMENT_ID,
            "status": "ERROR_INTEGRITY",
            "error": str(exc),
            "association_computed": False,
            "overall_pass": False,
        }
        exit_code = 1
    else:
        exit_code = 0 if result["overall_pass"] else 2
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
