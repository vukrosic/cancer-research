from __future__ import annotations

import numpy as np
import pytest

from candrel.sequence_inclusion_asymmetry import (
    IntegrityError,
    count_percentiles,
    parse_count,
    validate_exposure_adequacy,
    ScreenCountRecord,
)
from candrel.wrn_qc_asymmetry import bootstrap_interval


def test_parse_count_requires_finite_nonnegative_integer() -> None:
    assert parse_count("0", "n", "id") == 0
    assert parse_count("2.0", "n", "id") == 2
    for value in ("-1", "1.5", "nan", ""):
        with pytest.raises(IntegrityError):
            parse_count(value, "n", "id")


def test_count_percentiles_preserve_average_ties() -> None:
    records = []
    counts = {
        ("Avana", "Large Intestine"): [1] * 25,
        ("KY", "Large Intestine"): [1] * 30,
        ("Avana", "Ovary"): [1] * 22,
        ("KY", "Ovary"): [1] * 26,
    }
    counts[("Avana", "Large Intestine")][:3] = [1, 1, 3]
    for (source, tissue), values in counts.items():
        for index, value in enumerate(values):
            records.append(
                ScreenCountRecord(
                    model_id=f"{source}-{tissue}-{index:02d}",
                    tissue=tissue,
                    source=source,
                    screen_id=f"S-{source}-{tissue}-{index:02d}",
                    n_included=value,
                    n_passing=value,
                )
            )
    percentiles = count_percentiles(records, "nIncludedSequences")
    first = percentiles[("Avana-Large Intestine-00", "Avana")]
    second = percentiles[("Avana-Large Intestine-01", "Avana")]
    third = percentiles[("Avana-Large Intestine-02", "Avana")]
    assert first == second
    assert third > first


def test_discrete_exposure_gate_accepts_five_levels_and_tie_of_eight() -> None:
    values = [0.0] * 8 + [0.1] * 3 + [0.2] * 2 + [0.3] * 2 + [0.4] * 2
    result = validate_exposure_adequacy(values, "Ovary", "nIncludedSequences")
    assert result["distinct_exposure_values"] == 5
    assert result["largest_tie"] == 8


def test_discrete_exposure_gate_rejects_four_levels() -> None:
    values = [0.0] * 5 + [0.1] * 4 + [0.2] * 4 + [0.3] * 4
    with pytest.raises(IntegrityError, match="exposure levels"):
        validate_exposure_adequacy(values, "Ovary", "nIncludedSequences")


def test_discrete_exposure_gate_rejects_tie_of_nine() -> None:
    values = [0.0] * 9 + [0.1] * 2 + [0.2] * 2 + [0.3] * 2 + [0.4] * 2
    with pytest.raises(IntegrityError, match="largest tie"):
        validate_exposure_adequacy(values, "Ovary", "nIncludedSequences")


class _DegenerateRng:
    def integers(self, low: int, high: int, size: int) -> np.ndarray:
        return np.zeros(size, dtype=int)


def test_bootstrap_zero_variance_is_not_discarded_or_redrawn() -> None:
    arrays = {
        tissue: (np.arange(17, dtype=float), np.arange(17, dtype=float))
        for tissue in ("Large Intestine", "Ovary")
    }
    with pytest.raises(RuntimeError, match="constant fixed-percentile"):
        bootstrap_interval(arrays, 1, _DegenerateRng())
