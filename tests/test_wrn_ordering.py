from __future__ import annotations

import numpy as np
import pytest

from candrel.wrn_ordering import (
    IntegrityError,
    PairRecord,
    bootstrap_interval,
    dependency_percentiles,
    fixed_percentile_correlation,
    kendall_pair_concordance,
    permutation_pvalue,
    primary_estimate,
)


def _pairs(reverse_ovary: bool = False) -> list[PairRecord]:
    pairs = []
    for tissue in ("Large Intestine", "Ovary"):
        for index in range(17):
            avana = index / 16
            ky = (16 - index) / 16 if tissue == "Ovary" and reverse_ovary else avana
            pairs.append(
                PairRecord(
                    model_id=f"{tissue}-{index}",
                    model_name=f"M{index}",
                    tissue=tissue,
                    label="MSI" if index < 5 else "MSS",
                    avana_score=-avana,
                    ky_score=-ky,
                    avana_percentile=avana,
                    ky_percentile=ky,
                    absolute_percentile_gap=abs(avana - ky),
                    discordant_ge_0_25=abs(avana - ky) >= 0.25,
                )
            )
    return pairs


def test_dependency_percentiles_direction_and_ties() -> None:
    result = dependency_percentiles([-2.0, -1.0, -1.0, 0.0])
    assert result[0] == 1.0
    assert result[-1] == 0.0
    assert result[1] == result[2] == 0.5


def test_primary_equal_tissue_mean() -> None:
    theta, tissues = primary_estimate(_pairs(reverse_ovary=True))
    assert tissues["Large Intestine"] == pytest.approx(1.0)
    assert tissues["Ovary"] == pytest.approx(-1.0)
    assert theta == pytest.approx(0.0)


def test_permutation_strong_signal_is_significant() -> None:
    pairs = _pairs()
    theta, _ = primary_estimate(pairs)
    p_value = permutation_pvalue(pairs, theta, 500, np.random.default_rng(3))
    assert theta == pytest.approx(1.0)
    assert p_value < 0.01


def test_bootstrap_is_seed_deterministic() -> None:
    first = bootstrap_interval(_pairs(), 100, np.random.default_rng(4))
    second = bootstrap_interval(_pairs(), 100, np.random.default_rng(4))
    assert first == second == pytest.approx((1.0, 1.0))


def test_fixed_percentile_bootstrap_does_not_rerank_duplicates() -> None:
    avana = np.asarray([0.0, 0.0, 0.2, 1.0])
    ky = np.asarray([0.0, 0.0, 0.8, 1.0])
    fixed = fixed_percentile_correlation(avana, ky)
    reranked = float(__import__("scipy").stats.spearmanr(avana, ky).statistic)
    assert fixed == pytest.approx(0.8252740455)
    assert fixed != pytest.approx(reranked)


def test_kendall_pair_concordance_extremes() -> None:
    strong = kendall_pair_concordance(_pairs())
    mixed = kendall_pair_concordance(_pairs(reverse_ovary=True))
    assert strong["pooled_concordance_minus_discordance"] == 1.0
    assert mixed["pooled_concordance_minus_discordance"] == 0.0


def test_percentiles_require_multiple_finite_values() -> None:
    with pytest.raises(IntegrityError):
        dependency_percentiles([1.0])
    with pytest.raises(IntegrityError):
        dependency_percentiles([1.0, float("nan")])
