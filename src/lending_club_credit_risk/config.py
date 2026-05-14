from __future__ import annotations

import os
from pathlib import Path


#-----------|
# Roots     |
#-----------|

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent

#------------|
# Directories|
#------------|

DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path(os.getenv("LCCR_OUTPUT_DIR", str(PROJECT_ROOT / "outputs")))


# --------------------| 
# Default data file   |
# --------------------|

RAW_DATA_FILE = Path(
    os.getenv(
        "LCCR_RAW_DATA_FILE",
        str(RAW_DATA_DIR / "LC_loans_granting_model_dataset.csv"),
    )
)


# --------------------------|
# Default pipeline settings |
# --------------------------|

RANDOM_STATE = int(os.getenv("LCCR_RANDOM_STATE", "42"))
TEST_SIZE = float(os.getenv("LCCR_TEST_SIZE", "0.2"))
DEFAULT_THRESHOLD = float(os.getenv("LCCR_THRESHOLD", "0.5"))
TARGET_COLUMN = os.getenv("LCCR_TARGET_COLUMN", "default")
COLUMNS_TO_DROP = ("id", "title", "desc", "zip_code")

#-----------------------------------------------|
# Default artifact output paths                 |
#-----------------------------------------------|
DEFAULT_MODEL_PATH = OUTPUT_DIR / "models" / "lightgbm_model.joblib"
DEFAULT_PREPROCESSOR_PATH = OUTPUT_DIR / "preprocessors" / "preprocessor.joblib"
DEFAULT_METRICS_PATH = OUTPUT_DIR / "reports" / "metrics.json"
