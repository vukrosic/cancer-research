from __future__ import annotations

import csv
import inspect
import json
from pathlib import Path

import pytest

from candrel import wrn_guide_loo_passing as module


def test_strict_median_defines_even_and_odd_behavior() -> None:
    assert module.strict_median([8.0, 1.0, 3.0, 2.0]) == pytest.approx(2.5)
    assert module.strict_median([8.0, 1.0, 3.0]) == pytest.approx(3.0)
    with pytest.raises(module.IntegrityError):
        module.strict_median([])


def test_scores_omit_only_selected_source_guide(monkeypatch) -> None:
    monkeypatch.setattr(
        module.base,
        "EXPECTED_GUIDES",
        {"Avana": ("a", "b", "c", "d"), "KY": ("e", "f", "g", "h", "i")},
    )
    means = {
        ("S1", "M1", "Avana"): {"a": 1.0, "b": 2.0, "c": 3.0, "d": 8.0},
        ("S2", "M1", "KY"): {"e": 1.0, "f": 2.0, "g": 3.0, "h": 4.0, "i": 9.0},
    }
    baseline = module.scores_from_guide_means(means, expected_records=2)
    omitted = module.scores_from_guide_means(
        means, "Avana", "d", expected_records=2
    )
    assert baseline[("S1", "M1", "Avana")] == pytest.approx(2.5)
    assert omitted[("S1", "M1", "Avana")] == pytest.approx(2.0)
    assert omitted[("S2", "M1", "KY")] == baseline[("S2", "M1", "KY")]


def _records() -> list[module.GapRecord]:
    return [
        module.GapRecord(
            model_id=f"M{i}",
            model_name=f"Model {i}",
            tissue="Large Intestine" if i < 17 else "Ovary",
            label="MSS",
            avana_score=0.0,
            ky_score=0.0,
            avana_percentile=0.0,
            ky_percentile=0.0,
            baseline_gap=0.30 if i < 10 else 0.10,
            baseline_flagged=i < 10,
        )
        for i in range(34)
    ]


def test_primary_requires_eight_of_ten_across_all_nine() -> None:
    gaps = {}
    for source, count in (("Avana", 4), ("KY", 5)):
        for index in range(count):
            gaps[f"omit_{source}_g{index}"] = {
                f"M{i}": 0.30 if i < 10 else 0.10 for i in range(34)
            }
    gaps["omit_Avana_g0"]["M8"] = 0.24
    gaps["omit_KY_g0"]["M9"] = 0.24
    rows, summary = module.summarize_robustness(_records(), gaps)
    assert summary["fully_robust_flagged_models"] == 8
    assert summary["primary_pass"] is True
    assert sum(row.fully_robust_all_nine for row in rows if row.baseline_flagged) == 8


