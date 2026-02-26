# This the 1st entry point of the preprocess.py file and it is used to test the basic cleaning function.
# ------------------------------------------------------------------------------------------------

# import pandas as pd

# def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
#     """
#     Perform basic cleaning on the DataFrame.
#     """
#     df = df.copy()

#     # Example operations
#     df = df.drop_duplicates()
#     df.columns = df.columns.str.lower()

#     return df
#------------------------------------------------------------------------------------------------

# This the 2nd entry point of the preprocess.py file and it is used to improve the basic cleaning
# function by adding more cleaning steps.

import pandas as pd
def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform minimal cleaning operations on the DataFrame by:
    - Remove duplicates row
    - Normalize column names  
    """
    df = df.copy() # Give me a copy of the original DataFrame to work on, so I don't mess with 
                    # the original data.
    
    initial_shape = df.shape

    df = df.drop_duplicates() # Remove duplicate rows from the DataFrame to ensure that each row is unique.
    df.columns = df.columns.str.strip().str.lower()

    final_shape = df.shape

    print(f"[CLEANING] shape before : {initial_shape}, shape after: {final_shape}")

    return df


#------------------------------------------------------------------------------

def split_target(df: pd.DataFrame, target_column: str): 
    """
    Split the DataFrame into features (X) and target (y).
    """
    if target_column not in df.columns:
        raise ValueError(f"{target_column} not found in DataFrame columns.")
    
    X = df.drop(columns=[target_column])
    y = df[target_column]

    return X,y