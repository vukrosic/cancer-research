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
from typing import Sequence

import numpy as np

from .paralog_replication import (
    IntegrityError,
    T0Stop,
    bootstrap_deltas,
    delta_from_scores,
    permutation_deltas,
)


EXPERIMENT_ID = "EXP-20260822-015"
SOURCES = ("Avana", "KY")
STATUS_COLUMN = "ARID1A (8289)"
TARGET_COLUMN = "ARID1B (57492)"
PAIR_ID = "ARID1A_to_ARID1B"
EXPECTED_HASHES = {
    "endpoint": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "screen_qc": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "screen_map": "1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad",
    "model": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "damaging": "aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3",
}
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_LOSS_COUNTS = {"Avana": 101, "KY": 43}
PERMUTATIONS = 100_000
BOOTSTRAPS = 10_000
DESIGN_SIMULATIONS = 10_000
SEED = 20260830
DESIGN_SEEDS = {"Avana": 20260830, "KY": 20260930}
INFERENCE_SEEDS = {"Avana": 20270830, "KY": 20270930}
NORMAL_MEAN_SHIFT = -0.358286909243
MIN_LOSS = 20
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
    status: str
    matrix_value: int


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
        if not {"ModelID", "OncotreeLineage"}.issubset(reader.fieldnames or set()):
            raise IntegrityError("Model.csv header drift")
        for row in reader:
            model_id = row["ModelID"].strip()
            lineage = row["OncotreeLineage"].strip()
            if not model_id or model_id in lineages or not lineage:
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
        if set(reader.fieldnames or ()) != {"ScreenID", "ModelID"}:
            raise IntegrityError("CRISPRScreenMap.csv header drift")
        for row in reader:
            screen_id = row["ScreenID"].strip()
            model_id = row["ModelID"].strip()
            if not screen_id or screen_id in mapping or not model_id:
                raise IntegrityError(f"invalid screen map identity: {screen_id}")
            mapping[screen_id] = model_id
    return mapping, actual


def load_status_matrix(path: Path, model_ids: set[str]) -> tuple[dict[str, int], str]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["damaging"]:
        raise IntegrityError(f"damaging matrix SHA-256 drift: {actual}")
    statuses: dict[str, int] = {}
    seen_model_ids: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or not header or header[0] != "":
            raise IntegrityError("damaging matrix first-column drift")
        if header.count(STATUS_COLUMN) != 1:
            raise IntegrityError(f"missing/duplicate damaging column: {STATUS_COLUMN}")
        index = header.index(STATUS_COLUMN)
        for row in reader:
            if not row:
                continue
            model_id = row[0].strip()
            if not model_id or model_id in seen_model_ids:
                raise IntegrityError(f"duplicate damaging matrix ModelID: {model_id}")
            seen_model_ids.add(model_id)
            if model_id in model_ids:
                if index >= len(row):
                    raise IntegrityError(f"short damaging row for {model_id}")
                statuses[model_id] = parse_matrix_value(row[index], (model_id, STATUS_COLUMN))
    if set(statuses) != model_ids:
        raise IntegrityError(
            f"damaging matrix coverage drift: expected {len(model_ids)}, got {len(statuses)}"
        )
    return statuses, actual


def load_context(
    qc_path: Path,
    screen_map_path: Path,
    model_path: Path,
    damaging_path: Path,
) -> tuple[list[Context], dict[str, object]]:
    lineages, model_hash = load_model_lineages(model_path)
    screen_map, screen_map_hash = load_screen_map(screen_map_path)
    eligible: list[EligibleScreen] = []
    seen_screens: set[str] = set()
    qc_actual = sha256(qc_path)
    if qc_actual != EXPECTED_HASHES["screen_qc"]:
        raise IntegrityError(f"AchillesScreenQCReport.csv SHA-256 drift: {qc_actual}")
    with qc_path.open(newline="", encoding="utf-8") as handle:
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
    statuses, damaging_hash = load_status_matrix(damaging_path, model_ids)
    contexts = [
        Context(
            source=source,
            model_id=model_id,
            lineage=screens[0].lineage,
            screen_ids=tuple(sorted(screen.screen_id for screen in screens)),
            status="damaging" if statuses[model_id] >= 1 else "intact",
            matrix_value=statuses[model_id],
        )
        for (source, model_id), screens in sorted(by_model.items())
    ]
    counts = Counter(context.source for context in contexts)
    if dict(counts) != EXPECTED_SOURCE_MODELS:
        raise IntegrityError(f"eligible source/model count drift: {dict(counts)}")
    for source in SOURCES:
        selected = [context for context in contexts if context.source == source]
        damaging_models = [context for context in selected if context.status == "damaging"]
        intact_models = [context for context in selected if context.status == "intact"]
        mixed_lineages = {
            context.lineage
            for context in damaging_models
            if any(other.lineage == context.lineage for other in intact_models)
        }
        if len(damaging_models) != EXPECTED_LOSS_COUNTS[source]:
            raise IntegrityError(f"frozen ARID1A loss count drift: {source}")
        if (
            len(damaging_models) < MIN_LOSS
            or len(intact_models) < MIN_INTACT
            or len(mixed_lineages) < MIN_LINEAGES
        ):
            raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"context adequacy failure: {source}")
    return contexts, {
        "screen_qc_sha256": qc_actual,
        "screen_map_sha256": screen_map_hash,
        "model_sha256": model_hash,
        "damaging_sha256": damaging_hash,
        "eligible_screens": len(eligible),
        "eligible_source_models": dict(sorted(counts.items())),
        "unique_model_ids": len(model_ids),
        "status_column": STATUS_COLUMN,
        "status_threshold": 1,
    }


