import joblib

from fastapi.testclient import TestClient

from lending_club_credit_risk.api.app import create_app
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline
from tests.test_inference import _write_training_dataset


def test_health_endpoint_returns_ok():
    """
    Test that the /health endpoint returns a 200 status code and the expected response.
    """
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint_returns_prediction(tmp_path):
    """
    Test that the /predict endpoint returns a valid prediction response.
    """
    train_file = _write_training_dataset(tmp_path / "train.csv")

    X_train_processed, _, y_train, _, preprocessor = run_training_pipeline(
        raw_data_file=train_file,
        test_size=0.2,
        target_column="default",
    )
    model = train_lightgbm_model(X_train_processed, y_train)

    model_path = tmp_path / "model.joblib"
    preprocessor_path = tmp_path / "preprocessor.joblib"

    joblib.dump(model, model_path)
    joblib.dump(preprocessor, preprocessor_path)

    app = create_app(
        model_path=model_path,
        preprocessor_path=preprocessor_path,
    )
    client = TestClient(app)

    payload = {
        "id": 101,
        "title": "Loan for car",
        "desc": "I need a loan to buy a car.",
        "zip_code": "12345",
        "issue_d": "Nov-2020",
        "emp_length": "5 years",
        "loan_amnt": 10000.0,
        "revenue": 50000.0,
        "fico_n": 700.0,
        "purpose": "car",
        "addr_state": "CA",
        "home_ownership_n": 1,
        "dti_n": 10.0,
        "experience_c": 5,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == 101
    assert "default_probability" in response_data
    assert "predicted_default" in response_data
    assert response_data["predicted_default"] in [0, 1]


def test_predict_endpoint_rejects_missing_required_field():
    """
    Test that the /predict endpoint returns a validation error when a required field is missing.
    """
    app = create_app()
    client = TestClient(app)

    invalid_payload = {
        "id": 101,
        "title": "Loan for car",
        "desc": "I need a loan to buy a car.",
        "zip_code": "12345",
        "issue_d": "Nov-2020",
        "emp_length": "5 years",
        "revenue": 50000.0,
        "fico_n": 700.0,
        "purpose": "car",
        "addr_state": "CA",
        "home_ownership_n": 1,
        "dti_n": 10.0,
        "experience_c": 5,
    }

    response = client.post("/predict", json=invalid_payload)

    assert response.status_code == 422    