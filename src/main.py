from lightgbm import LGBMClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
import pandas as pd

from src.config import RANDOM_STATE
from src.data.load import load_raw_data
from src.features.preprocess import (
    basic_cleaning,
    split_target,
    engineer_issue_date_features,
    engineer_emp_length
)


TARGET_COLUMN = "default"
SAMPLE_SIZE = 200_000
COLUMNS_TO_DROP = ["id", "title", "desc", "zip_code"]

RUN_LOGISTIC = False
RUN_LIGHTGBM = True


def main() -> None:
    # 1. Load and clean raw data
    df = load_raw_data("LC_loans_granting_model_dataset.csv")
    
    df = basic_cleaning(df)

    df = engineer_issue_date_features(df)

    df = engineer_emp_length(df)

    # 2. Sample the dataset to control memory usage on the local machine
    df = df.sample(n=SAMPLE_SIZE, random_state=RANDOM_STATE)

    # 3. Separate features and target
    X, y = split_target(df, target_column=TARGET_COLUMN)

    # 4. Drop non-useful or high-cardinality columns from features only
    X = X.drop(columns=COLUMNS_TO_DROP, errors="ignore")

    # 5. Quick inspection of categorical features before encoding
    cat_cols = X.select_dtypes(include=["object", "string"]).columns

    print(f"Raw X shape: {X.shape}")
    print(f"y shape: {y.shape}")
    print(f"Number of categorical columns: {len(cat_cols)}")

    print("\nCategorical cardinality:")
    for col in cat_cols:
        print(f"{col}: {X[col].nunique()} unique values")

    # 6. Split before encoding to avoid data leakage
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=y,
    )

    # 7. One-hot encode categorical variables
    X_train = pd.get_dummies(X_train, drop_first=True)
    X_test = pd.get_dummies(X_test, drop_first=True)

    # 8. Align encoded train and test sets to ensure identical columns
    X_train, X_test = X_train.align(X_test, join="left", axis=1, fill_value=0)

    print(f"Encoded X_train shape: {X_train.shape}")
    print(
        "Remaining object columns:",
        X_train.select_dtypes(include=["object", "string"]).shape[1],
    )

    # 9. Reduce memory usage
    X_train = X_train.astype("float32")
    X_test = X_test.astype("float32")

    # 10. Logistic Regression
    if RUN_LOGISTIC:
        print("\n==============================")
        print("Logistic Regression")
        print("==============================")

        model = LogisticRegression(
            max_iter=1000,
            solver="saga",
            class_weight="balanced",
        )

        model.fit(X_train, y_train)
        y_proba = model.predict_proba(X_test)[:, 1]

        thresholds = [0.3, 0.4, 0.5, 0.6, 0.7]

        for t in thresholds:
            print(f"\n---- THRESHOLD: {t} ----")

            y_pred = (y_proba >= t).astype(int)

            print("\nConfusion Matrix:")
            print(confusion_matrix(y_test, y_pred))

            print("\nEvaluation Metrics:")
            print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
            print(f"AUC-ROC: {roc_auc_score(y_test, y_proba):.4f}")

            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, zero_division=0))

    # 11. LightGBM
    if RUN_LIGHTGBM:
        print("\n==============================")
        print("LightGBM")
        print("==============================")

        lgbm = LGBMClassifier(
            n_estimators=100,
            learning_rate=0.1,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        )

        lgbm.fit(X_train, y_train)

        y_proba_lgbm = lgbm.predict_proba(X_test)[:, 1]

        thresholds = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

        for t in thresholds:
            print(f"\n---- LightGBM THRESHOLD: {t} ----")

            y_pred = (y_proba_lgbm >= t).astype(int)

            print("\nConfusion Matrix:")
            print(confusion_matrix(y_test, y_pred))

            print("\nEvaluation Metrics:")
            print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
            print(f"AUC-ROC: {roc_auc_score(y_test, y_proba_lgbm):.4f}")

            print("\nClassification Report:")
            print(classification_report(y_test, y_pred, zero_division=0))

    print("\nPipeline executed successfully.")


if __name__ == "__main__":
    main()