def write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    fields = [
        "source",
        "model_id",
        "lineage",
        "eligible_screen_ids",
        "ARID1A_matrix_value",
        "ARID1A_status",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {
                "source": context.source,
                "model_id": context.model_id,
                "lineage": context.lineage,
                "eligible_screen_ids": ";".join(context.screen_ids),
                "ARID1A_matrix_value": context.matrix_value,
                "ARID1A_status": context.status,
            }
            for context in contexts
        )


def grouped_contexts(contexts: Sequence[Context], source: str) -> dict[str, dict[str, list[str]]]:
    groups: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"damaging": [], "intact": []}
    )
    for context in contexts:
        if context.source == source:
            groups[context.lineage][context.status].append(context.model_id)
    return {
        lineage: {status: sorted(ids) for status, ids in by_status.items()}
        for lineage, by_status in groups.items()
    }


def design_sensitivity(
    contexts: Sequence[Context], source: str, rng: np.random.Generator
) -> dict[str, object]:
    groups = grouped_contexts(contexts, source)
    ids = [model_id for by_status in groups.values() for ids in by_status.values() for model_id in ids]
    null_scores = {model_id: float(rng.normal()) for model_id in ids}
    null = permutation_deltas(groups, null_scores, PERMUTATIONS, rng)
    critical = float(np.quantile(null, P_MAX, method="linear"))
    shift = NORMAL_MEAN_SHIFT
    alternative = np.empty(DESIGN_SIMULATIONS, dtype=float)
    for index in range(DESIGN_SIMULATIONS):
        scores = {
            model_id: float(rng.normal(loc=shift if status == "damaging" else 0.0))
            for by_status in groups.values()
            for status, group_ids in by_status.items()
            for model_id in group_ids
        }
        alternative[index] = delta_from_scores(groups, scores)[0]
    power = float(np.mean(alternative <= critical))
    return {
        "pair_id": PAIR_ID,
        "source": source,
        "loss_models": sum(len(by_status["damaging"]) for by_status in groups.values()),
        "intact_models": sum(len(by_status["intact"]) for by_status in groups.values()),
        "contributing_lineages": sum(
            bool(by_status["damaging"]) and bool(by_status["intact"])
            for by_status in groups.values()
        ),
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
        "pair_id",
        "source",
        "loss_models",
        "intact_models",
        "contributing_lineages",
        "expected_delta",
        "normal_mean_shift",
        "null_permutations",
        "alternative_simulations",
        "null_lower_05_critical_delta",
        "simulated_power_for_permutation_gate",
        "confirmatory_power_adequate",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_endpoint(
    path: Path, contexts: Sequence[Context]
) -> tuple[dict[str, float], dict[str, object]]:
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
        if header is None or not header or header[0] != "":
            raise IntegrityError("endpoint header drift")
        if header.count(TARGET_COLUMN) != 1:
            raise IntegrityError(f"missing/duplicate endpoint column: {TARGET_COLUMN}")
        index = header.index(TARGET_COLUMN)
        seen_screens: set[str] = set()
        for row in reader:
            if not row:
                continue
            screen_id = row[0].strip()
            if screen_id not in screen_to_context:
                continue
            if screen_id in seen_screens:
                raise IntegrityError(f"duplicate endpoint ScreenID: {screen_id}")
            seen_screens.add(screen_id)
            if index >= len(row) or not row[index].strip():
                continue
            context = screen_to_context[screen_id]
            values[(context.source, context.model_id)].append(
                parse_float(row[index], (screen_id, TARGET_COLUMN))
            )
    model_scores: dict[tuple[str, str], float] = {}
    missing = []
    for context in contexts:
        key = (context.source, context.model_id)
        if not values[key]:
            missing.append((context.source, context.model_id))
        else:
            model_scores[key] = float(median(values[key]))
    if missing:
        raise T0Stop(
            "T0_ENDPOINT_COMPLETENESS",
            True,
            f"endpoint completeness failure: {len(missing)} missing model values",
        )
    return model_scores, {
        "sha256": actual,
        "eligible_screens_seen": len(seen_screens),
        "eligible_screens_expected": len(screen_to_context),
        "model_values": len(model_scores),
        "median_collapse": True,
    }


def write_endpoint_rows(
    path: Path, contexts: Sequence[Context], scores: dict[tuple[str, str], float]
) -> None:
    fields = ["pair_id", "source", "model_id", "lineage", "status", "target_score"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(
            {
                "pair_id": PAIR_ID,
                "source": context.source,
                "model_id": context.model_id,
                "lineage": context.lineage,
                "status": context.status,
                "target_score": scores[(context.source, context.model_id)],
            }
            for context in contexts
        )


def inference_for(
    contexts: Sequence[Context],
    scores: dict[tuple[str, str], float],
    source: str,
    rng: np.random.Generator,
) -> dict[str, object]:
    groups = grouped_contexts(contexts, source)
    source_scores = {
        model_id: scores[(source, model_id)]
        for by_status in groups.values()
        for ids in by_status.values()
        for model_id in ids
    }
    delta, lineage_deltas, pair_count = delta_from_scores(groups, source_scores)
    permutation = permutation_deltas(groups, source_scores, PERMUTATIONS, rng)
    extreme = int(np.count_nonzero(permutation <= delta))
    p_value = (1 + extreme) / (PERMUTATIONS + 1)
    bootstrap = bootstrap_deltas(groups, source_scores, BOOTSTRAPS, rng)
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
        "pair_id": PAIR_ID,
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
        "pair_id",
        "source",
        "primary_confirmatory",
        "delta",
        "pair_count",
        "permutation_extreme_count",
        "permutation_p_one_sided_lower",
        "bootstrap_ci_low",
        "bootstrap_ci_high",
        "pass",
        "gates_json",
        "lineage_deltas_json",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for result in results:
            interval = result["bootstrap_ci_95_percentile"]
            writer.writerow(
                {
                    "pair_id": result["pair_id"],
                    "source": result["source"],
                    "primary_confirmatory": False,
                    "delta": result["delta"],
                    "pair_count": result["pair_count"],
                    "permutation_extreme_count": result["permutation_extreme_count"],
                    "permutation_p_one_sided_lower": result["permutation_p_one_sided_lower"],
                    "bootstrap_ci_low": interval[0],
                    "bootstrap_ci_high": interval[1],
                    "pass": result["pass"],
                    "gates_json": json.dumps(result["gates"], sort_keys=True),
                    "lineage_deltas_json": json.dumps(result["lineage_deltas"], sort_keys=True),
                }
            )


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
    design_rows = [
        design_sensitivity(contexts, source, np.random.default_rng(DESIGN_SEEDS[source]))
        for source in SOURCES
    ]
    write_design_rows(stage / "design_sensitivity.csv", design_rows)
    design_receipt = {
        "design_sensitivity_sha256": sha256(stage / "design_sensitivity.csv"),
        "minimum_confirmatory_power": MIN_CONFIRMATORY_POWER,
        "frozen_label": "FEASIBILITY_ONLY",
        "confirmatory_claim_enabled": False,
        "all_primary_sources_power_adequate": all(
            row["confirmatory_power_adequate"] for row in design_rows
        ),
    }

    pre_endpoint_payload = {
        "experiment_id": EXPERIMENT_ID,
        "context_ledger_sha256": context_receipt["context_ledger_sha256"],
        "design_sensitivity_sha256": design_receipt["design_sensitivity_sha256"],
    }
    pre_endpoint_receipt = {
        **pre_endpoint_payload,
        "receipt_sha256": hashlib.sha256(
            (json.dumps(pre_endpoint_payload, sort_keys=True) + "\n").encode()
        ).hexdigest(),
        "sealed_before_endpoint": True,
    }
    write_json_atomic(Path(args.pre_endpoint_receipt), pre_endpoint_receipt)

    scores, endpoint_receipt = load_endpoint(Path(args.endpoint_file), contexts)
    write_endpoint_rows(stage / "endpoint_scores.csv", contexts, scores)
    results = [
        inference_for(contexts, scores, source, np.random.default_rng(INFERENCE_SEEDS[source]))
        for source in SOURCES
    ]
    write_inference(stage / "inference.csv", results)
    primary_pass = all(result["pass"] for result in results)
    confirmatory = False
    result = {
        "experiment_id": EXPERIMENT_ID,
        "status": "FEASIBILITY_ONLY_NOMINAL_GATES_PASS" if primary_pass else "FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE",
        "analysis_type": "preregistered_source_specific_lineage_stratified_arid1a_status_replication",
        "claim_eligibility": {
            "primary_confirmatory": confirmatory,
            "design_sensitivity_label": "FEASIBILITY_ONLY",
            "nominal_primary_gates_pass": primary_pass,
        },
        "context_receipt": context_receipt,
        "design_sensitivity": design_receipt,
        "pre_endpoint_receipt": pre_endpoint_receipt,
        "endpoint_receipt": endpoint_receipt,
        "primary": results,
        "inference_receipt": {
            "design_seeds": DESIGN_SEEDS,
            "inference_seeds": INFERENCE_SEEDS,
            "permutations": PERMUTATIONS,
            "bootstraps": BOOTSTRAPS,
            "bootstrap_interval": "percentile_95_linear_quantile",
            "unit": "collapsed_source_model_id",
            "cross_source_raw_score_comparison": False,
        },
        "artifact_receipt_sha256": {
            name: sha256(stage / name)
            for name in ("context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv")
        } | {"summary.json": ""},
        "overall_pass": confirmatory,
        "claim_boundary": "matrix-defined damaging ARID1A status association with source-specific ARID1B dependency in frozen 23Q4 cell-line screen cohorts; no biological independence or clinical claim",
    }
    return result


def write_json_atomic(path: Path, payload: dict[str, object]) -> None:
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


def write_error(path: Path, payload: dict[str, object]) -> None:
    write_json_atomic(path, payload)


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP015 staged file set drift")
    with (stage / "context_ledger.csv").open(newline="", encoding="utf-8") as handle:
        context_rows = list(csv.DictReader(handle))
    if len(context_rows) != sum(EXPECTED_SOURCE_MODELS.values()):
        raise IntegrityError("context ledger count drift")
    if len({(row["source"], row["model_id"]) for row in context_rows}) != len(context_rows):
        raise IntegrityError("context ledger identity drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        design_rows = list(csv.DictReader(handle))
    if len(design_rows) != len(SOURCES) or {row["source"] for row in design_rows} != set(SOURCES):
        raise IntegrityError("design sensitivity receipt drift")
    with (stage / "endpoint_scores.csv").open(newline="", encoding="utf-8") as handle:
        endpoint_rows = list(csv.DictReader(handle))
    if len(endpoint_rows) != sum(EXPECTED_SOURCE_MODELS.values()):
        raise IntegrityError("endpoint ledger count drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        inference_rows = list(csv.DictReader(handle))
    if len(inference_rows) != len(SOURCES) or {row["source"] for row in inference_rows} != set(SOURCES):
        raise IntegrityError("inference receipt drift")
    if any(row["primary_confirmatory"] != "False" for row in inference_rows):
        raise IntegrityError("feasibility-only confirmatory flag drift")
    expected_keys = {
        "experiment_id", "status", "analysis_type", "claim_eligibility", "context_receipt",
        "design_sensitivity", "pre_endpoint_receipt", "endpoint_receipt", "primary", "inference_receipt",
        "artifact_receipt_sha256", "overall_pass", "claim_boundary",
    }
    if set(result) != expected_keys or result["experiment_id"] != EXPERIMENT_ID:
        raise IntegrityError("summary schema drift")
    if result["overall_pass"] != result["claim_eligibility"]["primary_confirmatory"]:
        raise IntegrityError("summary identity/pass drift")
    if result["claim_eligibility"]["primary_confirmatory"] is not False:
        raise IntegrityError("feasibility-only claim drift")
    if result["pre_endpoint_receipt"]["sealed_before_endpoint"] is not True:
        raise IntegrityError("pre-endpoint receipt seal drift")
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
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-015/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-015/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-015/pre_endpoint_receipt.json")
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
            try:
                result = run(args, stage)
            except T0Stop as exc:
                preserved_path = None
                if any(stage.iterdir()):
                    preserved = target.parent / "t0_provenance"
                    if preserved.exists():
                        raise IntegrityError(f"T0 provenance directory already exists: {preserved}")
                    os.replace(stage, preserved)
                    preserved_path = str(preserved)
                write_error(error, {
                    "experiment_id": EXPERIMENT_ID,
                    "status": exc.status,
                    "error": str(exc),
                    "error_type": type(exc).__name__,
                    "t0": True,
                    "endpoint_opened": exc.endpoint_opened,
                    "results_written": False,
                    "preserved_path": preserved_path,
                })
                return 2
            result["artifact_receipt_sha256"]["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            if json.loads((stage / "summary.json").read_text(encoding="utf-8")) != result:
                raise IntegrityError("summary round-trip drift")
            os.replace(stage, target)
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
