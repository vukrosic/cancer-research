from __future__ import annotations

import json

import pytest

from candrel import wrn_process_association as module


def test_percentile_formula_uses_average_midrank(monkeypatch: pytest.MonkeyPatch) -> None:
    denominators = [
        module.Denominator("M1", "M1", "Ovary", "MSS", "Avana", "S1"),
        module.Denominator("M2", "M2", "Ovary", "MSS", "Avana", "S2"),
        module.Denominator("M3", "M3", "Ovary", "MSS", "Avana", "S3"),
    ]
    values = {("M1", "Avana"): 1.0, ("M2", "Avana"): 1.0, ("M3", "Avana"): 3.0}
    monkeypatch.setattr(module, "EXPECTED_DENOMINATORS", {("Avana", "Ovary"): 3})
    result = module.within_stratum_percentiles(denominators, values)
    assert result[("M1", "Avana")] == pytest.approx(0.25)
    assert result[("M2", "Avana")] == pytest.approx(0.25)
    assert result[("M3", "Avana")] == pytest.approx(1.0)


def test_tied_exposure_gate_rejects_large_tie() -> None:
    with pytest.raises(module.IntegrityError, match="largest_tie"):
        module.tied_exposure_gate([0.1] * 9 + [0.2] * 8, "Ovary", "efficacy")


def test_summary_digest_normalizes_self_receipt() -> None:
    result = {"artifact_receipt_sha256": {name: "" for name in module.EXPECTED_RESULT_FILES}}
    digest = module.summary_digest(result)
    result["artifact_receipt_sha256"]["summary.json"] = digest
    assert module.summary_digest(result) == digest


def test_parser_uses_exp013_paths() -> None:
    args = module.build_parser().parse_args([])
    assert "EXP-20260822-013" in args.results_dir
    assert "EXP-20260822-005" in args.outcome_file
