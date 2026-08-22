"""Bounded composite PBRM1/ARID2 proxy to PARP1 dependency audit."""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Sequence

from . import brca12_polq_replication as base


EXPERIMENT_ID = "EXP-20260822-039"
PAIR_ID = "PBRM1_or_ARID2_damaging_to_PARP1"
STATUS_COLUMNS = ("PBRM1 (55193)", "ARID2 (196528)")
STATUS_LABEL = "PBRM1_or_ARID2_composite"
TARGET_COLUMN = "PARP1 (142)"
SOURCES = ("Avana", "KY")
ANALYSIS_EXPOSED = "damaging"
ANALYSIS_REFERENCE = "matrix_intact"
EXPECTED_MODULE_PATH = "src/candrel/pbrm1_arid2_parp1_replication.py"
ENGINE_MODULE_PATH = "src/candrel/tp53_mdm2_replication.py"
PROJECT_PATH = "pyproject.toml"
REQUIRED_BASE_COMMIT = "037c6d5"
EXPECTED_HASHES = {
    "endpoint": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "screen_qc": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "screen_map": "1e2bf9075600cd049dafc385866991523c65806657c3f8bd71afde3fe00ee9ad",
    "model": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "damaging": "aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3",
}
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_STATUS_COUNTS = {
    "Avana": {"damaging": 49, "matrix_intact": 926},
    "KY": {"damaging": 22, "matrix_intact": 293},
}
EXPECTED_MIXED_LINEAGES = {"Avana": 15, "KY": 8}
DESIGN_SEEDS = {"Avana": 20263900, "KY": 20264000}
INFERENCE_SEEDS = {"Avana": 20273900, "KY": 20274000}
EXPECTED_ROSTER_SHA256 = "6ab143e99b7d58d82a1b1e22b9948aacc5944ebe6daabe448505cd8735188af4"
EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = "cb136013f13860195e55a6f59ed1abc4a843ff276135a13b0906142801a499d7"

IntegrityError = base.IntegrityError
T0Stop = base.T0Stop
Context = base.Context


def _configure_base() -> None:
    base.EXPERIMENT_ID = EXPERIMENT_ID
    base.PAIR_ID = PAIR_ID
    base.STATUS_COLUMNS = STATUS_COLUMNS
    base.STATUS_LABEL = STATUS_LABEL
    base.TARGET_COLUMN = TARGET_COLUMN
    base.EXPECTED_HASHES = EXPECTED_HASHES.copy()
    base.EXPECTED_SOURCE_MODELS = EXPECTED_SOURCE_MODELS.copy()
    base.EXPECTED_STATUS_COUNTS = {source: counts.copy() for source, counts in EXPECTED_STATUS_COUNTS.items()}
    base.EXPECTED_MIXED_LINEAGES = EXPECTED_MIXED_LINEAGES.copy()
    base.DESIGN_SEEDS = DESIGN_SEEDS.copy()
    base.INFERENCE_SEEDS = INFERENCE_SEEDS.copy()
    base.EXPECTED_ROSTER_SHA256 = EXPECTED_ROSTER_SHA256
    base.EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256
    base.EXPECTED_MODULE_PATH = EXPECTED_MODULE_PATH
    base.ENGINE_MODULE_PATH = ENGINE_MODULE_PATH
    base.PROJECT_PATH = PROJECT_PATH
    base.REQUIRED_BASE_COMMIT = REQUIRED_BASE_COMMIT


def _load_composite_status_matrix(path: Path, model_ids: set[str]) -> tuple[dict[str, int], str]:
    actual = base.sha256(path)
    if actual != EXPECTED_HASHES["damaging"]:
        raise IntegrityError(f"damaging matrix SHA-256 drift: {actual}")
    statuses: dict[str, int] = {}
    seen: set[str] = set()
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        header = next(reader, None)
        if header is None or not header or header[0] != "" or any(header.count(column) != 1 for column in STATUS_COLUMNS):
            raise IntegrityError("PBRM1/ARID2 matrix header drift")
        indices = [header.index(column) for column in STATUS_COLUMNS]
        for row in reader:
            if not row:
                continue
            model_id = row[0].strip()
            if not model_id or model_id in seen:
                raise IntegrityError(f"duplicate matrix ModelID: {model_id}")
            seen.add(model_id)
            if model_id in model_ids:
                if any(index >= len(row) for index in indices):
                    raise IntegrityError(f"short matrix row: {model_id}")
                values = [base.engine.parse_matrix_value(row[index], (model_id, column)) for index, column in zip(indices, STATUS_COLUMNS)]
                statuses[model_id] = int(any(value in {1, 2} for value in values))
    if set(statuses) != model_ids:
        raise IntegrityError(f"PBRM1/ARID2 matrix coverage drift: expected {len(model_ids)}, got {len(statuses)}")
    return statuses, actual


