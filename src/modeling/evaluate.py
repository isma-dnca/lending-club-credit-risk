# First, import evaluation functions from sklearn.metrics.
# Each one helps us measure a different aspect of model performance.
from sklearn.metrics import (
    accuracy_score,        # % of total predictions that are correct
    confusion_matrix,      # full prediction breakdown: TN, FP, FN, TP
    f1_score,              # balance between precision and recall
    precision_score,       # among predicted positives, how many are truly positive
    recall_score,          # among actual positives, how many were correctly found
    roc_auc_score,         # probability-ranking quality: can the model rank positives above negatives?
    classification_report, # detailed report of precision, recall, f1-score for each class
)


# Function definition:
# This function evaluates a trained binary classification model on test data.
#
# It does two different things:
# 1. It uses predicted probabilities to calculate ROC AUC.
#    ROC AUC does not need hard class predictions. It evaluates how well the model
#    separates positive examples from negative ones using scores/probabilities.
#
# 2. It converts predicted probabilities into binary predictions (0 or 1)
#    using a decision threshold, then calculates classification metrics
#    such as accuracy, precision, recall, f1, and confusion matrix.

def evaluate_model(model, X_test, y_test, threshold=0.5):
    """
    Evaluate the performance of a trained binary classification model on test data.

    Parameters
    ----------
    model : estimator
        Already trained classification model with predict_proba support.
    X_test : array-like
        Test features, already preprocessed and ready for prediction.
    y_test : array-like
        True labels for the test set.
    threshold : float, default=0.5
        Probability threshold used to convert predicted probabilities
        into binary class predictions.

    Returns
    -------
    dict
        Dictionary containing evaluation metrics and prediction summary.
    """

    # Step 1 — Get predicted probabilities for the positive class (class 1)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Explanation:
    # predict_proba(X_test) returns an array of shape (n_samples, n_classes)
    # where each row contains the predicted probability for each class.
    #
    # Example:
    # [
    #   [P(class=0), P(class=1)],
    #   [P(class=0), P(class=1)],
    #   ...
    # ]
    #
    # By using [:, 1], we keep only the probability of class 1.
    # In binary classification:
    # - class 0 = negative class
    # - class 1 = positive class
    #
    # So here we are extracting the predicted probability of the event of interest.

    # Step 2 — Convert predicted probabilities into binary class predictions
    y_pred = (y_pred_proba >= threshold).astype(int)

    # Explanation:
    # We compare each predicted probability to the threshold.
    #
    # Rule:
    # - if probability >= threshold  -> predict class 1
    # - if probability < threshold   -> predict class 0
    #
    # Example:
    # y_pred_proba = [0.2, 0.6, 0.4, 0.8]
    # threshold    = 0.5
    #
    # Comparison:
    # [0.2 >= 0.5, 0.6 >= 0.5, 0.4 >= 0.5, 0.8 >= 0.5]
    # [False,      True,       False,      True]
    #
    # After .astype(int):
    # [0, 1, 0, 1]
    #
    # Important:
    # the threshold is not something learned by the model itself.
    # It is a decision rule chosen by us depending on the business objective.
    #
    # For example:
    # - lower threshold -> predict more positives -> usually recall goes up
    # - higher threshold -> predict fewer positives -> usually precision goes up

    # Step 3 — Calculate evaluation metrics
    metrics = {
        # ROC AUC uses probabilities, not binary predictions
        # because it evaluates ranking quality across all possible thresholds.
        "roc_auc": roc_auc_score(y_test, y_pred_proba),

        # Accuracy uses final binary predictions
        "accuracy": accuracy_score(y_test, y_pred),

        # Precision:
        # among all predicted positives, how many were actually positive?
        "precision": precision_score(y_test, y_pred, zero_division=0),

        # Recall:
        # among all actual positives, how many did the model capture?
        "recall": recall_score(y_test, y_pred, zero_division=0),

        # F1 score:
        # harmonic mean of precision and recall
        "f1": f1_score(y_test, y_pred, zero_division=0),

        # Confusion matrix:
        # [[TN, FP],
        #  [FN, TP]]
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),

        # Classification report:
        # detailed per-class summary of precision, recall, and f1-score
        # output_dict=True returns a structured dictionary instead of a plain string
        "classification_report": classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0
        ),

        # Keep threshold in the results for reproducibility
        "threshold": threshold,
    }

    # Final step — return the metrics dictionary.
    #
    # Returning a dictionary is better than printing directly because it allows us to:
    # - inspect results later
    # - log them
    # - save them to a file
    # - compare multiple runs
    # - track experiments in a clean way
    return metrics


# Summary:
# This function takes a trained binary classification model and test data,
# gets predicted probabilities for class 1,
# converts those probabilities into binary predictions using a threshold,
# computes several evaluation metrics,
# and returns everything in a structured dictionary.
#
# Mental pipeline:
# model -> predicted probabilities -> threshold -> class predictions -> metrics -> structured report