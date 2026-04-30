from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_raw_data(file_path: str | Path) -> pd.DataFrame:
    """
    Load raw data from a given file path.

    Parameters
    ----------
    file_path : str or Path
        Path to the raw dataset file.

    Returns
    -------
    pd.DataFrame
        Loaded data as a pandas DataFrame.

    Raises
    ------
    FileNotFoundError
        If the dataset file does not exist.
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")

    return pd.read_csv(path, low_memory=False)
