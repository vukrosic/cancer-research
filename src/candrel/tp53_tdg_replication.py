"""Bounded TP53-proxy to TDG dependency transport audit."""

from __future__ import annotations

import argparse
import csv
import json
import os
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Sequence

import numpy as np

from . import arid1a_atr_replication as base


EXPERIMENT_ID = "EXP-20260822-034"
PAIR_ID = "TP53_damaging_to_TDG"
STATUS_COLUMN = "TP53 (7157)"
TARGET_COLUMN = "TDG (6996)"
SOURCES = ("Avana", "KY")
ANALYSIS_EXPOSED = "damaging"
ANALYSIS_REFERENCE = "matrix_intact"
EXPECTED_MODULE_PATH = "src/candrel/tp53_tdg_replication.py"
BASE_MODULE_PATH = "src/candrel/arid1a_atr_replication.py"
ENGINE_MODULE_PATH = "src/candrel/tp53_mdm2_replication.py"
PROJECT_PATH = "pyproject.toml"
REQUIRED_BASE_COMMIT = "7a37a23"
EXPECTED_HASHES = base.EXPECTED_HASHES.copy()
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_STATUS_COUNTS = {"Avana": {"damaging": 610, "matrix_intact": 365}, "KY": {"damaging": 233, "matrix_intact": 82}}
EXPECTED_MIXED_LINEAGES = {"Avana": 25, "KY": 16}
DESIGN_SEEDS = {"Avana": 20263400, "KY": 20263500}
INFERENCE_SEEDS = {"Avana": 20273400, "KY": 20273500}
EXPECTED_ROSTER_SHA256 = "61060e6ef0c24ad1bb3acc2fbe75e9ad5f8908df505d20290cbab2189557b376"
EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = "6da1920e91e3e48ef9195e0e257f8eca25e0e6cfba6d359108b1597fb87c7edc"
EXPECTED_RESULT_FILES = {"context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv", "summary.json"}

IntegrityError = base.IntegrityError
T0Stop = base.T0Stop
Context = base.Context
engine = base.engine

_BASE_KEYS = ("EXPERIMENT_ID", "PAIR_ID", "STATUS_COLUMN", "TARGET_COLUMN", "EXPECTED_HASHES", "EXPECTED_SOURCE_MODELS", "EXPECTED_STATUS_COUNTS", "EXPECTED_MIXED_LINEAGES", "DESIGN_SEEDS", "INFERENCE_SEEDS", "EXPOSED", "REFERENCE", "MIN_EXPOSED", "MIN_REFERENCE", "EXPECTED_ROSTER_SHA256", "EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256", "EXPECTED_MODULE_PATH", "ENGINE_MODULE_PATH", "PROJECT_PATH", "REQUIRED_BASE_COMMIT")


def _configure_base() -> None:
    base.EXPERIMENT_ID = EXPERIMENT_ID
    base.PAIR_ID = PAIR_ID
    base.STATUS_COLUMN = STATUS_COLUMN
    base.TARGET_COLUMN = TARGET_COLUMN
    base.EXPECTED_HASHES = EXPECTED_HASHES.copy()
    base.EXPECTED_SOURCE_MODELS = EXPECTED_SOURCE_MODELS.copy()
    base.EXPECTED_STATUS_COUNTS = {source: counts.copy() for source, counts in EXPECTED_STATUS_COUNTS.items()}
    base.EXPECTED_MIXED_LINEAGES = EXPECTED_MIXED_LINEAGES.copy()
    base.DESIGN_SEEDS = DESIGN_SEEDS.copy()
    base.INFERENCE_SEEDS = INFERENCE_SEEDS.copy()
    base.EXPOSED = "damaging"
    base.REFERENCE = "matrix_intact"
    base.MIN_EXPOSED = 20
    base.MIN_REFERENCE = 50
    base.EXPECTED_ROSTER_SHA256 = EXPECTED_ROSTER_SHA256


@contextmanager
def _base_configured():
    saved = {key: getattr(base, key) for key in _BASE_KEYS if hasattr(base, key)}
    created = [key for key in _BASE_KEYS if not hasattr(base, key)]
    _configure_base()
    try:
        yield
    finally:
        for key, value in saved.items():
            setattr(base, key, value)
        for key in created:
            if hasattr(base, key):
                delattr(base, key)


def sha256(path: Path) -> str:
    return engine.sha256(path)


def normalized_receipt_sha256(path: Path, field: str) -> str:
    return engine.normalized_receipt_sha256(path, field)


def git_command(*arguments: str):
    return engine.git_command(*arguments)


def git_blob_sha256(commit: str, path: str) -> str:
    return engine.git_blob_sha256(commit, path)


