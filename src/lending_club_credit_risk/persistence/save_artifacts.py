import json
from pathlib import Path

import joblib


def save_model(model, output_path):
    """
    Save a trained model to disk using joblib.

    Parameters
    ----------
    model : object
        Trained model object.
    output_path : str or Path
        Path where the model should be saved.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, output_path)


def save_preprocessor(preprocessor, output_path):
    """
    Save a fitted preprocessor to disk using joblib.

    Parameters
    ----------
    preprocessor : object
        Fitted preprocessing object.
    output_path : str or Path
        Path where the preprocessor should be saved.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(preprocessor, output_path)


def save_metrics(metrics, output_path):
    """
    Save evaluation metrics to disk as JSON.

    Parameters
    ----------
    metrics : dict
        Dictionary containing evaluation metrics.
    output_path : str or Path
        Path where the metrics JSON file should be saved.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
