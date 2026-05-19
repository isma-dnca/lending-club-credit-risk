from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd

from lending_club_credit_risk.config import COLUMNS_TO_DROP, DEFAULT_THRESHOLD, DEFAULT_MODEL_PATH, DEFAULT_PREPROCESSOR_PATH
from lending_club_credit_risk.features.preprocess import (
    basic_cleaning,
    engineer_emp_length,
    engineer_ratio_features,
    engineer_issue_date_features,
)


def _load_model(model_path: str | Path):
    """
    Load a trained model from disk.
    """

    path = Path(model_path)

    if not path.exists():
        raise FileNotFoundError(f"Model file not found at {path}")
    return joblib.load(path)


def _load_preprocessor(preprocessor_path: str | Path):
    """
    Load a fitted preprocessor from disk.
    """

    path = Path(preprocessor_path)

    if not path.exists():
        raise FileNotFoundError(f"Preprocessor file not found at {path}")
    return joblib.load(path)


def _prepare_inference_dataframe(
    df: pd.DataFrame,
    columns_to_drop=COLUMNS_TO_DROP,
) -> tuple[pd.DataFrame, pd.Series | None]:
    """
    This helper function handles the deterministic preprocessing phase of the inference pipeline.
    
    Apply deterministic preprocessing steps to a raw inference DataFrame.

    ## Prepare fresh unseen data for inference exactly as it was done during training ##

    Returns
    -------
    tuple[pd.DataFrame, pd.Series | None]
        Prepared feature DataFrame ready for the saved preprocessor,
        and the `id` column if it exists.
    """

    df = basic_cleaning(df)
    df = engineer_issue_date_features(df)
    df = engineer_emp_length(df)
    df = engineer_ratio_features(df)

    # Preserve row identifiers (if they exist) so predictions can be linked back to input rows.
    row_ids = df["id"] if "id" in df.columns else None

    X = df.drop(columns=list(columns_to_drop), errors="ignore")

    return X, row_ids



def predict_from_dataframe(
    df: pd.DataFrame,
    model_path: str | Path = DEFAULT_MODEL_PATH,
    preprocessor_path: str | Path = DEFAULT_PREPROCESSOR_PATH,
    threshold: float = DEFAULT_THRESHOLD,
    columns_to_drop=COLUMNS_TO_DROP,
) -> pd.DataFrame:
    """
    Run inference on a raw DataFrame using saved model artifacts.

    Parameters
    ----------
    df : pd.DataFrame
        Raw DataFrame containing new observations, unseen data.
    model_path : str or Path
        Path to the saved trained model artifact.
    preprocessor_path : str or Path
        Path to the saved fitted preprocessor artifact.
    threshold : float, default=DEFAULT_THRESHOLD
        Threshold used to convert probabilities into predicted classes.
    columns_to_drop : sequence of str
        Columns excluded from modeling.

    Returns
    -------
    pd.DataFrame
        Prediction results containing at least:
        - default_probability
        - predicted_default
        and `id` if it was present in the raw input.
    """
    model = _load_model(model_path)
    preprocessor = _load_preprocessor(preprocessor_path)

    X, row_ids = _prepare_inference_dataframe(
        df=df,
        columns_to_drop=columns_to_drop,
    )

    X_processed = preprocessor.transform(X)

    default_probabilities = model.predict_proba(X_processed)[:, 1]
    predicted_default = (default_probabilities >= threshold).astype(int)

    results = pd.DataFrame(
        {
            "default_probability": default_probabilities,
            "predicted_default": predicted_default,
        }
    )

    if row_ids is not None:
        results.insert(0, "id", row_ids.reset_index(drop=True))

    return results


def predict_from_csv(
    input_file: str | Path,
    model_path: str | Path = DEFAULT_MODEL_PATH,
    preprocessor_path: str | Path = DEFAULT_PREPROCESSOR_PATH,
    threshold: float = DEFAULT_THRESHOLD,
    columns_to_drop=COLUMNS_TO_DROP,
) -> pd.DataFrame:
    """
    Run inference on a raw CSV file containing new observations, unseen data.

    Parameters
    ----------
    input_file : str or Path
        Path to the raw CSV file.
    model_path : str or Path
        Path to the saved trained model artifact.
    preprocessor_path : str or Path
        Path to the saved fitted preprocessor artifact.
    threshold : float, default=DEFAULT_THRESHOLD
        Threshold used to convert probabilities into predicted classes.
    columns_to_drop : sequence of str
        Columns excluded from modeling.

    Returns
    -------
    pd.DataFrame
        Prediction results containing at least:
        - default_probability
        - predicted_default
        and `id` if it was present in the raw input.
    """
    path = Path(input_file)
    if not path.exists():
        raise FileNotFoundError(f"Inference input file not found:{path}")

    df = pd.read_csv(path, low_memory=False)
    return predict_from_dataframe(
        df=df,
        model_path=model_path,
        preprocessor_path=preprocessor_path,
        threshold=threshold,
        columns_to_drop=columns_to_drop,
    )