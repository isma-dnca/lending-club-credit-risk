# Evaluation Module — `src/modeling/evaluate.py`

After building the preprocessing flow and training the model, the next step is to separate model evaluation into its own file. The `src/modeling/evaluate.py` file is dedicated to the evaluation layer — responsible only for measuring model performance on test data.

---

## Why separate evaluation from training?

Training and evaluation are related, but they do not share the same responsibility:

- **Training** is about fitting the model on `X_train` and `y_train`.
- **Evaluation** is about measuring how well the trained model performs on unseen test data.

Separating them makes the project modular, clean, and easier to maintain. It also makes it straightforward to compare results after saving metrics or changing the model.

---

## Main function

The evaluation module contains one main function:

```python
evaluate_model(model, X_test, y_test, threshold=0.5)
```

Its arguments are the trained model, preprocessed test features, true test labels, and a classification threshold. Its role is to evaluate a trained binary classification model on test data and return the results in a structured way.

---

## Two types of model outputs used during evaluation

A binary classifier does not produce one kind of output — it produces **two**, used for different purposes.

### Output 1 — Predicted probabilities

Before deciding on a final label, the model outputs a **probability** for each sample: how confident it is that the sample belongs to class `1`.

For example, for three samples the model might output: `[0.78, 0.34, 0.78]`

These probabilities are used **only for ROC-AUC**, because ROC-AUC sweeps through every possible threshold and asks: *at each threshold, how well does the model rank positives above negatives?* It does not need a fixed cut-off — it evaluates the full probability ranking.

### Output 2 — Binary predictions (hard labels)

The probabilities are then converted into hard `0` or `1` predictions using a threshold τ. With the default τ = 0.5, the example above becomes:

```
[0.78, 0.34, 0.78]  →  [1, 0, 1]
```

These hard predictions are used for all other metrics — accuracy, precision, recall, F1, and the confusion matrix — because those metrics all require a definitive predicted class to compare against the true label.

### Why this distinction matters

| | Probabilities | Binary predictions |
|---|---|---|
| Represent | Confidence / ranking | Final decision |
| Depend on threshold? | No | Yes |
| Used for | ROC-AUC | All other metrics |

- **ROC-AUC** is threshold-independent: it evaluates all thresholds at once.
- **Accuracy, precision, recall, F1** are threshold-dependent: they reflect behaviour at one chosen threshold.

The threshold is a decision rule chosen by us. Changing it shifts prediction behaviour:

- Lower threshold → predicts more positives → **recall** usually increases.
- Higher threshold → predicts fewer positives → **precision** usually increases.

For this reason, the threshold is stored in the returned results for reproducibility.

---

## The function returns a dictionary

The function can share its results in two ways: by printing them, or by returning a dictionary. A dictionary is the better choice.

`print` sends results to the screen and they are gone — nothing can use them afterwards. A returned dictionary is a **living object** that stays in memory and can be passed around, stored, compared, or transformed.

The guiding principle is: **functions should produce values, not side effects.** Printing is a side effect. Returning is producing a value.

---

## Final summary

The evaluation module has one responsibility: measure model performance on unseen test data in a clean and reusable way.

The evaluation flow is:

1. Trained model
2. Predicted probabilities
3. Threshold-based binary predictions
4. Computed metrics
5. Structured results returned as a dictionary

This is an important step toward a professional ML project structure — training and evaluation are now separated into different modules, each with a single, clearly defined responsibility.