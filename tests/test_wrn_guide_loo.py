from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pytest

from candrel.wrn_guide_loo import (
    FLAG_THRESHOLD,
    GapRecord,
    IntegrityError,
    extract_lfc_values,
    scores_from_guide_means,
    summarize_robustness,
    verify_baseline,
)


def test_scores_from_guide_means_omits_only_selected_source_guide() -> None:
    guide_means = {
        ("M1", "Avana"): {"a": 1.0, "b": 2.0, "c": 3.0, "d": 8.0},
        ("M1", "KY"): {"e": 1.0, "f": 2.0, "g": 3.0, "h": 4.0, "i": 9.0},
    }
    import candrel.wrn_guide_loo as module

    original = module.EXPECTED_GUIDES
    module.EXPECTED_GUIDES = {
        "Avana": ("a", "b", "c", "d"),
        "KY": ("e", "f", "g", "h", "i"),
    }
    try:
        baseline = scores_from_guide_means(guide_means, expected_records=2)
        omitted = scores_from_guide_means(
            guide_means, "Avana", "d", expected_records=2
        )
    finally:
        module.EXPECTED_GUIDES = original
    assert baseline[("M1", "Avana")] == pytest.approx(2.5)
    assert omitted[("M1", "Avana")] == pytest.approx(2.0)
    assert omitted[("M1", "KY")] == baseline[("M1", "KY")]


def test_baseline_gate_uses_absolute_tolerance_without_tuning() -> None:
    from candrel.wrn_guide_loo import DenominatorRecord

    rows = [
        DenominatorRecord("M1", "Name", "Ovary", "MSS", "Avana", "S1", -1.0)
    ]
    reconstructed = {("M1", "Avana"): -1.0 + 1e-9}
    result = verify_baseline(rows, reconstructed, {"S1": -1.0}, expected_records=1)
    assert result["passed"] is True
    with pytest.raises(IntegrityError, match="baseline reconstruction drift"):
        verify_baseline(
            rows,
            {("M1", "Avana"): -1.0 + 2e-8},
            {"S1": -1.0},
            expected_records=1,
        )


def _gap_records() -> list[GapRecord]:
    return [
        GapRecord(
            model_id=f"M{i}",
            model_name=f"Model {i}",
            tissue="Large Intestine" if i < 17 else "Ovary",
            label="MSS",
            baseline_gap=0.3 if i < 10 else 0.1,
            baseline_flagged=i < 10,
        )
        for i in range(34)
    ]


def test_primary_robustness_requires_eight_of_ten_survive_all_nine() -> None:
    gaps = {}
    for source, count in (("Avana", 4), ("KY", 5)):
        for guide in range(count):
            values = {f"M{i}": (0.3 if i < 10 else 0.1) for i in range(34)}
            gaps[f"omit_{source}_g{guide}"] = values
    gaps["omit_Avana_g0"]["M8"] = FLAG_THRESHOLD - 0.01
    gaps["omit_KY_g0"]["M9"] = FLAG_THRESHOLD - 0.01
    rows, summary = summarize_robustness(_gap_records(), gaps)
    assert summary["fully_robust_flagged_models"] == 8
    assert summary["primary_pass"] is True
    assert sum(row.fully_robust_all_nine for row in rows if row.baseline_flagged) == 8


def test_unflagged_transition_counts_unique_and_model_configuration() -> None:
    gaps = {}
    for source, count in (("Avana", 4), ("KY", 5)):
        for guide in range(count):
            gaps[f"omit_{source}_g{guide}"] = {
                f"M{i}": (0.3 if i < 10 else 0.1) for i in range(34)
            }
    gaps["omit_Avana_g0"]["M10"] = 0.25
    gaps["omit_Avana_g1"]["M10"] = 0.26
    gaps["omit_KY_g0"]["M11"] = 0.25
    _, summary = summarize_robustness(_gap_records(), gaps)
    assert summary["unique_baseline_unflagged_becoming_flagged"] == 2
    assert summary["total_unflagged_to_flagged_transitions"] == 3
    assert summary["possible_unflagged_configuration_transitions"] == 216


def test_large_lfc_extractor_handles_quoted_sequence_header(tmp_path, monkeypatch) -> None:
    path = tmp_path / "lfc.csv"
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["", "sequence,one", "sequence-two"])
        writer.writerow(["guide-a", "1.5", "-2.0"])
        writer.writerow(["guide-b", "9.0", "8.0"])
    import candrel.wrn_guide_loo as module

    raw = path.read_bytes()
    expected = {"size": len(raw), "md5": __import__("hashlib").md5(raw).hexdigest()}
    monkeypatch.setitem(module.EXPECTED_LFC, "Avana", expected)
    values, receipt = extract_lfc_values(
        path, "Avana", ["guide-a"], {"sequence,one", "sequence-two"}
    )
    assert values["guide-a"]["sequence,one"] == 1.5
    assert values["guide-a"]["sequence-two"] == -2.0
    assert receipt["guide_rows"] == 1
