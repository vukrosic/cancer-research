import numpy as np

from candrel.processing_sensitivity import evaluate, paired_by_model, summarize_gene


def record(model: str, source: str, h: float, b: float, raw_bf: float | None = None) -> dict:
    return {
        "attributes": {
            "source": source,
            "fc_clean_qn": h,
            "bf_scaled": b,
            "bf": b if raw_bf is None else raw_bf,
            "qc_pass": True,
        },
        "relationships": {"model": {"data": {"id": model}}},
    }


def test_paired_by_model_is_field_specific_and_collapses_duplicates():
    records = [
        record("M1", "Broad", -1.0, 2.0),
        record("M1", "Broad", -0.8, 4.0),
        record("M1", "Sanger", -0.7, 3.0),
        record("M2", "Broad", 0.0, 0.0),
    ]
    assert paired_by_model(records, "fc_clean_qn") == {"M1": (-0.9, -0.7)}
    assert paired_by_model(records, "bf_scaled") == {"M1": (3.0, 3.0)}


def test_summarize_gene_detects_higher_harmonized_agreement():
    records = []
    rng = np.random.default_rng(7)
    for i in range(120):
        latent = i / 20
        records.extend(
            [
                record(f"M{i}", "Broad", latent, rng.normal(), rng.normal()),
                record(f"M{i}", "Sanger", latent + rng.normal(scale=0.01), rng.normal(), rng.normal()),
            ]
        )
    result = summarize_gene("TEST", records, seed=8, repeats=50)
    assert result["eligible"] is True
    assert result["spearman_fc_clean_qn"] > 0.99
    assert result["delta_rho_fc_clean_qn_minus_bf_scaled"] > 0.8


def test_evaluate_requires_both_effect_gates_and_all_eight_genes():
    genes = [
        {"eligible": True, "delta_rho_fc_clean_qn_minus_bf_scaled": d}
        for d in [0.20, 0.18, 0.16, 0.14, 0.12, 0.10, -0.01, -0.02]
    ]
    aggregate, gates = evaluate(genes)
    assert aggregate["genes_with_positive_delta"] == 6
    assert aggregate["median_delta_rho"] == 0.13
    assert all(gates.values())
