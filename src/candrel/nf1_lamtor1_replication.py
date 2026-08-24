"""Bounded NF1-proxy to LAMTOR1 dependency transport audit."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import nf1_ptpn11_replication as base


EXPERIMENT_ID = "EXP-20260822-040"
PAIR_ID = "NF1_damaging_to_LAMTOR1"
STATUS_COLUMN = "NF1 (4763)"
TARGET_COLUMN = "LAMTOR1 (55004)"
SOURCES = ("Avana", "KY")
ANALYSIS_EXPOSED = "damaging"
ANALYSIS_REFERENCE = "matrix_intact"
EXPECTED_MODULE_PATH = "src/candrel/nf1_lamtor1_replication.py"
ENGINE_MODULE_PATH = "src/candrel/tp53_mdm2_replication.py"
PROJECT_PATH = "pyproject.toml"
REQUIRED_BASE_COMMIT = "a67b546"
EXPECTED_HASHES = {
    "endpoint": "e674845fcff8297cc99a3dc0188a40e210289207c37004ba78ddd74d8f03d721",
    "screen_qc": "fbb4bc1f27a65a626250d8c5e51a485c8d31f853461e717756be0dcdd160c407",
    "screen_map": "1e2bf9075600cd049dafc385866991523c65806657f3c8bd71afde3fe00ee9ad",
    "model": "6b77a73209ce3faaa7442dbd947d8e08ddcb08b538c36fe820163f9cff321341",
    "damaging": "aea4d970c0876afb90d2dc0e2709ff28be5a84e4e246f3a5a31faaba0fbc47e3",
}
EXPECTED_SOURCE_MODELS = {"Avana": 975, "KY": 315}
EXPECTED_STATUS_COUNTS = {
    "Avana": {"damaging": 57, "matrix_intact": 918},
    "KY": {"damaging": 21, "matrix_intact": 294},
}
EXPECTED_MIXED_LINEAGES = {"Avana": 15, "KY": 9}
DESIGN_SEEDS = {"Avana": 20264000, "KY": 20264100}
INFERENCE_SEEDS = {"Avana": 20274000, "KY": 20274100}
EXPECTED_ROSTER_SHA256 = "8c3229c5925e533688a9efb8979700d1f2d379a760d0672544a61073a8bfc375"
EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = "484cdb578f157a736e472a5c90f68bb56d7fee1305b69a27115b01dc66567660"

IntegrityError = base.IntegrityError
T0Stop = base.T0Stop
Context = base.Context

_ORIGINAL_RUN = base.run
_BASE_CONFIG_KEYS = (
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
    "EXPECTED_ROSTER_SHA256",
    "EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256",
    "EXPECTED_MODULE_PATH",
    "ENGINE_MODULE_PATH",
    "PROJECT_PATH",
    "REQUIRED_BASE_COMMIT",
)


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
    base.EXPECTED_ROSTER_SHA256 = EXPECTED_ROSTER_SHA256
    base.EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256 = EXPECTED_DESIGN_RECEIPT_NORMALIZED_SHA256
    base.EXPECTED_MODULE_PATH = EXPECTED_MODULE_PATH
    base.ENGINE_MODULE_PATH = ENGINE_MODULE_PATH
    base.PROJECT_PATH = PROJECT_PATH
    base.REQUIRED_BASE_COMMIT = REQUIRED_BASE_COMMIT


def _verify_manifest(manifest_path: Path) -> dict[str, object]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest["experiment_id"] != EXPERIMENT_ID or manifest["entrypoint"] != ".venv/bin/python -m candrel.nf1_lamtor1_replication":
            raise ValueError("manifest identity/entrypoint drift")
        expected_inputs = {
            "endpoint": {"path": "data/raw/depmap/23q4/ScreenNaiveGeneScore.csv", "sha256": EXPECTED_HASHES["endpoint"], "target_column": TARGET_COLUMN},
            "screen_qc": {"path": "data/raw/depmap/23q4/AchillesScreenQCReport.csv", "sha256": EXPECTED_HASHES["screen_qc"]},
            "screen_map": {"path": "data/raw/depmap/23q4/CRISPRScreenMap.csv", "sha256": EXPECTED_HASHES["screen_map"]},
            "model": {"path": "data/raw/depmap/23q4/Model.csv", "sha256": EXPECTED_HASHES["model"]},
            "damaging_matrix": {"path": "data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv", "sha256": EXPECTED_HASHES["damaging"], "status_column": STATUS_COLUMN},
        }
        if manifest["inputs"] != expected_inputs:
            raise ValueError("manifest input contract drift")
        if manifest["eligibility"] != {"libraries": list(SOURCES), "pass_qc": True, "can_include": True, "expected_source_models": EXPECTED_SOURCE_MODELS}:
            raise ValueError("manifest eligibility drift")
        expected_status = {"exposed": ANALYSIS_EXPOSED, "reference": ANALYSIS_REFERENCE, "exposed_matrix_values": [1, 2], "reference_matrix_values": [0], "expected_counts": EXPECTED_STATUS_COUNTS, "expected_mixed_lineages": EXPECTED_MIXED_LINEAGES}
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
        expected_design = {"mean_shift": base.engine.NORMAL_MEAN_SHIFT, "null_permutations": base.engine.PERMUTATIONS, "alternative_simulations": base.engine.DESIGN_SIMULATIONS, "planning_power_seeds": DESIGN_SEEDS, "expected_critical_delta": {"Avana": -0.14961776483436476, "KY": -0.23846153846153847}, "expected_power": {"Avana": 0.7192, "KY": 0.4014}, "minimum_power_for_confirmatory_label": base.engine.MIN_CONFIRMATORY_POWER, "frozen_label": "FEASIBILITY_ONLY"}
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


def _run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    result = _ORIGINAL_RUN(args, stage)
    result["analysis_type"] = "preregistered_source_specific_lineage_stratified_nf1_lamtor1_replication"
    result["claim_boundary"] = "damaging-matrix NF1 status association with source-specific LAMTOR1 dependency in frozen 23Q4 screen cohorts; no NF1 protein loss, RAS/mTOR causality, LAMTOR1 pharmacology, treatment, clinical, or confirmatory claim"
    return result


def run(args: argparse.Namespace, stage: Path) -> dict[str, object]:
    saved = {key: getattr(base, key) for key in _BASE_CONFIG_KEYS}
    saved_verify = base.verify_implementation_boundary
    _configure_base()
    base.verify_implementation_boundary = _verify_manifest
    try:
        return _run(args, stage)
    finally:
        base.verify_implementation_boundary = saved_verify
        for key, value in saved.items():
            setattr(base, key, value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--endpoint-file", default="data/raw/depmap/23q4/ScreenNaiveGeneScore.csv")
    parser.add_argument("--qc-file", default="data/raw/depmap/23q4/AchillesScreenQCReport.csv")
    parser.add_argument("--screen-map-file", default="data/raw/depmap/23q4/CRISPRScreenMap.csv")
    parser.add_argument("--model-file", default="data/raw/depmap/23q4/Model.csv")
    parser.add_argument("--damaging-file", default="data/raw/depmap/23q4/OmicsSomaticMutationsMatrixDamaging.csv")
    parser.add_argument("--manifest-file", default="experiments/EXP-20260822-040/manifest.json")
    parser.add_argument("--results-dir", default="experiments/EXP-20260822-040/results")
    parser.add_argument("--error-receipt", default="experiments/EXP-20260822-040/error_receipt.json")
    parser.add_argument("--pre-endpoint-receipt", default="experiments/EXP-20260822-040/pre_endpoint_receipt.json")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    saved = {key: getattr(base, key) for key in _BASE_CONFIG_KEYS}
    saved_verify = base.verify_implementation_boundary
    saved_run = base.run
    _configure_base()
    base.verify_implementation_boundary = _verify_manifest
    base.run = _run
    try:
        raise SystemExit(base.publish(args))
    finally:
        base.verify_implementation_boundary = saved_verify
        base.run = saved_run
        for key, value in saved.items():
            setattr(base, key, value)


if __name__ == "__main__":
    main()