def _verify_manifest(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["experiment_id"] != EXPERIMENT_ID or manifest["entrypoint"] != ".venv/bin/python -m candrel.pbrm1_arid2_parp1_replication":
            raise ValueError("manifest identity/entrypoint drift")
        expected_inputs = {
            "endpoint": {"path": "data/raw/depmap/23q4/ScreenNaiveGeneScore.csv", "sha256": EXPECTED_HASHES["endpoint"], "target_column": TARGET_COLUMN},
            "screen_qc": {"path": "data/raw/depmap/23q4/AchillesScreenQCReport.csv", "sha256": EXPECTED_HASHES["screen_qc"]},
            "screen_map": {"path": "data/raw/depmap/23q4/CRISPRScreenMap.csv", "sha256": EXPECTED_HASHES["screen_map"]},
            "model": {"path": "data/raw/depmap/23q4/Model.csv", "sha256": EXPECTED_HASHES["model"]},
            "damaging_matrix": {"path": "data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv", "sha256": EXPECTED_HASHES["damaging"], "status_columns": list(STATUS_COLUMNS)},
        }
        if manifest["inputs"] != expected_inputs:
            raise ValueError("manifest input contract drift")
        if manifest["eligibility"] != {"libraries": list(SOURCES), "pass_qc": True, "can_include": True, "expected_source_models": EXPECTED_SOURCE_MODELS}:
            raise ValueError("manifest eligibility drift")
        expected_status = {"exposed": ANALYSIS_EXPOSED, "reference": ANALYSIS_REFERENCE, "status_columns": list(STATUS_COLUMNS), "exposed_matrix_values": [1], "reference_matrix_values": [0], "expected_counts": EXPECTED_STATUS_COUNTS, "expected_mixed_lineages": EXPECTED_MIXED_LINEAGES}
        if manifest["status_contract"] != expected_status:
            raise ValueError("manifest status contract drift")
        census = Path(manifest["candidate_census"]["path"])
        receipt = Path(manifest["design_receipt"]["path"])
        seal = Path(manifest["selection_seal"]["path"])
        if base.sha256(census) != manifest["candidate_census"]["sha256"] or base.sha256(receipt) != manifest["design_receipt"]["sha256"] or base.sha256(seal) != manifest["selection_seal"]["sha256"]:
            raise ValueError("selection/census/design receipt SHA-256 drift")
        if manifest["candidate_census"]["canonical_roster_sha256"] != EXPECTED_ROSTER_SHA256 or manifest["design_receipt"]["canonical_roster_sha256"] != EXPECTED_ROSTER_SHA256:
            raise ValueError("canonical roster binding drift")
        if base.normalized_receipt_sha256(receipt, "receipt_sha256") != EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256:
            raise ValueError("design receipt normalized digest drift")
        if manifest["selection_seal"]["sealed_before_endpoint_access"] is not True or manifest["selection_seal"]["protocol_commit"] != "1fd72544be7a09d6c9d21bee9a4cf6a04c864b5a":
            raise ValueError("selection seal contract drift")
        expected_design = {"mean_shift": base.engine.NORMAL_MEAN_SHIFT, "null_permutations": base.engine.PERMUTATIONS, "alternative_simulations": base.engine.DESIGN_SIMULATIONS, "planning_power_seeds": DESIGN_SEEDS, "expected_critical_delta": {"Avana": -0.16113744075829384, "KY": -0.23933209647495363}, "expected_power": {"Avana": 0.6569, "KY": 0.3913}, "minimum_power_for_confirmatory_label": base.engine.MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY"}
        if manifest["design_sensitivity"] != expected_design:
            raise ValueError("manifest design contract drift")
        expected_inference = {"inference_seeds": INFERENCE_SEEDS, "permutations": base.engine.PERMUTATIONS, "bootstraps": base.engine.BOOTSTRAPS, "delta_target": base.engine.DELTA_TARGET, "permutation_p_max": base.engine.P_MAX, "bootstrap_upper_max": base.engine.BOOTSTRAP_UPPER_MAX, "max_lineage_delta": base.engine.MAX_LINEAGE_DELTA}
        if manifest["inference"] != expected_inference or manifest["claim_contract"] != {"analysis_label": "FEASIBILITY_ONLY", "confirmatory_claim": False, "overall_pass": False}:
            raise ValueError("manifest inference/claim contract drift")
        if base.sha256(Path("uv.lock")) != manifest["uv_lock_sha256"]:
            raise ValueError("uv.lock SHA-256 drift")
        boundary = manifest["implementation_boundary"]
        if boundary["required_base_commit"] != REQUIRED_BASE_COMMIT or boundary["implementation_module"] != EXPECTED_MODULE_PATH or boundary["engine_module"] != ENGINE_MODULE_PATH or boundary["project_file"] != PROJECT_PATH:
            raise ValueError("implementation boundary path/base drift")
        for commit in (boundary["required_base_commit"], boundary["implementation_commit"]):
            if base.git_command("rev-parse", "--verify", f"{commit}^{{commit}}").returncode != 0 or base.git_command("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
                raise ValueError(f"unresolvable/non-ancestor commit: {commit}")
        if {item["path"] for item in boundary["modules"]} != {EXPECTED_MODULE_PATH, ENGINE_MODULE_PATH, PROJECT_PATH}:
            raise ValueError("transitive module set drift")
        for item in boundary["modules"]:
            if base.sha256(Path(item["path"])) != item["sha256"] or base.git_blob_sha256(boundary["implementation_commit"], item["path"]) != item["sha256"]:
                raise ValueError(f"implementation module hash drift: {item['path']}")
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        raise T0Stop("T0_IMPLEMENTATION_BOUNDARY", False, str(exc)) from exc
    return manifest


def _write_context_ledger(path: Path, contexts: Sequence[Context]) -> None:
    fields = ["source", "model_id", "lineage", "eligible_screen_ids", "PBRM1_or_ARID2_composite_matrix_value", "PBRM1_or_ARID2_status"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for context in contexts:
            writer.writerow({"source": context.source, "model_id": context.model_id, "lineage": context.lineage, "eligible_screen_ids": ";".join(context.screen_ids), "PBRM1_or_ARID2_composite_matrix_value": context.matrix_value, "PBRM1_or_ARID2_status": context.status})


def _run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    result = base._ORIGINAL_RUN(args, stage)
    result["analysis_type"] = "preregistered_source_specific_lineage_stratified_pbrm1_arid2_parp1_proxy_replication"
    result["claim_boundary"] = "composite PBRM1-or-ARID2 damaging-matrix proxy association with source-specific PARP1 dependency in frozen 23Q4 cell-line screen cohorts; no isolated PBRM1 loss, ARID2 loss, PBAF causality, HRD, PARP-inhibitor, treatment, clinical, or confirmatory claim"
    return result


_configure_base()
base._load_composite_status_matrix = _load_composite_status_matrix
base.verify_implementation_boundary = _verify_manifest
base.write_context_ledger = _write_context_ledger
base._ORIGINAL_RUN = base.run
base.run = _run


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--screen-map-file", default="data/raw/depmap/23q4/CRISPRScreenMap.csv")
    parser.add_argument("--model-file", default="data/raw/depmap/23q4/Model.csv")
    parser.add_argument("--damaging-file", default="data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv")
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-039/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-039/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-039/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-039/pre_endpoint_receipt.json")
    return parser


def main() -> None:
    raise SystemExit(base.publish(build_parser().parse_args()))


if __name__ == "__main__":
    main()
