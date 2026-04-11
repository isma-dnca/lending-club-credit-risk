from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


def build_preprocessor(numeric_features, categorical_features):
    """
    Define a function that returns a preprocessing object.

    Parameters
    ----------
    numeric_features : list
        List of numeric feature names.
    categorical_features : list
        List of categorical feature names.

    Steps
    -----
    1. Create numeric pipeline
    2. Create categorical pipeline
    3. Combine both using ColumnTransformer

    Returns
    -------
    ColumnTransformer
        A preprocessing object ready to be fit later on X_train.
    """

    # Numeric branch:
    # fill missing numeric values using the median learned from X_train
    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ]
    )

    # Categorical branch:
    # fill missing categorical values with "missing"
    # then encode categories into numbers
    # ignore unseen categories at transform time so the pipeline does not crash
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # Combine numeric and categorical branches into one preprocessing object
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, numeric_features),
            ("cat", categorical_pipeline, categorical_features),
        ]
    )

    return preprocessor
