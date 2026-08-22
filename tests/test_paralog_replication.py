from __future__ import annotations

import pytest

from candrel.paralog_replication import delta_from_scores, summary_digest


def test_delta_counts_lower_scores_as_negative_and_ties_as_zero() -> None:
    groups = {"Lung": {"damaging": ["d1", "d2"], "intact": ["i1", "i2"]}}
    scores = {"d1": -2.0, "d2": 0.0, "i1": -1.0, "i2": 0.0}
    delta, lineage, pair_count = delta_from_scores(groups, scores)
    assert pair_count == 4
    assert delta == pytest.approx(-0.25)
    assert lineage["Lung"] == pytest.approx(-0.25)


def test_delta_rejects_zero_comparison_population() -> None:
    groups = {"Lung": {"damaging": ["d1"], "intact": []}}
    with pytest.raises(RuntimeError, match="zero pair denominator"):
        delta_from_scores(groups, {"d1": -1.0})


def test_summary_digest_normalizes_self_receipt() -> None:
    result = {"artifact_receipt_sha256": {name: "" for name in {
        "context_ledger.csv", "design_sensitivity.csv", "endpoint_scores.csv", "inference.csv", "summary.json"
    }}}
    digest = summary_digest(result)
    result["artifact_receipt_sha256"]["summary.json"] = digest
    assert summary_digest(result) == digest
