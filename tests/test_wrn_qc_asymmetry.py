from __future__ import annotations

import numpy as np
import pytest

from candrel.wrn_qc_asymmetry import (
    AssociationRecord,
    IntegrityError,
    bootstrap_interval,
    estimate_from_arrays,
    frozen_rank_arrays,
    permutation_pvalue,
    quality_transform,
    verify_screen_identity,
)


def _rows(reverse_ovary: bool = False) -> list[AssociationRecord]:
    rows = []
    for tissue in ("Large Intestine", "Ovary"):
        for index in range(17):
            gap = index / 16
            composite = (
                (16 - index) / 16 if reverse_ovary and tissue == "Ovary" else gap
            )
            rows.append(
                AssociationRecord(
                    model_id=f"{tissue}-{index}",
                    model_name=f"M{index}",
                    tissue=tissue,
                    label="MSI" if index < 5 else "MSS",
                    avana_screen_id=f"A-{tissue}-{index}",
                    ky_screen_id=f"K-{tissue}-{index}",
                    wrn_percentile_gap=gap,
                    exp005_gap_flag=gap >= 0.25,
                    nnmd_asymmetry=composite,
                    rocauc_asymmetry=composite,
                    fpr_asymmetry=composite,
                    essential_depletion_asymmetry=composite,
                    nonessential_depletion_asymmetry=composite,
                    qc_rank_asymmetry_composite=composite,
                )
            )
    return rows


def test_quality_metric_directions() -> None:
    assert quality_transform("ScreenNNMD", -5.0) == 5.0
    assert quality_transform("ScreenROCAUC", 0.9) == 0.9
    assert quality_transform("ScreenFPR", 0.1) == -0.1
    assert quality_transform("ScreenMedianEssentialDepletion", -0.8) == 0.8
    assert quality_transform("ScreenMedianNonessentialDepletion", -0.1) == -0.1


def test_equal_tissue_estimate() -> None:
    theta, tissue = estimate_from_arrays(
        frozen_rank_arrays(_rows(reverse_ovary=True), "qc_rank_asymmetry_composite")
    )
    assert tissue["Large Intestine"] == pytest.approx(1.0)
    assert tissue["Ovary"] == pytest.approx(-1.0)
    assert theta == pytest.approx(0.0)


def test_strong_permutation_signal() -> None:
    arrays = frozen_rank_arrays(_rows(), "qc_rank_asymmetry_composite")
    theta, _ = estimate_from_arrays(arrays)
    p_value = permutation_pvalue(arrays, theta, 500, np.random.default_rng(6))
    assert theta == pytest.approx(1.0)
    assert p_value < 0.01


def test_bootstrap_keeps_frozen_ranks() -> None:
    arrays = frozen_rank_arrays(_rows(), "qc_rank_asymmetry_composite")
    first = bootstrap_interval(arrays, 100, np.random.default_rng(8))
    second = bootstrap_interval(arrays, 100, np.random.default_rng(8))
    assert first == second == pytest.approx((1.0, 1.0))


def test_unknown_metric_rejected() -> None:
    with pytest.raises(IntegrityError):
        quality_transform("WRN", 1.0)


def test_frozen_screen_identity_drift_rejected() -> None:
    verify_screen_identity(("ACH-1", "Avana"), "SC-1", "SC-1")
    with pytest.raises(IntegrityError, match="screen identity drift"):
        verify_screen_identity(("ACH-1", "Avana"), "SC-2", "SC-1")
