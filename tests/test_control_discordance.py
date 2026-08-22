from __future__ import annotations

from argparse import Namespace

import numpy as np
import pytest

import candrel.control_discordance as module
from candrel.control_discordance import (
    DenominatorRecord,
    ExposureRecord,
    GeneEligibility,
    assess_adequacy,
    depletion_percentiles,
)


def test_depletion_percentile_direction_and_full_denominator() -> None:
    denominators = [
        DenominatorRecord(f"M{i}", "Large Intestine", "Avana", f"S{i}")
        for i in range(3)
    ]
    values = np.asarray([[-3.0], [-2.0], [-1.0]])
    percentiles = depletion_percentiles(values, denominators)
    assert percentiles[:, 0].tolist() == [1.0, 0.5, 0.0]


def _exposure_rows(distinct: int = 17) -> list[ExposureRecord]:
    return [
        ExposureRecord(
            model_id=f"{tissue}-{index}",
            tissue=tissue,
            common_essential_exposure=float(index % distinct),
            nonessential_exposure=float(index % distinct),
        )
        for tissue in ("Large Intestine", "Ovary")
        for index in range(17)
    ]


def _ledger(essential: int = 996, nonessential: int = 584) -> list[GeneEligibility]:
    return [
        GeneEligibility("common_essential", f"E{i}", 1, True, True, "")
        for i in range(essential)
    ] + [
        GeneEligibility("nonessential", f"N{i}", 1, True, True, "")
        for i in range(nonessential)
    ]


def test_adequacy_requires_ten_distinct_exposures() -> None:
    assert assess_adequacy(_exposure_rows(10), _ledger())["overall_adequate"]
    assert not assess_adequacy(_exposure_rows(9), _ledger())["overall_adequate"]


def test_adequacy_keeps_panel_gene_gates_separate() -> None:
    result = assess_adequacy(_exposure_rows(), _ledger(995, 584))
    assert not result["panels"]["common_essential"]["gene_count_adequate"]
    assert result["panels"]["nonessential"]["gene_count_adequate"]
    assert not result["overall_adequate"]


def test_percentile_ties_use_average_midranks() -> None:
    denominators = [
        DenominatorRecord(f"M{i}", "Large Intestine", "Avana", f"S{i}")
        for i in range(3)
    ]
    values = np.asarray([[-2.0], [-2.0], [-1.0]])
    percentiles = depletion_percentiles(values, denominators)
    assert percentiles[:, 0].tolist() == pytest.approx([0.75, 0.75, 0.0])


def test_adequacy_failure_never_touches_outcome(monkeypatch: pytest.MonkeyPatch) -> None:
    exposures = _exposure_rows(distinct=1)
    ledger = _ledger()
    monkeypatch.setattr(module, "verify_pre_outcome_hashes", lambda args: {})
    monkeypatch.setattr(module, "load_cohort", lambda path: {})
    monkeypatch.setattr(module, "load_denominators", lambda path: [])
    monkeypatch.setattr(module, "load_control_list", lambda path: [])
    monkeypatch.setattr(
        module,
        "load_control_scores",
        lambda path, denominators, panels: (np.empty((0, 0)), [], ledger),
    )
    monkeypatch.setattr(module, "depletion_percentiles", lambda matrix, rows: matrix)
    monkeypatch.setattr(
        module,
        "build_exposures",
        lambda cohort, denominators, percentiles, genes, rows: exposures,
    )
    monkeypatch.setattr(module, "write_dataclasses", lambda path, rows: None)
    monkeypatch.setattr(
        module,
        "sha256",
        lambda path: (_ for _ in ()).throw(AssertionError("outcome was touched")),
    )
    args = Namespace(
        cohort_file="cohort",
        denominator_file="denominator",
        score_file="scores",
        essential_file="essential",
        nonessential_file="nonessential",
        gap_file="forbidden_outcome",
        gene_output="genes",
        model_output="models",
    )
    result = module.run(args)
    assert result["status"] == "FAIL_T0_CONTROL_EXPOSURE_ADEQUACY"
    assert result["outcome_hash_verified"] is False
    assert result["outcome_values_loaded"] is False
    assert result["association_computed"] is False
