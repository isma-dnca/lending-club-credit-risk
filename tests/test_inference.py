from pathlib import Path

import joblib
import pandas as pd

from lending_club_credit_risk.inference.predict import predict_from_csv
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline


def _write_training_dataset(path: Path) -> Path:
    df = pd.DataFrame(
        [
            {
                "id": 1,
                "title": "a",
                "desc": "x",
                "zip_code": "100xx",
                "issue_d": "Jan-2020",
                "emp_length": "1 year",
                "loan_amnt": 1000,
                "revenue": 5000,
                "fico_n": 720,
                "purpose": "debt_consolidation",
                "addr_state": "CA",
                "home_ownership_n": 1,
                "dti_n": 10.5,
                "experience_c": 2,
                "default": 0,
            },
            {
                "id": 2,
                "title": "b",
                "desc": "x",
                "zip_code": "101xx",
                "issue_d": "Feb-2020",
                "emp_length": "2 years",
                "loan_amnt": 1200,
                "revenue": 4500,
                "fico_n": 690,
                "purpose": "credit_card",
                "addr_state": "NY",
                "home_ownership_n": 2,
                "dti_n": 14.0,
                "experience_c": 3,
                "default": 1,
            },
            {
                "id": 3,
                "title": "c",
                "desc": "x",
                "zip_code": "102xx",
                "issue_d": "Mar-2020",
                "emp_length": "3 years",
                "loan_amnt": 1500,
                "revenue": 6000,
                "fico_n": 710,
                "purpose": "small_business",
                "addr_state": "TX",
                "home_ownership_n": 1,
                "dti_n": 11.2,
                "experience_c": 4,
                "default": 0,
            },
            {
                "id": 4,
                "title": "d",
                "desc": "x",
                "zip_code": "103xx",
                "issue_d": "Apr-2020",
                "emp_length": "4 years",
                "loan_amnt": 1800,
                "revenue": 3000,
                "fico_n": 660,
                "purpose": "moving",
                "addr_state": "FL",
                "home_ownership_n": 3,
                "dti_n": 18.0,
                "experience_c": 5,
                "default": 1,
            },
            {
                "id": 5,
                "title": "e",
                "desc": "x",
                "zip_code": "104xx",
                "issue_d": "May-2020",
                "emp_length": "5 years",
                "loan_amnt": 2000,
                "revenue": 7000,
                "fico_n": 730,
                "purpose": "car",
                "addr_state": "CA",
                "home_ownership_n": 1,
                "dti_n": 9.4,
                "experience_c": 6,
                "default": 0,
            },
            {
                "id": 6,
                "title": "f",
                "desc": "x",
                "zip_code": "105xx",
                "issue_d": "Jun-2020",
                "emp_length": "6 years",
                "loan_amnt": 2200,
                "revenue": 3500,
                "fico_n": 650,
                "purpose": "vacation",
                "addr_state": "NV",
                "home_ownership_n": 1,
                "dti_n": 20.0,
                "experience_c": 7,
                "default": 1,
            },
            {
                "id": 7,
                "title": "g",
                "desc": "x",
                "zip_code": "106xx",
                "issue_d": "Jul-2020",
                "emp_length": "7 years",
                "loan_amnt": 2400,
                "revenue": 8000,
                "fico_n": 740,
                "purpose": "home_improvement",
                "addr_state": "WA",
                "home_ownership_n": 2,
                "dti_n": 8.0,
                "experience_c": 8,
                "default": 0,
            },
            {
                "id": 8,
                "title": "h",
                "desc": "x",
                "zip_code": "107xx",
                "issue_d": "Aug-2020",
                "emp_length": "8 years",
                "loan_amnt": 2600,
                "revenue": 3200,
                "fico_n": 645,
                "purpose": "medical",
                "addr_state": "AZ",
                "home_ownership_n": 1,
                "dti_n": 21.0,
                "experience_c": 9,
                "default": 1,
            },
            {
                "id": 9,
                "title": "i",
                "desc": "x",
                "zip_code": "108xx",
                "issue_d": "Sep-2020",
                "emp_length": "9 years",
                "loan_amnt": 2800,
                "revenue": 9000,
                "fico_n": 750,
                "purpose": "debt_consolidation",
                "addr_state": "OR",
                "home_ownership_n": 3,
                "dti_n": 7.5,
                "experience_c": 10,
                "default": 0,
            },
            {
                "id": 10,
                "title": "j",
                "desc": "x",
                "zip_code": "109xx",
                "issue_d": "Oct-2020",
                "emp_length": "10+ years",
                "loan_amnt": 3000,
                "revenue": 2800,
                "fico_n": 640,
                "purpose": "major_purchase",
                "addr_state": "UT",
                "home_ownership_n": 1,
                "dti_n": 23.0,
                "experience_c": 11,
                "default": 1,
            },
        ]
    )

    df.to_csv(path, index=False)
    return path


