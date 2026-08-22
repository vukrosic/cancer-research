from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import subprocess
import tempfile
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Sequence

import numpy as np
from scipy.stats import rankdata


EXPERIMENT_ID = "EXP-20260822-017"
PAIR_ID = "TP53_matrix_intact_to_MDM2"
STATUS_COLUMN = "TP53 (7157)"
TARGET_COLUMN = "MDM2 (4193)"
SOURCES = ("Avana", "KY")
EXPOSED = "matrix_intact"
REFERENCE = "damaging"
EXPECTED_MODULE_PATH = "src/candrel/tp53_mdm2_replication.py"
EXPECTED_HASHES = {
    "endpoint": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "screen_qc": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "screen_map": "1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad",
    "model": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "damaging": "aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3",
}
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_STATUS_COUNTS = {
    "Avana": {EXPOSED: 365, REFERENCE: 610},
    "KY": {EXPOSED: 82, REFERENCE: 233},
}
EXPECTED_MIXED_LINEAGES = {"Avana": 25, "KY": 16}
MIN_EXPOSED = 20
MIN_REFERENCE = 50
MIN_MIXED_LINEAGES = 5
PERMUTATIONS = 100_000
BOOTSTRAPS = 10_000
DESIGN_SIMULATIONS = 10_000
NORMAL_MEAN_SHIFT = -0.358286909243
DELTA_TARGET = -0.20
P_MAX = 0.05
BOOTSTRAP_UPPER_MAX = 0.0
MAX_LINEAGE_DELTA = 0.20
MIN_CONFIRMATORY_POWER = 0.80
DESIGN_SEEDS = {"Avana": 20261730, "KY": 20261830}
INFERENCE_SEEDS = {"Avana": 20271730, "KY": 20271830}
EXPECTED_ROSTER_SHA256 = "61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376"
EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = "cf0979249a2071283089b97168edc8204f0c9b7a5d472726fecba3f1281ec57c"
EXPECTED_RESULT_FILES = {
    "context_ledger.csv",
    "design_sensitivity.csv",
    "endpoint_scores.csv",
    "inference.csv",
    "summary.json",
}


class IntegrityError(RuntimeError):
    pass


class T0Stop(IntegrityError):
    def __init__(self, status: str, endpoint_opened: bool, message: str):
        super().__init__(message)
        self.status = status
        self.endpoint_opened = endpoint_opened


@dataclass(frozen=True)
class Context:
    source: str
    model_id: str
    lineage: str
    screen_ids: tuple[str, ...]
    status: str
    matrix_value: int


@dataclass(frozen=True)
class EligibleScreen:
    screen_id: str
    model_id: str
    source: str
    lineage: str


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
    if not np.isfinite(parsed):
        raise IntegrityError(f"non-finite value for {identity}")
    return parsed


def parse_matrix_value(value: str, identity: object) -> int:
    parsed = parse_float(value, identity)
    if parsed not in {0.0, 1.0, 2.0}:
        raise IntegrityError(f"TP53 matrix domain drift for {identity}: {parsed}")
    return int(parsed)


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


def git_command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["git", *arguments], capture_output=True, text=True, check=False)


def git_blob_sha256(commit: str, path: str) -> str:
    result = subprocess.run(["git", "show", f"{commit}:{path}"], capture_output=True, check=False)
    if result.returncode != 0:
        raise ValueError(f"missing implementation blob: {commit}:{path}")
    return hashlib.sha256(result.stdout).hexdigest()


