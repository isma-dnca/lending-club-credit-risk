from __future__ import annotations

from pathlib import Path
from typing import Sequence

from sklearn.model_selection import train_test_split

from lending_club_credit_risk.config import (
    COLUMNS_TO_DROP,
    RANDOM_STATE,
    RAW_DATA_FILE,
    TARGET_COLUMN,
    TEST_SIZE,
)
from lending_club_credit_risk.data.load import load_raw_data
from lending_club_credit_risk.features.preprocess import (
    basic_cleaning,
    engineer_emp_length,
    engineer_issue_date_features,
    engineer_ratio_features,
    split_target,
)
from lending_club_credit_risk.features.preprocessor import build_preprocessor


def run_training_pipeline(
    raw_data_file: str | Path = RAW_DATA_FILE,
    target_column: str = TARGET_COLUMN,
    test_size: float = TEST_SIZE,
    columns_to_drop: Sequence[str] = COLUMNS_TO_DROP,
):
    """
    Run the preprocessing part of the training pipeline.

    Parameters
    ----------
    raw_data_file : str or Path
        Path to the raw dataset file.
    target_column : str
        Name of the target column.
    test_size : float
        Proportion of the dataset used for the test split.
    columns_to_drop : Sequence[str]
        Columns excluded from modeling.

    Returns
    -------
    tuple
        X_train_processed, X_test_processed, y_train, y_test, preprocessor
    """
    df = load_raw_data(raw_data_file)

    df = basic_cleaning(df)
    df = engineer_issue_date_features(df)
    df = engineer_emp_length(df)
    df = engineer_ratio_features(df)

    X, y = split_target(df, target_column=target_column)
    X = X.drop(columns=list(columns_to_drop), errors="ignore")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    numeric_features = X_train.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X_train.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    preprocessor = build_preprocessor(numeric_features, categorical_features)

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor
