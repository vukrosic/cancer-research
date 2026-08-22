"""Bounded SMAD4-proxy to AURKA dependency transport audit."""

from __future__ import annotations

import argparse
from functools import wraps
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence

import numpy as np

from . import smad4_brd4_replication as base


EXPERIMENT_ID = "EXP-20260822-032"
PAIR_ID = "SMAD4_damaging_to_AURKA"
STATUS_COLUMN = "SMAD4 (4089)"
TARGET_COLUMN = "AURKA (6790)"
SOURCES = ("Avana", "KY")
LOADER_EXPOSED = "matrix_intact"
LOADER_REFERENCE = "damaging"
ANALYSIS_EXPOSED = "damaging"
ANALYSIS_REFERENCE = "matrix_intact"
EXPECTED_MODULE_PATH = "src/candrel/smad4_aurka_replication.py"
BASE_MODULE_PATH = "src/candrel/smad4_brd4_replication.py"
ENGINE_MODULE_PATH = "src/candrel/tp53_mdm2_replication.py"
PROJECT_PATH = "pyproject.toml"
REQUIRED_BASE_COMMIT = "f248a25"
EXPECTED_HASHES = base.EXPECTED_HASHES.copy()
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_STATUS_COUNTS = {"Avana": {ANALYSIS_EXPOSED: 46, ANALYSIS_REFERENCE: 929}, "KY": {ANALYSIS_EXPOSED: 25, ANALYSIS_REFERENCE: 290}}
EXPECTED_MIXED_LINEAGES = {"Avana": 12, "KY": 6}
DESIGN_SEEDS = {"Avana": 20263200, "KY": 20263300}
INFERENCE_SEEDS = {"Avana": 20273200, "KY": 20273300}
EXPECTED_ROSTER_SHA256 = "3532122677a66a5fedbd664cb452d7dcd7ea6d179556ca4df1d1dbe4a81cef62"
EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = "88bb13dc586fe7777aedcb374817cfcb1f025d75b57507c60cf798ac72882ff8"
EXPECTED_RESULT_FILES = {"context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv", "summary.json"}

IntegrityError = base.IntegrityError
T0Stop = base.T0Stop
Context = base.Context

_BASE_CONFIGURATION_KEYS = (
    "EXPERIMENT_ID",
    "PAIR_ID",
    "STATUS_COLUMN",
    "TARGET_COLUMN",
    "EXPECTED_HASHES",
    "EXPECTED_SOURCE_MODELS",
    "EXPECTED_STATUS_COUNTS",
    "EXPECTED_MIXED_LINEAGES",
    "DESIGN_SEEDS",
    "INFERENCE_SEEDS",
    "EXPOSED",
    "REFERENCE",
    "MIN_EXPOSED",
    "MIN_REFERENCE",
    "EXPECTED_ROSTER_SHA256",
    "EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256",
)


def _preserve_base_globals(function):
    @wraps(function)
    def wrapped(*args, **kwargs):
        saved = {key: getattr(base, key) for key in _BASE_CONFIGURATION_KEYS if hasattr(base, key)}
        created = [key for key in _BASE_CONFIGURATION_KEYS if not hasattr(base, key)]
        try:
            return function(*args, **kwargs)
        finally:
            for key, value in saved.items():
                setattr(base, key, value)
            for key in created:
                if hasattr(base, key):
                    delattr(base, key)

    return wrapped


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
    base.EXPOSED = ANALYSIS_EXPOSED
    base.REFERENCE = ANALYSIS_REFERENCE
    base.MIN_EXPOSED = 20
    base.MIN_REFERENCE = 50
    base.EXPECTED_ROSTER_SHA256 = EXPECTED_ROSTER_SHA256
    base.EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256


def sha256(path: Path) -> str:
    return base.sha256(path)


def normalized_receipt_sha256(path: Path, field: str) -> str:
    return base.normalized_receipt_sha256(path, field)


def git_command(*arguments: str) -> subprocess.CompletedProcess[str]:
    return base.git_command(*arguments)


def git_blob_sha256(commit: str, path: str) -> str:
    return base.git_blob_sha256(commit, path)