def normalized_receipt_sha256(path: Path, field: str) -> str:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload[field] = ""
    return hashlib.sha256((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()).hexdigest()


def verify_implementation_boundary(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["experiment_id"] != EXPERIMENT_ID:
            raise ValueError("manifest experiment identity drift")
        if manifest["entrypoint"] != "uv run candrel-tp53-mdm2-replication":
            raise ValueError("manifest entrypoint drift")
        if manifest["inputs"] != {
            "endpoint": {"path": "data/raw/depmap/23q4/ScreenNaiveGeneScore.csv", "sha256": EXPECTED_HASHES["endpoint"], "target_column": TARGET_COLUMN},
            "screen_qc": {"path": "data/raw/depmap/23q4/AchillesScreenQCReport.csv", "sha256": EXPECTED_HASHES["screen_qc"]},
            "screen_map": {"path": "data/raw/depmap/23q4/CRISPRScreenMap.csv", "sha256": EXPECTED_HASHES["screen_map"]},
            "model": {"path": "data/raw/depmap/23q4/Model.csv", "sha256": EXPECTED_HASHES["model"]},
            "damaging_matrix": {"path": "data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv", "sha256": EXPECTED_HASHES["damaging"], "status_column": STATUS_COLUMN},
        }:
            raise ValueError("manifest input contract drift")
        if manifest["eligibility"] != {"libraries": list(SOURCES), "pass_qc": True, "can_include": True, "expected_source_models": EXPECTED_SOURCE_MODELS}:
            raise ValueError("manifest eligibility contract drift")
        if manifest["status_contract"] != {"exposed": EXPOSED, "reference": REFERENCE, "exposed_matrix_value": 0, "reference_matrix_values": [1, 2], "expected_counts": EXPECTED_STATUS_COUNTS, "expected_mixed_lineages": EXPECTED_MIXED_LINEAGES}:
            raise ValueError("manifest status contract drift")
        if manifest["candidate_census"]["path"] != "experiments/EXP-20260822-017/candidate_census.json":
            raise ValueError("candidate census path drift")
        if manifest["design_receipt"]["path"] != "experiments/EXP-20260822-017/design_census_receipt.json":
            raise ValueError("design receipt path drift")
        if manifest["design_receipt"]["canonical_roster_sha256"] != EXPECTED_ROSTER_SHA256:
            raise ValueError("canonical roster hash drift")
        if manifest["design_sensitivity"] != {
            "mean_shift": NORMAL_MEAN_SHIFT,
            "null_permutations": PERMUTATIONS,
            "alternative_simulations": DESIGN_SIMULATIONS,
            "planning_power_seeds": DESIGN_SEEDS,
            "expected_critical_delta": {"Avana": -0.07879789321491273, "KY": -0.14327062228654125},
            "expected_power": {"Avana": 0.9941, "KY": 0.7521},
            "minimum_power_for_confirmatory_label": MIN_CONFIRMATORY_POWER,
            "frozen_label": "FEASIBILITY_ONLY",
        }:
            raise ValueError("manifest design contract drift")
        if manifest["inference"] != {"inference_seeds": INFERENCE_SEEDS, "permutations": PERMUTATIONS, "bootstraps": BOOTSTRAPS, "delta_target": DELTA_TARGET, "permutation_p_max": P_MAX, "bootstrap_upper_max": BOOTSTRAP_UPPER_MAX, "max_lineage_delta": MAX_LINEAGE_DELTA}:
            raise ValueError("manifest inference contract drift")
        if manifest["claim_contract"] != {"analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False}:
            raise ValueError("manifest claim contract drift")
        census = Path(manifest["candidate_census"]["path"])
        receipt = Path(manifest["design_receipt"]["path"])
        if sha256(census) != manifest["candidate_census"]["sha256"]:
            raise ValueError("candidate census SHA-256 drift")
        if sha256(receipt) != manifest["design_receipt"]["sha256"]:
            raise ValueError("design receipt SHA-256 drift")
        if normalized_receipt_sha256(receipt, "receipt_sha256") != EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256:
            raise ValueError("design receipt normalized digest drift")
        boundary = manifest["implementation_boundary"]
        if boundary["implementation_module"] != EXPECTED_MODULE_PATH:
            raise ValueError("implementation module path drift")
        for commit in (boundary["required_base_commit"], boundary["implementation_commit"]):
            if git_command("rev-parse", "--verify", f"{commit}^{{commit}}").returncode != 0:
                raise ValueError(f"unresolvable implementation commit: {commit}")
            if git_command("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
                raise ValueError(f"implementation commit is not an ancestor: {commit}")
        modules = boundary["modules"]
        if len(modules) != 1 or modules[0]["path"] != EXPECTED_MODULE_PATH:
            raise ValueError("transitive implementation module contract drift")
        if sha256(Path(EXPECTED_MODULE_PATH)) != modules[0]["sha256"] or git_blob_sha256(boundary["implementation_commit"], EXPECTED_MODULE_PATH) != modules[0]["sha256"]:
            raise ValueError("implementation module SHA-256 drift")
        if sha256(Path("uv.lock")) != manifest["uv_lock_sha256"]:
            raise ValueError("uv.lock SHA-256 drift")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise T0Stop("T0_IMPLEMENTATION_BOUNDARY", False, str(exc)) from exc
    return manifest


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
            if not model_id or model_id in lineages:
                raise IntegrityError(f"invalid ModelID: {model_id}")
            lineages[model_id] = row["OncotreeLineage"].strip()
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
            screen_id, model_id = row["ScreenID"].strip(), row["ModelID"].strip()
            if not screen_id or screen_id in mapping or not model_id:
                raise IntegrityError(f"invalid screen identity: {screen_id}")
            mapping[screen_id] = model_id
    return mapping, actual


def load_status_matrix(path: Path, model_ids: set[str]) -> tuple[dict[str, int], str]:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["damaging"]:
        raise IntegrityError(f"damaging matrix SHA-256 drift: {actual}")
    statuses: dict[str, int] = {}
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or not header or header[0] != "" or header.count(STATUS_COLUMN) != 1:
            raise IntegrityError("TP53 matrix header drift")
        index = header.index(STATUS_COLUMN)
        for row in reader:
            if not row:
                continue
            model_id = row[0].strip()
            if not model_id or model_id in seen:
                raise IntegrityError(f"duplicate matrix ModelID: {model_id}")
            seen.add(model_id)
            if model_id in model_ids:
                if index >= len(row):
                    raise IntegrityError(f"short matrix row: {model_id}")
                statuses[model_id] = parse_matrix_value(row[index], (model_id, STATUS_COLUMN))
    if set(statuses) != model_ids:
        raise IntegrityError(f"TP53 matrix coverage drift: expected {len(model_ids)}, got {len(statuses)}")
    return statuses, actual


def canonical_roster(contexts: Sequence[Context]) -> str:
    rows = [
        {"source": c.source, "model_id": c.model_id, "lineage": c.lineage, "screen_ids": list(c.screen_ids), "matrix_value": c.matrix_value, "status": c.status}
        for c in sorted(contexts, key=lambda c: (c.source, c.model_id))
    ]
    return "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows)


def load_context(qc_path: Path, screen_map_path: Path, model_path: Path, damaging_path: Path) -> tuple[list[Context], dict[str, object]]:
    lineages, model_hash = load_model_lineages(model_path)
    screen_map, map_hash = load_screen_map(screen_map_path)
    qc_hash = sha256(qc_path)
    if qc_hash != EXPECTED_HASHES["screen_qc"]:
        raise IntegrityError(f"AchillesScreenQCReport.csv SHA-256 drift: {qc_hash}")
    eligible: list[EligibleScreen] = []
    seen_screens: set[str] = set()
    with qc_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"ScreenID", "ModelID", "Library", "PassesQC", "CanInclude"}
        if not required.issubset(reader.fieldnames or set()):
            raise IntegrityError("screen QC header drift")
        for row in reader:
            source = row["Library"].strip()
            if source not in SOURCES or row["PassesQC"].strip() != "True" or row["CanInclude"].strip() != "True":
                continue
            screen_id, model_id = row["ScreenID"].strip(), row["ModelID"].strip()
            if screen_id in seen_screens or model_id not in lineages or not lineages[model_id] or screen_map.get(screen_id) != model_id:
                raise IntegrityError(f"invalid eligible identity: {screen_id}/{model_id}")
            seen_screens.add(screen_id)
            eligible.append(EligibleScreen(screen_id, model_id, source, lineages[model_id]))
    by_model: dict[tuple[str, str], list[EligibleScreen]] = defaultdict(list)
    for screen in eligible:
        by_model[(screen.source, screen.model_id)].append(screen)
    model_ids = {screen.model_id for screen in eligible}
    statuses, matrix_hash = load_status_matrix(damaging_path, model_ids)
    contexts = []
    for (source, model_id), screens in sorted(by_model.items()):
        value = statuses[model_id]
        contexts.append(Context(source, model_id, screens[0].lineage, tuple(sorted(s.screen_id for s in screens)), EXPOSED if value == 0 else REFERENCE, value))
    counts = {source: sum(c.source == source for c in contexts) for source in SOURCES}
    if counts != EXPECTED_SOURCE_MODELS:
        raise IntegrityError(f"eligible source/model count drift: {counts}")
    for source in SOURCES:
        selected = [c for c in contexts if c.source == source]
        status_counts = {status: sum(c.status == status for c in selected) for status in (EXPOSED, REFERENCE)}
        mixed = sum(any(c.lineage == lineage and c.status == EXPOSED for c in selected) and any(c.lineage == lineage and c.status == REFERENCE for c in selected) for lineage in {c.lineage for c in selected})
        if status_counts != EXPECTED_STATUS_COUNTS[source] or mixed != EXPECTED_MIXED_LINEAGES[source]:
            raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"frozen context drift for {source}: {status_counts}, mixed={mixed}")
        if status_counts[EXPOSED] < MIN_EXPOSED or status_counts[REFERENCE] < MIN_REFERENCE or mixed < MIN_MIXED_LINEAGES:
            raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"context adequacy failure: {source}")
    roster_hash = hashlib.sha256(canonical_roster(contexts).encode()).hexdigest()
    if roster_hash != EXPECTED_ROSTER_SHA256:
        raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"canonical roster hash drift: {roster_hash}")
    return contexts, {"screen_qc_sha256": qc_hash, "screen_map_sha256": map_hash, "model_sha256": model_hash, "damaging_sha256": matrix_hash, "eligible_screens": len(eligible), "eligible_source_models": counts, "unique_model_ids": len(model_ids), "status_column": STATUS_COLUMN, "status_threshold": 1, "canonical_roster_sha256": roster_hash, "status_counts": EXPECTED_STATUS_COUNTS, "mixed_lineages": EXPECTED_MIXED_LINEAGES}


