from sklearn.model_selection import train_test_split

from src.config import RANDOM_STATE
from src.data.load import load_raw_data
from src.features.preprocess import (
    basic_cleaning,
    engineer_emp_length,
    engineer_issue_date_features,
    engineer_ratio_features,
    split_target,
)
from src.features.preprocessor import build_preprocessor


TARGET_COLUMN = "default"
RAW_DATA_FILENAME = "LC_loans_granting_model_dataset.csv"
COLUMNS_TO_DROP = ["id", "title", "desc", "zip_code"]
TEST_SIZE = 0.2


def run_training_pipeline():
    """
    Run the preprocessing part of the training pipeline.

    Steps
    -----
    1. Load raw data
    2. Apply deterministic transformations
    3. Split features and target
    4. Drop excluded columns
    5. Split train/test
    6. Identify numeric and categorical columns from X_train
    7. Build preprocessor
    8. Fit preprocessor on X_train only
    9. Transform X_train and X_test

    Returns
    -------
    tuple
        X_train_processed, X_test_processed, y_train, y_test, preprocessor
    """
    # 1. Load raw data
    df = load_raw_data(RAW_DATA_FILENAME)

    # 2. Apply deterministic transformations
    df = basic_cleaning(df)
    df = engineer_issue_date_features(df)
    df = engineer_emp_length(df)
    df = engineer_ratio_features(df)

    # 3. Split features and target
    X, y = split_target(df, target_column=TARGET_COLUMN)

    # 4. Drop excluded columns from X only
    X = X.drop(columns=COLUMNS_TO_DROP, errors="ignore")

    # 5. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    # 6. Identify numeric and categorical columns from X_train
    numeric_features = X_train.select_dtypes(include=["number"]).columns.tolist()
    categorical_features = X_train.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    # 7. Build preprocessor
    preprocessor = build_preprocessor(numeric_features, categorical_features)

    # 8. Fit on X_train only, then transform train and test
    # After ColumnTransformer, the transformed outputs may no longer be pandas DataFrames.
    # Depending on the transformers used, they may become NumPy arrays or sparse matrices.

    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)

    return X_train_processed, X_test_processed, y_train, y_test, preprocessor
