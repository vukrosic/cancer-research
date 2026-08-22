from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import tempfile
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Iterable, Sequence

import numpy as np
from scipy.stats import norm, rankdata


EXPERIMENT_ID = "EXP-20260822-014"
SOURCES = ("Avana", "KY")
PAIRS = (
    {
        "pair_id": "STAG2_to_STAG1",
        "loss_gene": "STAG2",
        "target_gene": "STAG1",
        "matrix_column": "STAG2 (10735)",
        "score_column": "STAG1 (10274)",
        "primary": True,
    },
    {
        "pair_id": "PDS5B_to_PDS5A",
        "loss_gene": "PDS5B",
        "target_gene": "PDS5A",
        "matrix_column": "PDS5B (23047)",
        "score_column": "PDS5A (23244)",
        "primary": False,
    },
)
PAIR_BY_ID = {pair["pair_id"]: pair for pair in PAIRS}
SOURCE_COLUMNS = {"Avana": "Avana", "KY": "KY"}
EXPECTED_HASHES = {
    "endpoint": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "screen_qc": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "screen_map": "1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad",
    "model": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "damaging": "aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3",
}
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_LOSS_COUNTS = {
    ("STAG2_to_STAG1", "Avana"): 31,
    ("STAG2_to_STAG1", "KY"): 9,
    ("PDS5B_to_PDS5A", "Avana"): 23,
    ("PDS5B_to_PDS5A", "KY"): 12,
}
TARGET_SCORE_COLUMNS = {pair["pair_id"]: pair["score_column"] for pair in PAIRS}
PERMUTATIONS = 100_000
BOOTSTRAPS = 10_000
DESIGN_SIMULATIONS = 10_000
SEED = 20260830
MIN_LOSS = 8
MIN_INTACT = 50
MIN_LINEAGES = 5
DELTA_TARGET = -0.20
P_MAX = 0.05
BOOTSTRAP_UPPER_MAX = 0.0
MAX_LINEAGE_DELTA = 0.20
MIN_CONFIRMATORY_POWER = 0.80
EXPECTED_RESULT_FILES = {
    "context_ledger.csv",
    "design_sensitivity.csv",
    "endpoint_scores.csv",
    "inference.csv",
    "summary.json",
}


class IntegrityError(RuntimeError):
    """Raised when a frozen input, ordering, or analysis invariant drifts."""


class T0Stop(IntegrityError):
    """A preregistered non-evaluable stop, distinct from input/code integrity drift."""

    def __init__(self, status: str, endpoint_opened: bool, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.endpoint_opened = endpoint_opened


@dataclass(frozen=True)
class EligibleScreen:
    screen_id: str
    model_id: str
    source: str
    lineage: str


@dataclass(frozen=True)
class Context:
    source: str
    model_id: str
    lineage: str
    screen_ids: tuple[str, ...]
    statuses: dict[str, str]
    matrix_values: dict[str, int]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_float(value: str, identity: object) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise IntegrityError(f"non-numeric value for {identity}") from exc
    if not math.isfinite(parsed):
        raise IntegrityError(f"non-finite value for {identity}")
    return parsed


def parse_matrix_value(value: str, identity: object) -> int:
    parsed = parse_float(value, identity)
    if parsed not in {0.0, 1.0, 2.0}:
        raise IntegrityError(f"damaging matrix domain drift for {identity}: {parsed}")
    return int(parsed)


def load_model_lineages(path: Path) -> tuple[dict[str, str], str]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["model"]:
        raise IntegrityError(f"Model.csv SHA-256 drift: {actual}")
    lineages: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ModelID", "OncotreeLineage"}
        if not required.issubset(reader.fieldnames or set()):
            raise IntegrityError("Model.csv header drift")
        for row in reader:
            model_id = row["ModelID"].strip()
            lineage = row["OncotreeLineage"].strip()
            if not model_id or model_id in lineages:
                raise IntegrityError(f"invalid Model.csv identity: {model_id}")
            lineages[model_id] = lineage
    return lineages, actual


def load_screen_map(path: Path) -> tuple[dict[str, str], str]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["screen_map"]:
        raise IntegrityError(f"CRISPRScreenMap.csv SHA-256 drift: {actual}")
    mapping: dict[str, str] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if set((reader.fieldnames or ())) != {"ScreenID", "ModelID"}:
            raise IntegrityError("CRISPRScreenMap.csv header drift")
        for row in reader:
            screen_id = row["ScreenID"].strip()
            model_id = row["ModelID"].strip()
            if not screen_id or screen_id in mapping or not model_id:
                raise IntegrityError(f"invalid screen map identity: {screen_id}")
            mapping[screen_id] = model_id
    return mapping, actual


def load_damaging_matrix(path: Path, model_ids: set[str]) -> tuple[dict[str, dict[str, int]], str]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["damaging"]:
        raise IntegrityError(f"damaging matrix SHA-256 drift: {actual}")
    matrix: dict[str, dict[str, int]] = {}
    required_columns = {pair["matrix_column"]: pair["pair_id"] for pair in PAIRS}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or not header or header[0] != "":
            raise IntegrityError("damaging matrix first-column drift")
        indices = {}
        for column in required_columns:
            if header.count(column) != 1:
                raise IntegrityError(f"missing/duplicate damaging column: {column}")
            indices[column] = header.index(column)
        for row in reader:
            if not row:
                continue
            model_id = row[0].strip()
            if model_id in matrix:
                raise IntegrityError(f"duplicate damaging matrix ModelID: {model_id}")
            if model_id not in model_ids:
                continue
            matrix[model_id] = {
                pair_id: parse_matrix_value(row[index], (model_id, column))
                for column, pair_id in required_columns.items()
                for index in [indices[column]]
            }
    if set(matrix) != model_ids:
        raise IntegrityError(
            f"damaging matrix coverage drift: expected {len(model_ids)}, got {len(matrix)}"
        )
    return matrix, actual


def load_context(
    qc_path: Path, screen_map_path: Path, model_path: Path, damaging_path: Path
) -> tuple[list[Context], dict[str, object]]:
    lineages, model_hash = load_model_lineages(model_path)
    screen_map, screen_map_hash = load_screen_map(screen_map_path)
    eligible: list[EligibleScreen] = []
    seen_screens: set[str] = set()
    with qc_path.open(newline="", encoding="utf-8") as handle:
        actual = sha256(qc_path)
        if actual != EXPECTED_HASHES["screen_qc"]:
            raise IntegrityError(f"AchillesScreenQCReport.csv SHA-256 drift: {actual}")
        reader = csv.DictReader(handle)
        required = {"ScreenID", "ModelID", "Library", "PassesQC", "CanInclude"}
        if not required.issubset(reader.fieldnames or set()):
            raise IntegrityError("screen QC header drift")
        for row in reader:
            source = row["Library"].strip()
            if source not in SOURCES:
                continue
            if row["PassesQC"].strip() != "True" or row["CanInclude"].strip() != "True":
                continue
            screen_id = row["ScreenID"].strip()
            model_id = row["ModelID"].strip()
            if screen_id in seen_screens or not model_id or model_id not in lineages:
                raise IntegrityError(f"invalid eligible screen identity: {screen_id}")
            if not lineages[model_id]:
                raise IntegrityError(f"missing lineage for eligible ModelID: {model_id}")
            if screen_map.get(screen_id) != model_id:
                raise IntegrityError(f"screen map mismatch: {screen_id}")
            seen_screens.add(screen_id)
            eligible.append(EligibleScreen(screen_id, model_id, source, lineages[model_id]))
    by_model: dict[tuple[str, str], list[EligibleScreen]] = defaultdict(list)
    for screen in eligible:
        by_model[(screen.source, screen.model_id)].append(screen)
    model_ids = {screen.model_id for screen in eligible}
    damaging, damaging_hash = load_damaging_matrix(damaging_path, model_ids)
    contexts = []
    for (source, model_id), screens in sorted(by_model.items()):
        contexts.append(
            Context(
                source=source,
                model_id=model_id,
                lineage=screens[0].lineage,
                screen_ids=tuple(sorted(screen.screen_id for screen in screens)),
                statuses={
                    pair["pair_id"]: (
                        "damaging" if damaging[model_id][pair["pair_id"]] >= 1 else "intact"
                    )
                    for pair in PAIRS
                },
                matrix_values=damaging[model_id],
            )
        )
    counts = Counter(context.source for context in contexts)
    if dict(counts) != EXPECTED_SOURCE_MODELS:
        raise IntegrityError(f"eligible source/model count drift: {dict(counts)}")
    for pair in PAIRS:
        for source in SOURCES:
            selected = [c for c in contexts if c.source == source]
            losses = [c for c in selected if c.statuses[pair["pair_id"]] == "damaging"]
            intact = [c for c in selected if c.statuses[pair["pair_id"]] == "intact"]
            lineages = {
                c.lineage
                for c in losses
                if any(i.lineage == c.lineage for i in intact)
            }
            if len(losses) != EXPECTED_LOSS_COUNTS[(pair["pair_id"], source)]:
                raise IntegrityError(f"frozen loss count drift: {pair['pair_id']} {source}")
            if len(losses) < MIN_LOSS or len(intact) < MIN_INTACT or len(lineages) < MIN_LINEAGES:
                raise T0Stop(
                    "T0_CONTEXT_ADEQUACY",
                    False,
                    f"context adequacy failure: {pair['pair_id']} {source}",
                )
    receipt = {
        "screen_qc_sha256": actual,
        "screen_map_sha256": screen_map_hash,
        "model_sha256": model_hash,
        "damaging_sha256": damaging_hash,
        "eligible_screens": len(eligible),
        "eligible_source_models": dict(sorted(counts.items())),
        "unique_model_ids": len(model_ids),
    }
    return contexts, receipt


def write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    fields = [
        "source", "model_id", "lineage", "eligible_screen_ids",
        "STAG2_matrix_value", "STAG2_status", "PDS5B_matrix_value", "PDS5B_status",
    ]
    rows = []
    for context in contexts:
        rows.append(
            {
                "source": context.source,
                "model_id": context.model_id,
                "lineage": context.lineage,
                "eligible_screen_ids": ";".join(context.screen_ids),
                "STAG2_matrix_value": context.matrix_values["STAG2_to_STAG1"],
                "STAG2_status": context.statuses["STAG2_to_STAG1"],
                "PDS5B_matrix_value": context.matrix_values["PDS5B_to_PDS5A"],
                "PDS5B_status": context.statuses["PDS5B_to_PDS5A"],
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def grouped_contexts(
    contexts: Sequence[Context], pair_id: str, source: str
) -> dict[str, dict[str, list[str]]]:
    groups: dict[str, dict[str, list[str]]] = defaultdict(lambda: {"damaging": [], "intact": []})
    for context in contexts:
        if context.source == source:
            groups[context.lineage][context.statuses[pair_id]].append(context.model_id)
    return {lineage: {status: sorted(ids) for status, ids in by_status.items()} for lineage, by_status in groups.items()}


def delta_from_scores(
    groups: dict[str, dict[str, list[str]]], scores: dict[str, float]
) -> tuple[float, dict[str, float], int]:
    numerator = 0.0
    denominator = 0
    lineage_deltas = {}
    for lineage, by_status in sorted(groups.items()):
        loss = np.asarray([scores[mid] for mid in by_status["damaging"]], dtype=float)
        intact = np.asarray([scores[mid] for mid in by_status["intact"]], dtype=float)
        if len(loss) == 0 or len(intact) == 0:
            continue
        sorted_intact = np.sort(intact)
        greater = np.searchsorted(sorted_intact, loss, side="left").sum()
        less = (len(intact) - np.searchsorted(sorted_intact, loss, side="right")).sum()
        lineage_numerator = float(greater - less)
        lineage_denominator = len(loss) * len(intact)
        lineage_deltas[lineage] = lineage_numerator / lineage_denominator
        numerator += lineage_numerator
        denominator += lineage_denominator
    if denominator == 0:
        raise IntegrityError("zero pair denominator")
    return float(numerator / denominator), lineage_deltas, denominator


def permutation_deltas(
    groups: dict[str, dict[str, list[str]]],
    scores: dict[str, float],
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    prepared = []
    denominator = 0
    for lineage, by_status in sorted(groups.items()):
        ids = by_status["damaging"] + by_status["intact"]
        if not by_status["damaging"] or not by_status["intact"]:
            continue
        values = np.asarray([scores[mid] for mid in ids], dtype=float)
        ranks = rankdata(values, method="average")
        k = len(by_status["damaging"])
        m = len(by_status["intact"])
        prepared.append((ranks, k, m))
        denominator += k * m
    if denominator == 0:
        raise IntegrityError("zero permutation denominator")
    result = np.empty(repeats, dtype=float)
    generated = 0
    batch_size = 1000
    while generated < repeats:
        batch = min(batch_size, repeats - generated)
        numerator = np.zeros(batch, dtype=float)
        for ranks, k, m in prepared:
            n = len(ranks)
            choices = np.argpartition(rng.random((batch, n)), k - 1, axis=1)[:, :k]
            rank_sums = ranks[choices].sum(axis=1)
            u = rank_sums - (k * (k + 1) / 2)
            numerator += 2 * u - (k * m)
        result[generated : generated + batch] = numerator / denominator
        generated += batch
    return result


def bootstrap_deltas(
    groups: dict[str, dict[str, list[str]]],
    scores: dict[str, float],
    repeats: int,
    rng: np.random.Generator,
) -> np.ndarray:
    result = np.empty(repeats, dtype=float)
    original = {
        lineage: {
            status: np.asarray([scores[mid] for mid in ids], dtype=float)
            for status, ids in by_status.items()
        }
        for lineage, by_status in groups.items()
    }
    for repeat in range(repeats):
        numerator = 0.0
        denominator = 0
        for lineage, by_status in sorted(original.items()):
            loss = rng.choice(by_status["damaging"], size=len(by_status["damaging"]), replace=True)
            intact = rng.choice(by_status["intact"], size=len(by_status["intact"]), replace=True)
            sorted_intact = np.sort(intact)
            greater = np.searchsorted(sorted_intact, loss, side="left").sum()
            less = (len(intact) - np.searchsorted(sorted_intact, loss, side="right")).sum()
            numerator += float(greater - less)
            denominator += len(loss) * len(intact)
        if denominator == 0:
            raise IntegrityError(f"zero bootstrap denominator at replicate {repeat}")
        result[repeat] = numerator / denominator
    return result


def design_sensitivity(
    contexts: Sequence[Context], pair_id: str, source: str, rng: np.random.Generator
) -> dict[str, object]:
    groups = grouped_contexts(contexts, pair_id, source)
    ids = [model_id for by_status in groups.values() for ids in by_status.values() for model_id in ids]
    null_scores = {model_id: float(rng.normal()) for model_id in ids}
    null = permutation_deltas(groups, null_scores, PERMUTATIONS, rng)
    critical = float(np.quantile(null, P_MAX, method="linear"))
    shift = -math.sqrt(2.0) * float(norm.ppf(0.60))
    alternative = np.empty(DESIGN_SIMULATIONS, dtype=float)
    for index in range(DESIGN_SIMULATIONS):
        scores = {
            model_id: float(rng.normal(loc=shift if status == "damaging" else 0.0))
            for lineage, by_status in groups.items()
            for status, group_ids in by_status.items()
            for model_id in group_ids
        }
        alternative[index] = delta_from_scores(groups, scores)[0]
    power = float(np.mean(alternative <= critical))
    return {
        "pair_id": pair_id,
        "source": source,
        "loss_models": sum(len(v["damaging"]) for v in groups.values()),
        "intact_models": sum(len(v["intact"]) for v in groups.values()),
        "contributing_lineages": sum(bool(v["damaging"]) and bool(v["intact"]) for v in groups.values()),
        "expected_delta": DELTA_TARGET,
        "normal_mean_shift": shift,
        "null_permutations": PERMUTATIONS,
        "alternative_simulations": DESIGN_SIMULATIONS,
        "null_lower_05_critical_delta": critical,
        "simulated_power_for_permutation_gate": power,
        "confirmatory_power_adequate": power >= MIN_CONFIRMATORY_POWER,
    }


def write_design_rows(path: Path, rows: Sequence[dict[str, object]]) -> None:
    fields = [
        "pair_id", "source", "loss_models", "intact_models", "contributing_lineages",
        "expected_delta", "normal_mean_shift", "null_permutations",
        "alternative_simulations", "null_lower_05_critical_delta",
        "simulated_power_for_permutation_gate", "confirmatory_power_adequate",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_endpoint(
    path: Path, contexts: Sequence[Context]
) -> tuple[dict[tuple[str, str], float], dict[str, object]]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["endpoint"]:
        raise IntegrityError(f"ScreenNaiveGeneScore.csv SHA-256 drift: {actual}")
    screen_to_context = {
        screen_id: context
        for context in contexts
        for screen_id in context.screen_ids
    }
    values: dict[tuple[str, str], list[float]] = defaultdict(list)
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or header[0] != "":
            raise IntegrityError("endpoint header drift")
        indices = {}
        for pair in PAIRS:
            column = pair["score_column"]
            if header.count(column) != 1:
                raise IntegrityError(f"missing/duplicate endpoint column: {column}")
            indices[pair["pair_id"]] = header.index(column)
        seen_screens: set[str] = set()
        eligible_ids = set(screen_to_context)
        for row in reader:
            if not row:
                continue
            screen_id = row[0].strip()
            if screen_id not in eligible_ids:
                continue
            if screen_id in seen_screens:
                raise IntegrityError(f"duplicate endpoint ScreenID: {screen_id}")
            seen_screens.add(screen_id)
            context = screen_to_context[screen_id]
            for pair in PAIRS:
                index = indices[pair["pair_id"]]
                if index >= len(row) or not row[index].strip():
                    continue
                value = parse_float(row[index], (screen_id, pair["pair_id"]))
                values[(context.source, context.model_id, pair["pair_id"])].append(value)
    model_scores: dict[tuple[str, str], float] = {}
    missing = []
    for context in contexts:
        for pair in PAIRS:
            key = (context.source, context.model_id, pair["pair_id"])
            if not values[key]:
                missing.append(key)
            else:
                model_scores[key] = float(median(values[key]))
    if missing:
        raise T0Stop(
            "T0_ENDPOINT_COMPLETENESS",
            True,
            f"endpoint completeness failure: {len(missing)} missing model/pair values",
        )
    return model_scores, {
        "sha256": actual,
        "eligible_screens_seen": len(seen_screens),
        "eligible_screens_expected": len(screen_to_context),
        "model_pair_values": len(model_scores),
        "median_collapse": True,
    }


def write_endpoint_rows(path: Path, contexts: Sequence[Context], model_scores: dict[tuple[str, str, str], float]) -> None:
    fields = ["pair_id", "source", "model_id", "lineage", "status", "target_score"]
    rows = []
    for context in contexts:
        for pair in PAIRS:
            rows.append(
                {
                    "pair_id": pair["pair_id"],
                    "source": context.source,
                    "model_id": context.model_id,
                    "lineage": context.lineage,
                    "status": context.statuses[pair["pair_id"]],
                    "target_score": model_scores[(context.source, context.model_id, pair["pair_id"])],
                }
            )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def inference_for(
    contexts: Sequence[Context],
    model_scores: dict[tuple[str, str, str], float],
    pair_id: str,
    source: str,
    rng: np.random.Generator,
) -> dict[str, object]:
    groups = grouped_contexts(contexts, pair_id, source)
    scores = {
        model_id: model_scores[(source, model_id, pair_id)]
        for by_status in groups.values()
        for ids in by_status.values()
        for model_id in ids
    }
    delta, lineage_deltas, pair_count = delta_from_scores(groups, scores)
    permutation = permutation_deltas(groups, scores, PERMUTATIONS, rng)
    extreme = int(np.count_nonzero(permutation <= delta))
    p_value = (1 + extreme) / (PERMUTATIONS + 1)
    bootstrap = bootstrap_deltas(groups, scores, BOOTSTRAPS, rng)
    ci_low, ci_high = np.quantile(bootstrap, [0.025, 0.975], method="linear")
    gates = {
        "delta_lt_0": delta < 0,
        "delta_le_minus_0_20": delta <= DELTA_TARGET,
        "permutation_p_le_0_05": p_value <= P_MAX,
        "bootstrap_upper_lt_0": float(ci_high) < BOOTSTRAP_UPPER_MAX,
        "at_least_5_negative_lineages": sum(value < 0 for value in lineage_deltas.values()) >= MIN_LINEAGES,
        "no_lineage_delta_gt_plus_0_20": max(lineage_deltas.values()) <= MAX_LINEAGE_DELTA,
    }
    return {
        "pair_id": pair_id,
        "source": source,
        "delta": delta,
        "pair_count": pair_count,
        "lineage_deltas": lineage_deltas,
        "permutation_repeats": PERMUTATIONS,
        "permutation_extreme_count": extreme,
        "permutation_p_one_sided_lower": p_value,
        "bootstrap_repeats": BOOTSTRAPS,
        "bootstrap_ci_95_percentile": [float(ci_low), float(ci_high)],
        "gates": gates,
        "pass": all(gates.values()),
    }


def write_inference(path: Path, results: Sequence[dict[str, object]]) -> None:
    fields = [
        "pair_id", "source", "primary_confirmatory", "delta", "pair_count",
        "permutation_extreme_count", "permutation_p_one_sided_lower",
        "bootstrap_ci_low", "bootstrap_ci_high", "pass", "gates_json", "lineage_deltas_json",
    ]
    rows = []
    for result in results:
        ci = result["bootstrap_ci_95_percentile"]
        rows.append(
            {
                "pair_id": result["pair_id"],
                "source": result["source"],
                "primary_confirmatory": PAIR_BY_ID[result["pair_id"]]["primary"],
                "delta": result["delta"],
                "pair_count": result["pair_count"],
                "permutation_extreme_count": result["permutation_extreme_count"],
                "permutation_p_one_sided_lower": result["permutation_p_one_sided_lower"],
                "bootstrap_ci_low": ci[0],
                "bootstrap_ci_high": ci[1],
                "pass": result["pass"],
                "gates_json": json.dumps(result["gates"], sort_keys=True),
                "lineage_deltas_json": json.dumps(result["lineage_deltas"], sort_keys=True),
            }
        )
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def summary_digest(result: dict[str, object]) -> str:
    payload = json.loads(json.dumps(result))
    payload["artifact_receipt_sha256"]["summary.json"] = ""
    return hashlib.sha256((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()).hexdigest()


def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    contexts, context_receipt = load_context(
        Path(args.qc_file), Path(args.screen_map_file), Path(args.model_file), Path(args.damaging_file)
    )
    write_context_ledger(stage / "context_ledger.csv", contexts)
    context_receipt["context_ledger_sha256"] = sha256(stage / "context_ledger.csv")
    design_rows = []
    for pair_index, pair in enumerate(PAIRS):
        for source_index, source in enumerate(SOURCES):
            design_rows.append(
                design_sensitivity(
                    contexts,
                    pair["pair_id"],
                    source,
                    np.random.default_rng(SEED + 1000 * pair_index + 100 * source_index),
                )
            )
    write_design_rows(stage / "design_sensitivity.csv", design_rows)
    design_receipt = {
        "design_sensitivity_sha256": sha256(stage / "design_sensitivity.csv"),
        "minimum_confirmatory_power": MIN_CONFIRMATORY_POWER,
        "all_primary_sources_power_adequate": all(
            row["confirmatory_power_adequate"]
            for row in design_rows
            if row["pair_id"] == "STAG2_to_STAG1"
        ),
    }

    model_scores, endpoint_receipt = load_endpoint(Path(args.endpoint_file), contexts)
    write_endpoint_rows(stage / "endpoint_scores.csv", contexts, model_scores)
    results = []
    for pair_index, pair in enumerate(PAIRS):
        for source_index, source in enumerate(SOURCES):
            results.append(
                inference_for(
                    contexts,
                    model_scores,
                    pair["pair_id"],
                    source,
                    np.random.default_rng(SEED + 10000 + 1000 * pair_index + 100 * source_index),
                )
            )
    write_inference(stage / "inference.csv", results)
    primary_results = [r for r in results if r["pair_id"] == "STAG2_to_STAG1"]
    power_by_source = {
        row["source"]: row["simulated_power_for_permutation_gate"]
        for row in design_rows
        if row["pair_id"] == "STAG2_to_STAG1"
    }
    primary_pass = all(r["pass"] for r in primary_results)
    power_adequate = design_receipt["all_primary_sources_power_adequate"]
    status = "PASS_CONFIRMATORY_CORROBORATION" if primary_pass and power_adequate else "FEASIBILITY_ONLY_OR_PRIMARY_FAILURE"
    artifact_receipt = {
        name: sha256(stage / name)
        for name in ("context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv")
    }
    artifact_receipt["summary.json"] = ""
    secondary = [r for r in results if r["pair_id"] == "PDS5B_to_PDS5A"]
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": status,
        "analysis_type": "preregistered_source_specific_lineage_stratified_paralog_status_replication",
        "claim_eligibility": {
            "primary_confirmatory": primary_pass and power_adequate,
            "design_sensitivity_label": "CONFIRMATORY_ELIGIBLE" if power_adequate else "FEASIBILITY_ONLY",
            "secondary_confirmatory": False,
        },
        "context_receipt": context_receipt,
        "design_sensitivity": design_receipt,
        "endpoint_receipt": endpoint_receipt,
        "primary": primary_results,
        "secondary_descriptive": secondary,
        "inference_receipt": {
            "seed": SEED,
            "permutations": PERMUTATIONS,
            "bootstraps": BOOTSTRAPS,
            "bootstrap_interval": "percentile_95_linear_quantile",
            "unit": "collapsed_source_model_id",
            "cross_source_raw_score_comparison": False,
        },
        "artifact_receipt_sha256": artifact_receipt,
        "overall_pass": primary_pass and power_adequate,
        "claim_boundary": "matrix-defined damaging-status association with source-specific target-gene dependency in the frozen 23Q4 cell-line screen cohorts; no biological independence or clinical claim",
    }
    return result


def write_error(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False)
    temporary = Path(handle.name)
    try:
        with handle:
            handle.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP014 staged file set drift")
    with (stage / "context_ledger.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != sum(EXPECTED_SOURCE_MODELS.values()) or len({(r["source"], r["model_id"]) for r in rows}) != len(rows):
        raise IntegrityError("context ledger identity drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4 or len({(r["pair_id"], r["source"]) for r in rows}) != 4:
        raise IntegrityError("design sensitivity receipt drift")
    with (stage / "endpoint_scores.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != sum(EXPECTED_SOURCE_MODELS.values()) * len(PAIRS):
        raise IntegrityError("endpoint ledger count drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 4 or len({(r["pair_id"], r["source"]) for r in rows}) != 4:
        raise IntegrityError("inference receipt drift")
    if set(result) != {
        "experiment_id", "status", "analysis_type", "claim_eligibility", "context_receipt",
        "design_sensitivity", "endpoint_receipt", "primary", "secondary_descriptive",
        "inference_receipt", "artifact_receipt_sha256", "overall_pass", "claim_boundary",
    }:
        raise IntegrityError("summary schema drift")
    if result["experiment_id"] != EXPERIMENT_ID or result["overall_pass"] != result["claim_eligibility"]["primary_confirmatory"]:
        raise IntegrityError("summary identity/pass drift")
    if set(result["artifact_receipt_sha256"]) != EXPECTED_RESULT_FILES:
        raise IntegrityError("artifact receipt key drift")
    for name in EXPECTED_RESULT_FILES - {"summary.json"}:
        if result["artifact_receipt_sha256"][name] != sha256(stage / name):
            raise IntegrityError(f"artifact hash drift: {name}")
    if result["artifact_receipt_sha256"]["summary.json"] != summary_digest(result):
        raise IntegrityError("summary normalized self-digest drift")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--screen-map-file", default="data/raw/depmap/23q4/CRISPRScreenMap.csv")
    parser.add_argument("--model-file", default="data/raw/depmap/23q4/Model.csv")
    parser.add_argument("--damaging-file", default="data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-014/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-014/error_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target = Path(args.results_dir)
    error = Path(args.error_receipt)
    if target.exists():
        write_error(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False})
        return 1
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(dir=target.parent, prefix=f".{target.name}.stage.") as temporary_name:
            stage = Path(temporary_name)
            result = run(args, stage)
            result["artifact_receipt_sha256"]["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            if json.loads((stage / "summary.json").read_text(encoding="utf-8")) != result:
                raise IntegrityError("summary round-trip drift")
            os.replace(stage, target)
    except T0Stop as exc:
        write_error(
            error,
            {
                "experiment_id": EXPERIMENT_ID,
                "status": exc.status,
                "error": str(exc),
                "error_type": type(exc).__name__,
                "t0": True,
                "endpoint_opened": exc.endpoint_opened,
                "results_written": False,
            },
        )
        return 2
    except Exception as exc:
        write_error(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
