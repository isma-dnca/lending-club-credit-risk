from pathlib import Path

#----------------------------------
# Project Root
#----------------------------------
#The root directory of the repository, which is one level above the src/ directory.
# This resolve the path to the folder containing : 
# src/, data/, notebooks/, README.md, etc.

PROJECT_ROOT = Path(__file__).resolve().parent.parent

#----------------------------------
# Data Directories
#----------------------------------

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

#----------------------------------
# Dataset files. This is the path to the raw dataset file.
#----------------------------------

RAW_DATA_FILE = RAW_DATA_DIR / "LC_loans_granting_model_dataset.csv"

#----------------------------------
# Random seed for reproducibility
#----------------------------------

RANDOM_STATE = 42   