def test_gap_loader_rejects_noncanonical_boolean(tmp_path, monkeypatch) -> None:
    path = tmp_path / "gaps.csv"
    fields = [
        "model_id", "model_name", "tissue", "label", "avana_score", "ky_score",
        "avana_percentile", "ky_percentile", "absolute_percentile_gap",
        "discordant_ge_0_25",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerow(
            {
                "model_id": "M1", "model_name": "Model", "tissue": "Ovary",
                "label": "MSS", "avana_score": "0", "ky_score": "0",
                "avana_percentile": "0", "ky_percentile": "0",
                "absolute_percentile_gap": "0.3", "discordant_ge_0_25": "true",
            }
        )
    monkeypatch.setattr(module, "EXPECTED_GAP_HASH", module.base.sha256(path))
    frozen = [module.FrozenScreen("S1", "M1", "Avana", "Ovary"), module.FrozenScreen("S2", "M1", "KY", "Ovary")]
    with pytest.raises(module.IntegrityError, match="noncanonical boolean"):
        module.load_gap_records(path, frozen)


def test_execution_order_keeps_gap_loading_after_both_baseline_gates() -> None:
    source = inspect.getsource(module.run)
    assert source.index("verify_official_baseline") < source.index("load_gap_records")
    assert source.index("verify_parent_ledger") < source.index("load_gap_records")
    assert source.index("load_gap_records") < source.index("for source in base.SOURCES")


def test_parser_targets_exp012_outputs() -> None:
    args = module.build_parser().parse_args([])
    assert "EXP-20260822-012" in args.results_dir
    assert "EXP-20260822-012" in args.error_receipt


def test_screen_configuration_ledger_covers_every_screen_and_configuration(monkeypatch) -> None:
    monkeypatch.setattr(
        module.base,
        "EXPECTED_GUIDES",
        {"Avana": ("a", "b", "c", "d"), "KY": ("e", "f", "g", "h", "i")},
    )
    frozen = [
        module.FrozenScreen("S1", "M1", "Avana", "Ovary"),
        module.FrozenScreen("S2", "M1", "KY", "Ovary"),
    ]
    baseline_scores = {("S1", "M1", "Avana"): 1.0, ("S2", "M1", "KY"): 2.0}
    omitted_scores = {("S1", "M1", "Avana"): 1.5, ("S2", "M1", "KY"): 2.0}
    percentiles = {("M1", "Avana"): 0.5, ("M1", "KY"): 0.25}
    rows = module.build_screen_configuration_rows(
        frozen,
        [
            ("baseline", "", "", baseline_scores, percentiles),
            ("omit_Avana_d", "Avana", "d", omitted_scores, percentiles),
        ],
    )
    assert len(rows) == 4
    avana_omitted = next(
        row for row in rows if row["configuration"] == "omit_Avana_d" and row["source"] == "Avana"
    )
    ky_unaffected = next(
        row for row in rows if row["configuration"] == "omit_Avana_d" and row["source"] == "KY"
    )
    assert avana_omitted["retained_guide_count"] == 3
    assert ky_unaffected["retained_guide_count"] == 5


def test_publish_refuses_to_overwrite_existing_results(tmp_path, monkeypatch) -> None:
    target = tmp_path / "results"
    target.mkdir()
    (target / "sentinel.txt").write_text("old valid result")
    error = tmp_path / "error.json"
    args = module.build_parser().parse_args(
        ["--results-dir", str(target), "--error-receipt", str(error)]
    )
    monkeypatch.setattr(module, "run", lambda *_: pytest.fail("run must not execute"))
    assert module.publish(args) == 1
    assert (target / "sentinel.txt").read_text() == "old valid result"
    receipt = json.loads(error.read_text())
    assert receipt["status"] == "ERROR_RESULTS_DIRECTORY_EXISTS"
    assert receipt["results_written"] is False


def test_staged_validator_rejects_csv_schema_before_publish(tmp_path) -> None:
    stage = tmp_path / "stage"
    stage.mkdir()
    for name in module.EXPECTED_RESULT_FILES:
        (stage / name).write_text("bad\n")
    with pytest.raises(module.IntegrityError, match="staged CSV schema drift"):
        module.validate_staged_result_files(stage, {})


def test_summary_digest_is_normalized_for_self_receipt() -> None:
    result = {
        "experiment_id": module.EXPERIMENT_ID,
        "artifact_receipt_sha256": {name: "" for name in module.EXPECTED_RESULT_FILES},
    }
    digest = module.summary_digest(result)
    result["artifact_receipt_sha256"]["summary.json"] = digest
    assert module.summary_digest(result) == digest


def _summary_ledger_fixture() -> tuple[dict[str, object], list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    configs = ["baseline", *[f"omit_Avana_g{i}" for i in range(4)], *[f"omit_KY_g{i}" for i in range(5)]]
    config_rows = [
        {
            "configuration": name,
            "equal_tissue_theta": "0.5",
            "flagged_models": "10",
            "source": "" if name == "baseline" else ("Avana" if "Avana" in name else "KY"),
            "omitted_guide": "" if name == "baseline" else name.rsplit("_", 1)[1],
        }
        for name in configs
    ]
    model_gap_rows = []
    for model_index in range(34):
        for configuration in configs:
            flagged = model_index < 10
            model_gap_rows.append(
                {
                    "model_id": f"M{model_index}",
                    "configuration": configuration,
                    "baseline_flagged": str(flagged),
                    "gap": "0.3" if flagged else "0.1",
                    "flagged_ge_0_25": str(flagged),
                }
            )
    robustness_rows = [
        {
            "model_id": f"M{model_index}",
            "fully_robust_all_nine": str(model_index < 10),
            "avana_all_omissions_retain_flag": str(model_index < 10),
            "ky_all_omissions_retain_flag": str(model_index < 10),
            "flagged_omissions_of_nine": "9" if model_index < 10 else "0",
            "baseline_gap": "0.3" if model_index < 10 else "0.1",
            "min_gap_all_ten_configurations": "0.3" if model_index < 10 else "0.1",
            "median_gap_all_ten_configurations": "0.3" if model_index < 10 else "0.1",
            "max_gap_all_ten_configurations": "0.3" if model_index < 10 else "0.1",
        }
        for model_index in range(34)
    ]
    primary = {
        "locked_baseline_flagged_models": 10,
        "fully_robust_flagged_models": 10,
        "minimum_fully_robust_required": 8,
        "avana_all_omissions_robust_models": 10,
        "ky_all_omissions_robust_models": 10,
        "unique_baseline_unflagged_becoming_flagged": 0,
        "unique_transition_model_ids": [],
        "total_unflagged_to_flagged_transitions": 0,
        "possible_unflagged_configuration_transitions": 216,
        "primary_pass": True,
    }
    result = {
        "overall_pass": True,
        "primary": primary,
        "configurations": {
            "baseline_plus_omissions": 10,
            "single_guide_omissions": 9,
            "avana_omissions": 4,
            "ky_omissions": 5,
        },
        "ordering_sensitivity": {
            "baseline_equal_tissue_theta": 0.5,
            "minimum_perturbed_theta": 0.5,
            "maximum_perturbed_theta": 0.5,
        },
    }
    return result, config_rows, model_gap_rows, robustness_rows


def test_summary_validator_rejects_primary_tampering() -> None:
    result, config_rows, model_gap_rows, robustness_rows = _summary_ledger_fixture()
    result["primary"]["fully_robust_flagged_models"] = 9
    with pytest.raises(module.IntegrityError, match="primary cross-check"):
        module.validate_summary_against_ledgers(result, config_rows, model_gap_rows, robustness_rows)


def test_summary_validator_rejects_ordering_tampering() -> None:
    result, config_rows, model_gap_rows, robustness_rows = _summary_ledger_fixture()
    result["ordering_sensitivity"]["maximum_perturbed_theta"] = 0.9
    with pytest.raises(module.IntegrityError, match="ordering cross-check"):
        module.validate_summary_against_ledgers(result, config_rows, model_gap_rows, robustness_rows)


def test_summary_validator_rejects_overall_pass_tampering() -> None:
    result, config_rows, model_gap_rows, robustness_rows = _summary_ledger_fixture()
    result["overall_pass"] = False
    with pytest.raises(module.IntegrityError, match="overall-pass cross-check"):
        module.validate_summary_against_ledgers(result, config_rows, model_gap_rows, robustness_rows)


def test_summary_validator_rejects_combined_primary_and_overall_tampering() -> None:
    result, config_rows, model_gap_rows, robustness_rows = _summary_ledger_fixture()
    result["overall_pass"] = False
    result["primary"]["primary_pass"] = False
    with pytest.raises(module.IntegrityError, match="primary cross-check"):
        module.validate_summary_against_ledgers(result, config_rows, model_gap_rows, robustness_rows)