def _write_inference_dataset(path: Path) -> Path:
    df = pd.DataFrame(
        [
            {
                "id": 101,
                "title": "k",
                "desc": "x",
                "zip_code": "200xx",
                "issue_d": "Nov-2020",
                "emp_length": "2 years",
                "loan_amnt": 1600,
                "revenue": 5500,
                "fico_n": 705,
                "purpose": "credit_card",
                "addr_state": "CA",
                "home_ownership_n": 1,
                "dti_n": 12.0,
                "experience_c": 3,
            },
            {
                "id": 102,
                "title": "l",
                "desc": "x",
                "zip_code": "201xx",
                "issue_d": "Dec-2020",
                "emp_length": "7 years",
                "loan_amnt": 2500,
                "revenue": 4000,
                "fico_n": 660,
                "purpose": "medical",
                "addr_state": "NV",
                "home_ownership_n": 2,
                "dti_n": 19.0,
                "experience_c": 8,
            },
        ]
    )

    df.to_csv(path, index=False)
    return path


def test_predict_from_csv_returns_expected_columns(tmp_path):
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

    inference_file = _write_inference_dataset(tmp_path / "inference.csv")

    results = predict_from_csv(
        input_file=inference_file,
        model_path=model_path,
        preprocessor_path=preprocessor_path,
        threshold=0.5,
    )

    assert list(results.columns) == [
        "id",
        "default_probability",
        "predicted_default",
    ]
    assert len(results) == 2
    assert results["id"].tolist() == [101, 102]
    assert results["default_probability"].between(0.0, 1.0).all()
    assert set(results["predicted_default"].tolist()) <= {0, 1}


def test_predict_from_csv_raises_if_model_is_missing(tmp_path):
    train_file = _write_training_dataset(tmp_path / "train.csv")

    X_train_processed, _, y_train, _, preprocessor = run_training_pipeline(
        raw_data_file=train_file,
        test_size=0.2,
        target_column="default",
    )
    _ = train_lightgbm_model(X_train_processed, y_train)

    preprocessor_path = tmp_path / "preprocessor.joblib"
    joblib.dump(preprocessor, preprocessor_path)

    inference_file = _write_inference_dataset(tmp_path / "inference.csv")

    missing_model_path = tmp_path / "missing_model.joblib"

    try:
        predict_from_csv(
            input_file=inference_file,
            model_path=missing_model_path,
            preprocessor_path=preprocessor_path,
        )
        assert False, "Expected FileNotFoundError for missing model artifact"
    except FileNotFoundError:
        pass


def test_predict_from_csv_raises_if_preprocessor_is_missing(tmp_path):
    train_file = _write_training_dataset(tmp_path / "train.csv")

    X_train_processed, _, y_train, _, _ = run_training_pipeline(
        raw_data_file=train_file,
        test_size=0.2,
        target_column="default",
    )
    model = train_lightgbm_model(X_train_processed, y_train)

    model_path = tmp_path / "model.joblib"
    joblib.dump(model, model_path)

    inference_file = _write_inference_dataset(tmp_path / "inference.csv")

    missing_preprocessor_path = tmp_path / "missing_preprocessor.joblib"

    try:
        predict_from_csv(
            input_file=inference_file,
            model_path=model_path,
            preprocessor_path=missing_preprocessor_path,
        )
        assert False, "Expected FileNotFoundError for missing preprocessor artifact"
    except FileNotFoundError:
        pass
