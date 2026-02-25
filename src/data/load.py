import pandas as pd
from src.config import RAW_DATA_DIR

def load_raw_data(filename: str):
    file_path = RAW_DATA_DIR / filename
    return pd.read_csv(file_path, low_memory=False)