def verify_implementation_boundary(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["experiment_id"] != EXPERIMENT_ID or manifest["entrypoint"] != ".venv/bin/python -m candrel.tp53_tdg_replication":
            raise ValueError("manifest identity/entrypoint drift")
        expected_inputs = {
            "endpoint": {"path": "data/raw/depmap/23q4/ScreenNaiveGeneScore.csv", "sha256": EXPECTED_HASHES["endpoint"], "target_column": TARGET_COLUMN},
            "screen_qc": {"path": "data/raw/depmap/23q4/AchillesScreenQCReport.csv", "sha256": EXPECTED_HASHES["screen_qc"]},
            "screen_map": {"path": "data/raw/depmap/23q4/CRISPRScreenMap.csv", "sha256": EXPECTED_HASHES["screen_map"]},
            "model": {"path": "data/raw/depmap/23q4/Model.csv", "sha256": EXPECTED_HASHES["model"]},
            "damaging_matrix": {"path": "data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv", "sha256": EXPECTED_HASHES["damaging"], "status_columns": [STATUS_COLUMN]},
        }
        expected_eligibility = {"libraries": list(SOURCES), "pass_qc": True, "can_include": True, "expected_source_models": EXPECTED_SOURCE_MODELS}
        expected_status = {"exposed": "damaging", "reference": "matrix_intact", "status_columns": [STATUS_COLUMN], "exposed_matrix_values": [1], "reference_matrix_values": [0], "expected_counts": EXPECTED_STATUS_COUNTS, "expected_mixed_lineages": EXPECTED_MIXED_LINEAGES}
        if manifest["inputs"] != expected_inputs or manifest["eligibility"] != expected_eligibility or manifest["status_contract"] != expected_status:
            raise ValueError("manifest input/status contract drift")
        census = Path(manifest["candidate_census"]["path"]); receipt = Path(manifest["design_receipt"]["path"]); seal = Path(manifest["selection_seal"]["path"])
        if sha256(census) != manifest["candidate_census"]["sha256"] or sha256(receipt) != manifest["design_receipt"]["sha256"] or sha256(seal) != manifest["selection_seal"]["sha256"]:
            raise ValueError("selection/census/design receipt SHA-256 drift")
        if manifest["candidate_census"]["canonical_roster_sha256"] != EXPECTED_ROSTER_SHA256 or manifest["design_receipt"]["canonical_roster_sha256"] != EXPECTED_ROSTER_SHA256:
            raise ValueError("canonical roster binding drift")
        if normalized_receipt_sha256(receipt, "receipt_sha256") != EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256:
            raise ValueError("design receipt normalized digest drift")
        if manifest["selection_seal"]["sealed_before_endpoint_access"] is not True or manifest["selection_seal"]["protocol_commit"] != REQUIRED_BASE_COMMIT:
            raise ValueError("selection seal contract drift")
        expected_design = {"mean_shift": engine.NORMAL_MEAN_SHIFT, "null_permutations": engine.PERMUTATIONS, "alternative_simulations": engine.DESIGN_SIMULATIONS, "planning_power_seeds": DESIGN_SEEDS, "expected_critical_delta": {"Avana": -0.07838479809976247, "KY": -0.14327062228654125}, "expected_power": {"Avana": 0.9951, "KY": 0.7617}, "minimum_power_for_confirmatory_label": engine.MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY"}
        if manifest["design_sensitivity"] != expected_design:
            raise ValueError("manifest design contract drift")
        expected_inference = {"inference_seeds": INFERENCE_SEEDS, "permutations": engine.PERMUTATIONS, "bootstraps": engine.BOOTSTRAPS, "delta_target": engine.DELTA_TARGET, "permutation_p_max": engine.P_MAX, "bootstrap_upper_max": engine.BOOTSTRAP_UPPER_MAX, "max_lineage_delta": engine.MAX_LINEAGE_DELTA}
        if manifest["inference"] != expected_inference or manifest["claim_contract"] != {"analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False}:
            raise ValueError("manifest inference/claim contract drift")
        if sha256(Path("uv.lock")) != manifest["uv_lock_sha256"]:
            raise ValueError("uv.lock SHA-256 drift")
        boundary = manifest["implementation_boundary"]
        if boundary["required_base_commit"] != REQUIRED_BASE_COMMIT or boundary["implementation_module"] != EXPECTED_MODULE_PATH or boundary["engine_module"] != ENGINE_MODULE_PATH or boundary["project_file"] != PROJECT_PATH:
            raise ValueError("implementation boundary path/base drift")
        for commit in (boundary["required_base_commit"], boundary["implementation_commit"]):
            if git_command("rev-parse", "--verify", f"{commit}^{{commit}}").returncode != 0 or git_command("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
                raise ValueError(f"unresolvable/non-ancestor commit: {commit}")
        if {item["path"] for item in boundary["modules"]} != {EXPECTED_MODULE_PATH, BASE_MODULE_PATH, ENGINE_MODULE_PATH, PROJECT_PATH}:
            raise ValueError("transitive module set drift")
        for item in boundary["modules"]:
            if sha256(Path(item["path"])) != item["sha256"] or git_blob_sha256(boundary["implementation_commit"], item["path"]) != item["sha256"]:
                raise ValueError(f"implementation module hash drift: {item['path']}")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise T0Stop("T0_IMPLEMENTATION_BOUNDARY", False, str(exc)) from exc
    return manifest


def load_context(qc_path: Path, screen_map_path: Path, model_path: Path, damaging_path: Path):
    with _base_configured():
        return base.load_context(qc_path, screen_map_path, model_path, damaging_path)


def grouped_contexts(contexts: Sequence[Context], source: str):
    with _base_configured():
        return base.grouped_contexts(contexts, source)


def design_sensitivity(contexts: Sequence[Context], source: str, rng: np.random.Generator):
    with _base_configured():
        return base.design_sensitivity(contexts, source, rng)


def inference_for(contexts: Sequence[Context], scores: dict[tuple[str, str], float], source: str, rng: np.random.Generator):
    with _base_configured():
        return base.inference_for(contexts, scores, source, rng)


def verify_endpoint_hash(path: Path) -> None:
    with _base_configured():
        return base.verify_endpoint_hash(path)


def load_endpoint(path: Path, contexts: Sequence[Context]):
    with _base_configured():
        return base.load_endpoint(path, contexts)


def write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    fields = ["source", "model_id", "lineage", "eligible_screen_ids", "TP53_matrix_value", "TP53_status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for context in contexts:
            writer.writerow({"source": context.source, "model_id": context.model_id, "lineage": context.lineage, "eligible_screen_ids": ";".join(context.screen_ids), "TP53_matrix_value": context.matrix_value, "TP53_status": context.status})


def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    saved = {key: getattr(base, key) for key in _BASE_KEYS if hasattr(base, key)}
    created = [key for key in _BASE_KEYS if not hasattr(base, key)]
    saved_verify = base.verify_implementation_boundary
    saved_writer = base.write_context_ledger
    _configure_base()
    base.verify_implementation_boundary = verify_implementation_boundary
    base.write_context_ledger = write_context_ledger
    try:
        result = base.run(args, stage)
        result["analysis_type"] = "preregistered_source_specific_lineage_stratified_tp53_tdg_transport_replication"
        result["claim_boundary"] = "TP53 damaging-matrix proxy association with source-specific TDG dependency in frozen 23Q4 cell-line screen cohorts; no functional TP53-loss, TDG-inhibitor, DNA-repair, causal, pharmacologic, treatment, clinical, or confirmatory claim"
        return result
    finally:
        base.verify_implementation_boundary = saved_verify
        base.write_context_ledger = saved_writer
        for key, value in saved.items():
            setattr(base, key, value)
        for key in created:
            if hasattr(base, key):
                delattr(base, key)


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP034 staged file set drift")
    for filename in ("context_ledger.csv", "endpoint_scores.csv"):
        with (stage / filename).open(newline="", encoding="utf-8") as handle:
            if len(list(csv.DictReader(handle))) != 1290:
                raise IntegrityError(f"{filename} row count drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        if len(list(csv.DictReader(handle))) != 2:
            raise IntegrityError("design row drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
        if len(rows) != 2 or any(row["primary_confirmatory"] != "False" for row in rows):
            raise IntegrityError("inference claim drift")
    expected_keys = {"experiment_id", "status", "analysis_label", "confirmatory_claim", "analysis_type", "claim_eligibility", "context_receipt", "design_sensitivity", "pre_endpoint_receipt", "endpoint_receipt", "primary", "inference_receipt", "implementation_receipt", "artifact_receipt_sha256", "overall_pass", "claim_boundary"}
    if set(result) != expected_keys or result["experiment_id"] != EXPERIMENT_ID or result["analysis_label"] != "FEASIBILITY_ONLY" or result["confirmatory_claim"] is not False or result["overall_pass"] is not False:
        raise IntegrityError("terminal claim contract drift")
    if result["artifact_receipt_sha256"]["summary.json"] != engine.summary_digest(result):
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
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-034/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-034/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-034/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-034/pre_endpoint_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target, error = Path(args.results_dir), Path(args.error_receipt)
    if target.exists():
        engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False})
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
                    os.replace(stage, preserved); preserved_path = str(preserved)
                engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": exc.status, "analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False, "error": str(exc), "error_type": type(exc).__name__, "t0": True, "endpoint_opened": exc.endpoint_opened, "results_written": False, "preserved_path": preserved_path})
                return 2
            result["artifact_receipt_sha256"]["summary.json"] = engine.summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            os.replace(stage, target)
    except Exception as exc:
        engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
