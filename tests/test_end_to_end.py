import json

import numpy as np

from candrel.smoke import PANEL, run


def test_fixture_backed_end_to_end_gate(tmp_path):
    cache = tmp_path / "data" / "raw" / "cell_model_passports"
    cache.mkdir(parents=True)
    for gene_index, symbol in enumerate(PANEL):
        gene_id = f"GENE{gene_index}"
        gene_payload = {
            "data": [{"id": gene_id, "attributes": {"symbol": symbol}}],
            "meta": {"count": 1},
        }
        (cache / f"gene_{symbol}.json").write_text(json.dumps(gene_payload, sort_keys=True))

        records = []
        base = np.linspace(-2.0, 1.0, 120)
        for model_index, score in enumerate(base):
            model = f"MODEL{model_index:03d}"
            for source, value in (("Broad", score), ("Sanger", score * 0.9 + 0.01)):
                records.append(
                    {
                        "attributes": {
                            "fc_clean_qn": float(value),
                            "qc_pass": True,
                            "source": source,
                        },
                        "relationships": {"model": {"data": {"id": model}}},
                    }
                )
        score_payload = {"data": records, "meta": {"count": len(records)}}
        score_path = cache / f"crispr_full_v2_{symbol}_{gene_id}.json"
        score_path.write_text(json.dumps(score_payload, sort_keys=True))

    result = run(tmp_path, repeats=20)
    assert result["status"] == "PASS"
    assert result["aggregate"]["eligible_genes"] == 8
    assert result["aggregate"]["median_spearman"] > 0.99
