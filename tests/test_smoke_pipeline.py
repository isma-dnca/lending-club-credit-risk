from pathlib import Path

import pandas as pd

from lending_club_credit_risk.modeling.evaluate import evaluate_model
from lending_club_credit_risk.modeling.train import train_lightgbm_model
from lending_club_credit_risk.pipeline.train_pipeline import run_training_pipeline


def _write_mock_dataset(path: Path) -> Path:
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


def test_smoke_end_to_end(tmp_path):
    raw_data_file = _write_mock_dataset(tmp_path / "mini_loans.csv")

    X_train_processed, X_test_processed, y_train, y_test, preprocessor = run_training_pipeline(
        raw_data_file=raw_data_file,
        test_size=0.2,
        target_column="default",
    )

    model = train_lightgbm_model(X_train_processed, y_train)
    metrics = evaluate_model(model, X_test_processed, y_test, threshold=0.5)

    assert X_train_processed.shape[0] > 0
    assert X_test_processed.shape[0] > 0
    assert preprocessor is not None
    assert 0.0 <= metrics["roc_auc"] <= 1.0