def write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    fields = ["source", "model_id", "lineage", "eligible_screen_ids", "TP53_matrix_value", "TP53_status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for c in contexts:
            writer.writerow({"source": c.source, "model_id": c.model_id, "lineage": c.lineage, "eligible_screen_ids": ";".join(c.screen_ids), "TP53_matrix_value": c.matrix_value, "TP53_status": c.status})


def grouped_contexts(contexts: Sequence[Context], source: str) -> dict[str, dict[str, list[str]]]:
    groups: dict[str, dict[str, list[str]]] = defaultdict(lambda: {EXPOSED: [], REFERENCE: []})
    for c in sorted((c for c in contexts if c.source == source), key=lambda c: (c.lineage, c.status, c.model_id)):
        groups[c.lineage][c.status].append(c.model_id)
    return {lineage: {status: sorted(ids) for status, ids in groups[lineage].items()} for lineage in sorted(groups)}


def delta_from_scores(groups: dict[str, dict[str, list[str]]], scores: dict[str, float]) -> tuple[float, dict[str, float], int]:
    numerator = 0.0
    denominator = 0
    lineage_deltas: dict[str, float] = {}
    for lineage in sorted(groups):
        exposed = np.asarray([scores[mid] for mid in groups[lineage][EXPOSED]], dtype=float)
        reference = np.sort(np.asarray([scores[mid] for mid in groups[lineage][REFERENCE]], dtype=float))
        if len(exposed) == 0 or len(reference) == 0:
            continue
        greater = np.searchsorted(reference, exposed, side="left").sum()
        less = (len(reference) - np.searchsorted(reference, exposed, side="right")).sum()
        lineage_num = float(greater - less)
        lineage_den = len(exposed) * len(reference)
        lineage_deltas[lineage] = lineage_num / lineage_den
        numerator += lineage_num
        denominator += lineage_den
    if denominator == 0:
        raise IntegrityError("zero pair denominator")
    return numerator / denominator, lineage_deltas, denominator


def permutation_deltas(groups: dict[str, dict[str, list[str]]], scores: dict[str, float], repeats: int, rng: np.random.Generator) -> np.ndarray:
    prepared = []
    denominator = 0
    for lineage in sorted(groups):
        exposed, reference = groups[lineage][EXPOSED], groups[lineage][REFERENCE]
        if not exposed or not reference:
            continue
        ranks = rankdata(np.asarray([scores[mid] for mid in exposed + reference]), method="average")
        k, m = len(exposed), len(reference)
        prepared.append((ranks, k, m))
        denominator += k * m
    if denominator == 0:
        raise IntegrityError("zero permutation denominator")
    result = np.empty(repeats)
    generated = 0
    while generated < repeats:
        batch = min(1000, repeats - generated)
        numerator = np.zeros(batch)
        for ranks, k, m in prepared:
            choices = np.argpartition(rng.random((batch, len(ranks))), k - 1, axis=1)[:, :k]
            u = ranks[choices].sum(axis=1) - k * (k + 1) / 2
            numerator += 2 * u - k * m
        result[generated:generated + batch] = numerator / denominator
        generated += batch
    return result


def bootstrap_deltas(groups: dict[str, dict[str, list[str]]], scores: dict[str, float], repeats: int, rng: np.random.Generator) -> np.ndarray:
    result = np.empty(repeats)
    for repeat in range(repeats):
        sampled: dict[str, dict[str, list[str]]] = {}
        for lineage in sorted(groups):
            sampled[lineage] = {status: list(rng.choice(groups[lineage][status], size=len(groups[lineage][status]), replace=True)) for status in (EXPOSED, REFERENCE)}
        numerator = 0.0
        denominator = 0
        for lineage in sorted(sampled):
            exposed = np.sort(np.asarray([scores[mid] for mid in sampled[lineage][EXPOSED]], dtype=float))
            reference = np.sort(np.asarray([scores[mid] for mid in sampled[lineage][REFERENCE]], dtype=float))
            greater = np.searchsorted(reference, exposed, side="left").sum()
            less = (len(reference) - np.searchsorted(reference, exposed, side="right")).sum()
            numerator += float(greater - less)
            denominator += len(exposed) * len(reference)
        result[repeat] = numerator / denominator
    return result


def ordered_ids(groups: dict[str, dict[str, list[str]]]) -> list[str]:
    return [mid for lineage in sorted(groups) for status in (EXPOSED, REFERENCE) for mid in groups[lineage][status]]


def design_sensitivity(contexts: Sequence[Context], source: str, rng: np.random.Generator) -> dict[str, object]:
    groups = grouped_contexts(contexts, source)
    ids = ordered_ids(groups)
    null = permutation_deltas(groups, {mid: float(rng.normal()) for mid in ids}, PERMUTATIONS, rng)
    critical = float(np.quantile(null, 0.05, method="linear"))
    hits = 0
    for _ in range(DESIGN_SIMULATIONS):
        scores = {mid: float(rng.normal(loc=NORMAL_MEAN_SHIFT if status == EXPOSED else 0.0)) for lineage in sorted(groups) for status in (EXPOSED, REFERENCE) for mid in groups[lineage][status]}
        hits += delta_from_scores(groups, scores)[0] <= critical
    power = hits / DESIGN_SIMULATIONS
    return {"pair_id": PAIR_ID, "source": source, "exposed_models": sum(len(groups[l][EXPOSED]) for l in groups), "reference_models": sum(len(groups[l][REFERENCE]) for l in groups), "contributing_lineages": sum(bool(groups[l][EXPOSED]) and bool(groups[l][REFERENCE]) for l in groups), "expected_delta": DELTA_TARGET, "normal_mean_shift": NORMAL_MEAN_SHIFT, "null_permutations": PERMUTATIONS, "alternative_simulations": DESIGN_SIMULATIONS, "critical_delta": critical, "simulated_power": power, "confirmatory_power_adequate": power >= MIN_CONFIRMATORY_POWER}


def write_design_rows(path: Path, rows: Sequence[dict[str, object]]) -> None:
    fields = ["pair_id", "source", "exposed_models", "reference_models", "contributing_lineages", "expected_delta", "normal_mean_shift", "null_permutations", "alternative_simulations", "critical_delta", "simulated_power", "confirmatory_power_adequate"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def verify_endpoint_hash(path: Path) -> None:
    actual = sha256(path)
    if actual != EXPECTED_HASHES["endpoint"]:
        raise T0Stop("T0_INPUT_HASH", False, f"endpoint SHA-256 drift: {actual}")


def load_endpoint(path: Path, contexts: Sequence[Context]) -> tuple[dict[tuple[str, str], float], dict[str, object]]:
    verify_endpoint_hash(path)
    screen_to_context = {screen_id: c for c in contexts for screen_id in c.screen_ids}
    values: dict[tuple[str, str], list[float]] = defaultdict(list)
    seen_screens: set[str] = set()
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.reader(handle)
            header = next(reader, None)
            if header is None or not header or header[0] != "" or header.count(TARGET_COLUMN) != 1:
                raise T0Stop("T0_SCHEMA_HEADER", False, f"missing/duplicate endpoint column: {TARGET_COLUMN}")
            index = header.index(TARGET_COLUMN)
            for row in reader:
                if not row:
                    continue
                screen_id = row[0].strip()
                if screen_id not in screen_to_context:
                    continue
                if screen_id in seen_screens:
                    raise T0Stop("T0_ENDPOINT_COMPLETENESS", True, f"duplicate endpoint ScreenID: {screen_id}")
                seen_screens.add(screen_id)
                if index >= len(row) or not row[index].strip():
                    continue
                c = screen_to_context[screen_id]
                values[(c.source, c.model_id)].append(parse_float(row[index], (screen_id, TARGET_COLUMN)))
    except T0Stop:
        raise
    except (OSError, ValueError, IntegrityError) as exc:
        raise T0Stop("T0_ENDPOINT_COMPLETENESS", True, str(exc)) from exc
    scores: dict[tuple[str, str], float] = {}
    missing = []
    for c in contexts:
        key = (c.source, c.model_id)
        if not values[key]:
            missing.append(key)
        else:
            scores[key] = float(median(values[key]))
    if missing:
        raise T0Stop("T0_ENDPOINT_COMPLETENESS", True, f"missing endpoint values: {len(missing)}")
    return scores, {"sha256": EXPECTED_HASHES["endpoint"], "eligible_screens_seen": len(seen_screens), "eligible_screens_expected": len(screen_to_context), "model_values": len(scores), "median_collapse": True}


def classify_context_stop(error: IntegrityError) -> str:
    message = str(error).lower()
    if "sha-256" in message:
        return "T0_INPUT_HASH"
    if "matrix" in message and ("coverage" in message or "domain" in message or "duplicate" in message or "short" in message):
        return "T0_MATRIX_COVERAGE"
    if "header" in message or "column" in message:
        return "T0_SCHEMA_HEADER"
    return "T0_IDENTITY_JOIN"


def write_endpoint_rows(path: Path, contexts: Sequence[Context], scores: dict[tuple[str, str], float]) -> None:
    fields = ["pair_id", "source", "model_id", "lineage", "status", "target_score"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        for c in contexts:
            pass
        writer.writeheader()
        for c in contexts:
            writer.writerow({"pair_id": PAIR_ID, "source": c.source, "model_id": c.model_id, "lineage": c.lineage, "status": c.status, "target_score": scores[(c.source, c.model_id)]})


def inference_for(contexts: Sequence[Context], scores: dict[tuple[str, str], float], source: str, rng: np.random.Generator) -> dict[str, object]:
    groups = grouped_contexts(contexts, source)
    source_scores = {mid: scores[(source, mid)] for mid in ordered_ids(groups)}
    delta, lineage_deltas, pair_count = delta_from_scores(groups, source_scores)
    permutation = permutation_deltas(groups, source_scores, PERMUTATIONS, rng)
    extreme = int(np.count_nonzero(permutation <= delta))
    p_value = (1 + extreme) / (PERMUTATIONS + 1)
    bootstrap = bootstrap_deltas(groups, source_scores, BOOTSTRAPS, rng)
    ci_low, ci_high = np.quantile(bootstrap, [0.025, 0.975], method="linear")
    gates = {"delta_lt_0": delta < 0, "delta_le_minus_0_20": delta <= DELTA_TARGET, "permutation_p_le_0_05": p_value <= P_MAX, "bootstrap_upper_lt_0": float(ci_high) < BOOTSTRAP_UPPER_MAX, "at_least_5_negative_lineages": sum(v < 0 for v in lineage_deltas.values()) >= MIN_MIXED_LINEAGES, "no_lineage_delta_gt_plus_0_20": max(lineage_deltas.values()) <= MAX_LINEAGE_DELTA}
    return {"pair_id": PAIR_ID, "source": source, "delta": delta, "pair_count": pair_count, "lineage_deltas": lineage_deltas, "permutation_repeats": PERMUTATIONS, "permutation_extreme_count": extreme, "permutation_p_one_sided_lower": p_value, "bootstrap_repeats": BOOTSTRAPS, "bootstrap_ci_95_percentile": [float(ci_low), float(ci_high)], "gates": gates, "pass": all(gates.values())}


def write_inference(path: Path, results: Sequence[dict[str, object]]) -> None:
    fields = ["pair_id", "source", "primary_confirmatory", "delta", "pair_count", "permutation_extreme_count", "permutation_p_one_sided_lower", "bootstrap_ci_low", "bootstrap_ci_high", "pass", "gates_json", "lineage_deltas_json"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for result in results:
            interval = result["bootstrap_ci_95_percentile"]
            writer.writerow({"pair_id": PAIR_ID, "source": result["source"], "primary_confirmatory": False, "delta": result["delta"], "pair_count": result["pair_count"], "permutation_extreme_count": result["permutation_extreme_count"], "permutation_p_one_sided_lower": result["permutation_p_one_sided_lower"], "bootstrap_ci_low": interval[0], "bootstrap_ci_high": interval[1], "pass": result["pass"], "gates_json": json.dumps(result["gates"], sort_keys=True), "lineage_deltas_json": json.dumps(result["lineage_deltas"], sort_keys=True)})


def summary_digest(result: dict[str, object]) -> str:
    payload = json.loads(json.dumps(result))
    payload["artifact_receipt_sha256"]["summary.json"] = ""
    return hashlib.sha256((json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()).hexdigest()


def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    manifest = verify_implementation_boundary(Path(args.manifest_file))
    verify_endpoint_hash(Path(args.endpoint_file))
    try:
        contexts, context_receipt = load_context(Path(args.qc_file), Path(args.screen_map_file), Path(args.model_file), Path(args.damaging_file))
    except T0Stop:
        raise
    except IntegrityError as exc:
        raise T0Stop(classify_context_stop(exc), False, str(exc)) from exc
    write_context_ledger(stage / "context_ledger.csv", contexts)
    context_receipt["context_ledger_sha256"] = sha256(stage / "context_ledger.csv")
    design_rows = [design_sensitivity(contexts, source, np.random.default_rng(DESIGN_SEEDS[source])) for source in SOURCES]
    write_design_rows(stage / "design_sensitivity.csv", design_rows)
    for row in design_rows:
        expected = manifest["design_sensitivity"]["expected_power"][row["source"]]
        if row["simulated_power"] != expected:
            raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"design power drift: {row['source']}")
    design_receipt = {"design_sensitivity_sha256": sha256(stage / "design_sensitivity.csv"), "minimum_confirmatory_power": MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY", "confirmatory_claim_enabled": False, "all_primary_sources_power_adequate": all(row["confirmatory_power_adequate"] for row in design_rows)}
    pre_payload = {"experiment_id": EXPERIMENT_ID, "context_ledger_sha256": context_receipt["context_ledger_sha256"], "design_sensitivity_sha256": design_receipt["design_sensitivity_sha256"]}
    pre_receipt = {**pre_payload, "receipt_sha256": hashlib.sha256((json.dumps(pre_payload, sort_keys=True) + "\n").encode()).hexdigest(), "sealed_before_endpoint": True}
    write_json_atomic(Path(args.pre_endpoint_receipt), pre_receipt)
    scores, endpoint_receipt = load_endpoint(Path(args.endpoint_file), contexts)
    write_endpoint_rows(stage / "endpoint_scores.csv", contexts, scores)
    results = [inference_for(contexts, scores, source, np.random.default_rng(INFERENCE_SEEDS[source])) for source in SOURCES]
    write_inference(stage / "inference.csv", results)
    nominal_pass = all(result["pass"] for result in results)
    result = {"experiment_id": EXPERIMENT_ID, "status": "FEASIBILITY_ONLY_NOMINAL_GATES_PASS" if nominal_pass else "FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE", "analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "analysis_type": "preregistered_source_specific_lineage_stratified_tp53_mdm2_replication", "claim_eligibility": {"primary_confirmatory": False, "design_sensitivity_label": "FEASIBILITY_ONLY", "nominal_primary_gates_pass": nominal_pass}, "context_receipt": context_receipt, "design_sensitivity": design_receipt, "pre_endpoint_receipt": pre_receipt, "endpoint_receipt": endpoint_receipt, "primary": results, "inference_receipt": {"design_seeds": DESIGN_SEEDS, "inference_seeds": INFERENCE_SEEDS, "permutations": PERMUTATIONS, "bootstraps": BOOTSTRAPS, "bootstrap_interval": "percentile_95_linear_quantile", "unit": "collapsed_source_model_id", "cross_source_raw_score_comparison": False}, "implementation_receipt": {"manifest_path": args.manifest_file, "required_base_commit": manifest["implementation_boundary"]["required_base_commit"], "implementation_commit": manifest["implementation_boundary"]["implementation_commit"], "implementation_module": manifest["implementation_boundary"]["implementation_module"], "uv_lock_sha256": manifest["uv_lock_sha256"]}, "artifact_receipt_sha256": {name: sha256(stage / name) for name in ("context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv")} | {"summary.json": ""}, "overall_pass": False, "claim_boundary": "matrix-defined TP53 matrix-intact status association with source-specific MDM2 dependency in frozen 23Q4 cell-line screen cohorts; no functional-wild-type, biological-independence, clinical, or treatment claim"}
    return result


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {p.name for p in stage.iterdir() if p.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP017 staged file set drift")
    for filename, expected_rows in (("context_ledger.csv", 1290), ("endpoint_scores.csv", 1290)):
        with (stage / filename).open(newline="", encoding="utf-8") as handle:
            if len(list(csv.DictReader(handle))) != expected_rows:
                raise IntegrityError(f"{filename} row count drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        if len(list(csv.DictReader(handle))) != 2:
            raise IntegrityError("design receipt row drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        if len(rows) != 2 or any(row["primary_confirmatory"] != "False" for row in rows):
            raise IntegrityError("inference claim drift")
    expected_keys = {"experiment_id", "status", "analysis_label", "confirmatory_claim", "analysis_type", "claim_eligibility", "context_receipt", "design_sensitivity", "pre_endpoint_receipt", "endpoint_receipt", "primary", "inference_receipt", "implementation_receipt", "artifact_receipt_sha256", "overall_pass", "claim_boundary"}
    if set(result) != expected_keys or result["experiment_id"] != EXPERIMENT_ID or result["analysis_label"] != "FEASIBILITY_ONLY" or result["confirmatory_claim"] is not False or result["overall_pass"] is not False:
        raise IntegrityError("terminal claim contract drift")
    if result["artifact_receipt_sha256"]["summary.json"] != summary_digest(result):
        raise IntegrityError("summary digest drift")
    for filename in EXPECTED_RESULT_FILES - {"summary.json"}:
        if result["artifact_receipt_sha256"][filename] != sha256(stage / filename):
            raise IntegrityError(f"artifact hash drift: {filename}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--screen-map-file", default="data/raw/depmap/23q4/CRISPRScreenMap.csv")
    parser.add_argument("--model-file", default="data/raw/depmap/23q4/Model.csv")
    parser.add_argument("--damaging-file", default="data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv")
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-017/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-017/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-017/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-017/pre_endpoint_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target = Path(args.results_dir)
    error = Path(args.error_receipt)
    if target.exists():
        write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False})
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
                write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": exc.status, "analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False, "error": str(exc), "error_type": type(exc).__name__, "t0": True, "endpoint_opened": exc.endpoint_opened, "results_written": False, "preserved_path": preserved_path})
                return 2
            result["artifact_receipt_sha256"]["summary.json"] = summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            os.replace(stage, target)
    except Exception as exc:
        write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
