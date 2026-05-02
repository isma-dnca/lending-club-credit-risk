## instead of training a real model here, we will just create a dummy model that always predicts the same value.
# That has only one method: predict_proba(..). This way, we can test the evaluation function without needing to train a real model.

import numpy as np
import pandas as pd

from lending_club_credit_risk.modeling.evaluate import evaluate_model


class DummyModel:
    def predict_proba(self, X):
        return np.array(
            [
                [0.8, 0.2],
                [0.1, 0.9],
                [0.6, 0.4],
                [0.2, 0.8],
            ]
        )


def test_evaluate_model_returns_expected_keys():
    model = DummyModel()
    X_test = pd.DataFrame({"x": [1, 2, 3, 4]})
    y_test = np.array([0, 1, 0, 1])

    metrics = evaluate_model(model, X_test, y_test, threshold=0.5)

    assert {
        "roc_auc",
        "accuracy",
        "precision",
        "recall",
        "f1",
        "confusion_matrix",
        "classification_report",
        "threshold",
    } <= set(metrics.keys())

    assert metrics["threshold"] == 0.5
    assert 0.0 <= metrics["roc_auc"] <= 1.0