@_preserve_base_globals
def verify_implementation_boundary(manifest_path: Path) -> dict[str, object]:
    _configure_base()
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["experiment_id"] != EXPERIMENT_ID or manifest["entrypoint"] != ".venv/bin/python -m candrel.smad4_aurka_replication":
            raise ValueError("manifest identity/entrypoint drift")
        expected_inputs = {
            "endpoint": {"path": "data/raw/depmap/23q4/ScreenNaiveGeneScore.csv", "sha256": EXPECTED_HASHES["endpoint"], "target_column": TARGET_COLUMN},
            "screen_qc": {"path": "data/raw/depmap/23q4/AchillesScreenQCReport.csv", "sha256": EXPECTED_HASHES["screen_qc"]},
            "screen_map": {"path": "data/raw/depmap/23q4/CRISPRScreenMap.csv", "sha256": EXPECTED_HASHES["screen_map"]},
            "model": {"path": "data/raw/depmap/23q4/Model.csv", "sha256": EXPECTED_HASHES["model"]},
            "damaging_matrix": {"path": "data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv", "sha256": EXPECTED_HASHES["damaging"], "status_columns": [STATUS_COLUMN]},
        }
        expected_eligibility = {"libraries": list(SOURCES), "pass_qc": True, "can_include": True, "expected_source_models": EXPECTED_SOURCE_MODELS}
        expected_status = {"exposed": ANALYSIS_EXPOSED, "reference": ANALYSIS_REFERENCE, "status_columns": [STATUS_COLUMN], "exposed_matrix_values": [1], "reference_matrix_values": [0], "expected_counts": EXPECTED_STATUS_COUNTS, "expected_mixed_lineages": EXPECTED_MIXED_LINEAGES}
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
        engine = base.engine
        expected_design = {"mean_shift": engine.NORMAL_MEAN_SHIFT, "null_permutations": engine.PERMUTATIONS, "alternative_simulations": engine.DESIGN_SIMULATIONS, "planning_power_seeds": DESIGN_SEEDS, "expected_critical_delta": {"Avana": -0.16595289079229122, "KY": -0.2147239263803681}, "expected_power": {"Avana": 0.6502, "KY": 0.4713}, "minimum_power_for_confirmatory_label": engine.MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY"}
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


@_preserve_base_globals
def load_context(qc_path: Path, screen_map_path: Path, model_path: Path, damaging_path: Path):
    _configure_base()
    return base.load_context(qc_path, screen_map_path, model_path, damaging_path)


@_preserve_base_globals
def grouped_contexts(contexts: Sequence[Context], source: str):
    _configure_base()
    return base.grouped_contexts(contexts, source)


@_preserve_base_globals
def design_sensitivity(contexts: Sequence[Context], source: str, rng: np.random.Generator):
    _configure_base()
    return base.design_sensitivity(contexts, source, rng)


@_preserve_base_globals
def inference_for(contexts: Sequence[Context], scores: dict[tuple[str, str], float], source: str, rng: np.random.Generator):
    _configure_base()
    return base.inference_for(contexts, scores, source, rng)


@_preserve_base_globals
def verify_endpoint_hash(path: Path) -> None:
    _configure_base()
    return base.verify_endpoint_hash(path)


@_preserve_base_globals
def load_endpoint(path: Path, contexts: Sequence[Context]):
    _configure_base()
    return base.load_endpoint(path, contexts)


@_preserve_base_globals
def write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    _configure_base()
    return base.write_context_ledger(path, contexts)


@_preserve_base_globals
def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    _configure_base()
    manifest = verify_implementation_boundary(Path(args.manifest_file))
    verify_endpoint_hash(Path(args.endpoint_file))
    try:
        contexts, context_receipt = load_context(Path(args.qc_file), Path(args.screen_map_file), Path(args.model_file), Path(args.damaging_file))
    except T0Stop:
        raise
    except IntegrityError as exc:
        raise T0Stop(base.engine.classify_context_stop(exc), False, str(exc)) from exc
    write_context_ledger(stage / "context_ledger.csv", contexts)
    context_receipt["context_ledger_sha256"] = sha256(stage / "context_ledger.csv")
    design_rows = [design_sensitivity(contexts, source, np.random.default_rng(DESIGN_SEEDS[source])) for source in SOURCES]
    with base._configured(ANALYSIS_EXPOSED, ANALYSIS_REFERENCE):
        base.engine.write_design_rows(stage / "design_sensitivity.csv", design_rows)
    for row in design_rows:
        if row["simulated_power"] != manifest["design_sensitivity"]["expected_power"][row["source"]]:
            raise T0Stop("T0_CONTEXT_ADEQUACY", False, f"design power drift: {row['source']}")
    design_receipt = {"design_sensitivity_sha256": sha256(stage / "design_sensitivity.csv"), "minimum_confirmatory_power": base.engine.MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY", "confirmatory_claim_enabled": False, "all_primary_sources_power_adequate": all(row["confirmatory_power_adequate"] for row in design_rows)}
    pre_payload = {"experiment_id": EXPERIMENT_ID, "context_ledger_sha256": context_receipt["context_ledger_sha256"], "design_sensitivity_sha256": design_receipt["design_sensitivity_sha256"]}
    pre_receipt = {**pre_payload, "receipt_sha256": hashlib.sha256((json.dumps(pre_payload, sort_keys=True) + "\n").encode()).hexdigest(), "sealed_before_endpoint": True}
    base.engine.write_json_atomic(Path(args.pre_endpoint_receipt), pre_receipt)
    scores, endpoint_receipt = load_endpoint(Path(args.endpoint_file), contexts)
    with base._configured(ANALYSIS_EXPOSED, ANALYSIS_REFERENCE):
        base.engine.write_endpoint_rows(stage / "endpoint_scores.csv", contexts, scores)
    results = [inference_for(contexts, scores, source, np.random.default_rng(INFERENCE_SEEDS[source])) for source in SOURCES]
    with base._configured(ANALYSIS_EXPOSED, ANALYSIS_REFERENCE):
        base.engine.write_inference(stage / "inference.csv", results)
    nominal_pass = all(result["pass"] for result in results)
    return {"experiment_id": EXPERIMENT_ID, "status": "FEASIBILITY_ONLY_NOMINAL_GATES_PASS" if nominal_pass else "FEASIBILITY_ONLY_NOMINAL_GATE_FAILURE", "analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "analysis_type": "preregistered_source_specific_lineage_stratified_smad4_aurka_transport_replication", "claim_eligibility": {"primary_confirmatory": False, "design_sensitivity_label": "FEASIBILITY_ONLY", "nominal_primary_gates_pass": nominal_pass}, "context_receipt": context_receipt, "design_sensitivity": design_receipt, "pre_endpoint_receipt": pre_receipt, "endpoint_receipt": endpoint_receipt, "primary": results, "inference_receipt": {"design_seeds": DESIGN_SEEDS, "inference_seeds": INFERENCE_SEEDS, "permutations": base.engine.PERMUTATIONS, "bootstraps": base.engine.BOOTSTRAPS, "bootstrap_interval": "percentile_95_linear_quantile", "unit": "collapsed_source_model_id", "cross_source_raw_score_comparison": False}, "implementation_receipt": {"manifest_path": args.manifest_file, "required_base_commit": manifest["implementation_boundary"]["required_base_commit"], "implementation_commit": manifest["implementation_boundary"]["implementation_commit"], "implementation_module": manifest["implementation_boundary"]["implementation_module"], "engine_module": manifest["implementation_boundary"]["engine_module"], "uv_lock_sha256": manifest["uv_lock_sha256"]}, "artifact_receipt_sha256": {name: sha256(stage / name) for name in ("context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv")} | {"summary.json": ""}, "overall_pass": False, "claim_boundary": "SMAD4 damaging-matrix proxy association with source-specific AURKA dependency in frozen 23Q4 cell-line screen cohorts; no functional SMAD4-loss, AURKA-inhibitor, spindle-checkpoint, causal, pharmacologic, treatment, clinical, or confirmatory claim"}


def validate_staged(stage: Path, result: dict[str, object]) -> None:
    if {path.name for path in stage.iterdir() if path.is_file()} != EXPECTED_RESULT_FILES:
        raise IntegrityError("EXP032 staged file set drift")
    for filename in ("context_ledger.csv", "endpoint_scores.csv"):
        with (stage / filename).open(newline="", encoding="utf-8") as handle:
            if len(list(__import__('csv').DictReader(handle))) != 1290:
                raise IntegrityError(f"{filename} row count drift")
    with (stage / "design_sensitivity.csv").open(newline="", encoding="utf-8") as handle:
        if len(list(__import__('csv').DictReader(handle))) != 2:
            raise IntegrityError("design row drift")
    with (stage / "inference.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(__import__('csv').DictReader(handle))
        if len(rows) != 2 or any(row["primary_confirmatory"] != "False" for row in rows):
            raise IntegrityError("inference claim drift")
    expected_keys = {"experiment_id", "status", "analysis_label", "confirmatory_claim", "analysis_type", "claim_eligibility", "context_receipt", "design_sensitivity", "pre_endpoint_receipt", "endpoint_receipt", "primary", "inference_receipt", "implementation_receipt", "artifact_receipt_sha256", "overall_pass", "claim_boundary"}
    if set(result) != expected_keys or result["experiment_id"] != EXPERIMENT_ID or result["analysis_label"] != "FEASIBILITY_ONLY" or result["confirmatory_claim"] is not False or result["overall_pass"] is not False:
        raise IntegrityError("terminal claim contract drift")
    if result["artifact_receipt_sha256"]["summary.json"] != base.engine.summary_digest(result):
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
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-032/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-032/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-032/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-032/pre_endpoint_receipt.json")
    return parser


def publish(args: argparse.Namespace) -> int:
    target, error = Path(args.results_dir), Path(args.error_receipt)
    if target.exists():
        base.engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_RESULTS_DIRECTORY_EXISTS", "results_written": False})
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
                base.engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": exc.status, "analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False, "error": str(exc), "error_type": type(exc).__name__, "t0": True, "endpoint_opened": exc.endpoint_opened, "results_written": False, "preserved_path": preserved_path})
                return 2
            result["artifact_receipt_sha256"]["summary.json"] = base.engine.summary_digest(result)
            (stage / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            validate_staged(stage, result)
            os.replace(stage, target)
    except Exception as exc:
        base.engine.write_json_atomic(error, {"experiment_id": EXPERIMENT_ID, "status": "ERROR_INTEGRITY", "error": str(exc), "error_type": type(exc).__name__, "results_written": False})
        return 1
    if error.exists():
        error.unlink()
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["overall_pass"] else 2


def main() -> None:
    raise SystemExit(publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
