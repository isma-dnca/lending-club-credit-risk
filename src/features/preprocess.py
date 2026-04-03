import pandas as pd


def basic_cleaning(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform minimal cleaning on the input DataFrame.

    Operations:
    - remove duplicate rows
    - strip whitespace from column names
    - convert column names to lowercase

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        Cleaned copy of the DataFrame.
    """
    df = df.copy()

    initial_shape = df.shape

    df = df.drop_duplicates()
    df.columns = df.columns.str.strip().str.lower()

    final_shape = df.shape

    print(f"[CLEANING] shape before: {initial_shape}, shape after: {final_shape}")

    return df


def split_target(
    df: pd.DataFrame, target_column: str
) -> tuple[pd.DataFrame, pd.Series]:
    """
    Split a DataFrame into features (X) and target (y).

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.
    target_column : str
        Name of the target column.

    Returns
    -------
    tuple[pd.DataFrame, pd.Series]
        Features DataFrame X and target Series y.

    Raises
    ------
    ValueError
        If the target column is not present in the DataFrame.
    """
    if target_column not in df.columns:
        raise ValueError(f"'{target_column}' not found in DataFrame columns.")

    X = df.drop(columns=[target_column])
    y = df[target_column]

    return X, y


def engineer_issue_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create simple date-based features from the `issue_d` column.

    New features:
    - issue_year
    - issue_month

    The original `issue_d` column is dropped after transformation.

    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame with engineered date features.

    Raises
    ------
    ValueError
        If `issue_d` is not present in the DataFrame.
    """
    df = df.copy()

    if "issue_d" not in df.columns:
        raise ValueError("'issue_d' not found in DataFrame columns.")

    issue_dates = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")

    df["issue_year"] = issue_dates.dt.year
    df["issue_month"] = issue_dates.dt.month

    df = df.drop(columns=["issue_d"])

    return df