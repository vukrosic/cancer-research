from __future__ import annotations

import argparse

import pytest

from candrel.wrn_sequence_semantics import (
    IntegrityError,
    PARENT_MISMATCHES,
    ReconstructionLedgerRow,
    build_parser,
    parse_canonical_bool,
    parse_nonnegative_integer,
    summarize_mismatches,
)


def _row(model: str, source: str, passes: bool) -> ReconstructionLedgerRow:
    return ReconstructionLedgerRow(
        screen_id=f"S-{model}-{source}",
        model_id=model,
        source=source,
        tissue="Ovary",
        n_passing_sequences=2,
        n_included_sequences=3,
        retained_sequence_count=2,
        reconstructed_score=-1.0,
        official_score=-1.0 if passes else -1.1,
        absolute_discrepancy=0.0 if passes else 0.1,
        passes_absolute_1e_8_gate=passes,
    )


def test_boolean_parser_rejects_noncanonical_values() -> None:
    assert parse_canonical_bool("True", "id") is True
    assert parse_canonical_bool("False", "id") is False
    for value in ("true", "FALSE", "", "1"):
        with pytest.raises(IntegrityError, match="noncanonical boolean"):
            parse_canonical_bool(value, "id")


def test_qc_count_requires_nonnegative_integer() -> None:
    assert parse_nonnegative_integer("2", "id") == 2
    for value in ("-1", "1.5", "nan", ""):
        with pytest.raises(IntegrityError):
            parse_nonnegative_integer(value, "id")


def test_parent_comparison_distinguishes_resolved_persistent_and_new() -> None:
    parent = sorted(PARENT_MISMATCHES)
    rows = [
        _row(parent[0][0], parent[0][1], False),
        _row(parent[1][0], parent[1][1], True),
        _row(parent[2][0], parent[2][1], True),
        _row("NEW", "KY", False),
    ]
    result = summarize_mismatches(rows)
    assert result["resolved_parent_mismatch_count"] == 2
    assert result["persistent_parent_mismatch_count"] == 1
    assert result["newly_introduced_mismatch_count"] == 1


def test_cli_has_no_gap_or_omission_arguments() -> None:
    parser = build_parser()
    destinations = {action.dest for action in parser._actions}
    assert all("gap" not in destination for destination in destinations)
    assert all("omit" not in destination for destination in destinations)
