from __future__ import annotations

import pytest

from candrel.wrn_guide_mutation_adequacy import (
    ModelExposure,
    build_exposures,
    exposure_adequacy,
)


def test_build_exposures_uses_library_specific_denominators() -> None:
    rows = build_exposures(
        {"M1": "Large Intestine"}, {"M1": 1}, {"M1": 2}, 4, 5
    )
    assert rows[0].avana_fraction == 0.25
    assert rows[0].ky_fraction == 0.4
    assert rows[0].absolute_fraction_difference == pytest.approx(0.15)


def _row(model: str, tissue: str, exposure: float) -> ModelExposure:
    return ModelExposure(
        model_id=model,
        tissue=tissue,
        avana_mutated_guides=0,
        avana_total_guides=4,
        avana_fraction=0.0,
        ky_mutated_guides=0,
        ky_total_guides=5,
        ky_fraction=0.0,
        absolute_fraction_difference=exposure,
    )


def test_constant_exposure_fails_before_association() -> None:
    rows = [
        _row(f"{tissue}-{index}", tissue, 0.0)
        for tissue in ("Large Intestine", "Ovary")
        for index in range(17)
    ]
    result = exposure_adequacy(rows)
    assert result["adequate_for_association"] is False
    assert all(
        tissue["unique_exposure_values"] == 1
        for tissue in result["by_tissue"].values()
    )


def test_nonconstant_exposure_and_counts_pass_gate() -> None:
    rows = [
        _row(f"{tissue}-{index}", tissue, float(index % 2))
        for tissue in ("Large Intestine", "Ovary")
        for index in range(17)
    ]
    assert exposure_adequacy(rows)["adequate_for_association"] is True
