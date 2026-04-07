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

def engineer_emp_length(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "emp_length" not in df.columns:
        return df

    mapping = {
        "< 1 year": 0,
        "1 year": 1,
        "2 years": 2,
        "3 years": 3,
        "4 years": 4,
        "5 years": 5,
        "6 years": 6,
        "7 years": 7,
        "8 years": 8,
        "9 years": 9,
        "10+ years": 10,
    }

    df["emp_length_num"] = df["emp_length"].map(mapping)

    df = df.drop(columns=["emp_length"])

    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # numeric columns --> fill with median
    num_cols = df.select_dtypes(include=["number"]).columns
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())

    # categorical --> fill with "missing"
    cat_cols = df.select_dtypes(include=["object", "string"]).columns
    df[cat_cols] = df[cat_cols].fillna("missing")

    return df


def engineer_ratio_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Loan vs revenue (very important)
    if "loan_amnt" in df.columns and "revenue" in df.columns:
        df["loan_to_revenue"] = df["loan_amnt"] / (df["revenue"] + 1)

    # Loan vs credit quality (risk amplification)
    if "loan_amnt" in df.columns and "fico_n" in df.columns:
        df["loan_to_fico"] = df["loan_amnt"] / (df["fico_n"] + 1)

    # Revenue vs credit quality (capacity vs trust)
    if "revenue" in df.columns and "fico_n" in df.columns:
        df["revenue_to_fico"] = df["revenue"] / (df["fico_n"] + 1)

    return df