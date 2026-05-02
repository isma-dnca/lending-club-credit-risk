import pandas as pd

from lending_club_credit_risk.features.preprocess import (
    basic_cleaning,
    engineer_emp_length,
    engineer_issue_date_features,
    engineer_ratio_features,
    split_target,
)


def test_basic_cleaning_normalizes_columns_and_drops_duplicates():
    df = pd.DataFrame(
        [
            {" Loan_Amnt ": 1000, "default": 0},
            {" Loan_Amnt ": 1000, "default": 0},
        ]
    )

    cleaned = basic_cleaning(df)

    assert cleaned.shape[0] == 1
    assert list(cleaned.columns) == ["loan_amnt", "default"]


def test_split_target_returns_X_and_y():
    df = pd.DataFrame(
        {
            "loan_amnt": [1000, 2000],
            "default": [0, 1],
        }
    )

    X, y = split_target(df, target_column="default")

    assert "default" not in X.columns
    assert y.tolist() == [0, 1]


def test_engineer_issue_date_features_adds_year_and_month():
    df = pd.DataFrame(
        {
            "issue_d": ["Jan-2020", "Feb-2021"],
        }
    )

    transformed = engineer_issue_date_features(df)

    assert "issue_d" not in transformed.columns
    assert transformed["issue_year"].tolist() == [2020, 2021]
    assert transformed["issue_month"].tolist() == [1, 2]


def test_engineer_emp_length_maps_text_to_numeric():
    df = pd.DataFrame(
        {
            "emp_length": ["< 1 year", "10+ years"],
        }
    )

    transformed = engineer_emp_length(df)

    assert "emp_length" not in transformed.columns
    assert transformed["emp_length_num"].tolist() == [0, 10]


def test_engineer_ratio_features_creates_expected_columns():
    df = pd.DataFrame(
        {
            "loan_amnt": [1000],
            "revenue": [5000],
            "fico_n": [700],
        }
    )

    transformed = engineer_ratio_features(df)

    assert {"loan_to_revenue", "loan_to_fico", "revenue_to_fico"} <= set(
        transformed.columns
    )