from lightgbm import LGBMClassifier
from src.config import RANDOM_STATE

def train_lightgbm_model(X_train, y_train):
    """
    Train a LightGBM model on preprocessed training data.

    Parameters
    ----------
    X_train : pd.DataFrame
        Training features.
    y_train : pd.Series
        Training target variable.

    Returns
    -------
    LGBMClassifier
        Trained LightGBM model.
    """
    model = LGBMClassifier(
        random_state=RANDOM_STATE, # means fix randomness and improve reproducibility of the results. By setting a specific random state, we ensure that the same sequence of random numbers is generated each time we run the code, which can be helpful for debugging and comparing results across different runs.
        n_estimators=100,
        learning_rate=0.1,
        n_jobs=-1 # It means use all available CPU cores for training the model
    )
    # So till this point we have created an instance of the LGBMClassifier with specified parameters.
    # I mean an object of the LGBMClassifier class, but it is not yet trained on the data.
    # it is just an empty model(it is an initialized estimator or we can say not yet a fitted estimator)
    # with the specified parameters, but it has not yet learned anything from the data.


    # Now the next step is to train (fit) the model on the training data. where the model sees the data
    # and learns the patterns and relationships between the features (X_train) and the target variable
    # (y_train). Before this coming line, **configured only** and after this line, the model is considered
    # as a trained model or **trained object**.
    model.fit(X_train, y_train)

    return model # After fitting the model on the training data, we return the trained model object.

