import json

from lending_club_credit_risk.persistence.save_artifacts import save_metrics


def test_save_metrics_creates_parent_dirs(tmp_path):
    output_path = tmp_path / "reports" / "metrics.json"

    save_metrics({"roc_auc": 0.75}, output_path)

    assert output_path.exists()
    assert json.loads(output_path.read_text(encoding="utf-8"))["roc_auc"] == 0.75
