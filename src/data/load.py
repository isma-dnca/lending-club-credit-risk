import pandas as pd
from src.config import RAW_DATA_DIR


def load_raw_data(filename: str) -> pd.DataFrame:
    """Load raw data from raw data directory.
    
    Parameters
    ----------
    filename : str
        The name of the dataset file to load located in `data/raw/`.

    Returns
    -------
    pd.DataFrame
        Loaded data as a pandas DataFrame.

    Raises
    ------
        FileNotFoundError
            If the file does not exist in the raw data directory.

    """

    file_path = RAW_DATA_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"the file {filename} does not exist in the raw data directory.")
    
    return pd.read_csv(file_path, low_memory=False)

