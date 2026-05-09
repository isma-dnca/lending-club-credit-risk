## Section 1 — Exact Inference Contract

Inference is the moment when a trained machine learning model stops learning and starts using what it has already learned to make predictions on new unseen data.

In this project, the inference contract defines:
- what input data inference accepts
- which artifacts inference requires
- what processing steps inference applies
- what outputs inference returns
- what inference is not allowed to do

The first version of inference will consume a raw CSV file path containing new observations to score.

Inference will require:
- a saved trained model artifact
- a saved fitted preprocessor artifact

The inference workflow will follow this order:
1. load raw input data
2. apply deterministic preprocessing
3. transform the processed data with the saved fitted preprocessor
4. generate predicted probabilities
5. convert probabilities into predicted classes using a threshold

The deterministic preprocessing layer must remain consistent with training. That means inference must reuse the same deterministic preprocessing functions that were applied before fitting the training preprocessor.

The first version of inference should return prediction outputs containing at least:
- `default_probability`
- `predicted_default`

If an `id` column exists in the input, it should be preserved in the output.

Threshold behavior should remain configurable. If no threshold is passed explicitly, inference should use the project default threshold.

This first version of inference is local and package-level. It is not yet an API or deployment layer.

Inference must not:
- retrain the model
- refit the preprocessor
- split train/test
- require the target column
- call the full training pipeline

## Section 2 -- Module Structure

Inference should be introduced as its own package inside the main project package.
The new module should live at:
```bash
src/lending_club_credit_risk/inference/
```
At this level the inference package may look small like this:
```text
src/lending_club_credit_risk/inference/
├── __init__.py
└── predict.py
```
The role of `__init__.py` is only to make the directory as a Python package. and it should not contain any inference logic and can be minimal for first version.

The main inference workflow should live inside `predict.py` file. Its responsibilities are:
-   loading saved artifacts
-   applying deterministic preprocessing for new raw data
-   transforming data with the saved fitted preprocessor
-   generating predicted probabilities
-   converting predicted probabilities into predicted classes using a threshold
-   formatting prediction results

Also the inference package must stay focused on prediction behavior only. It means that other responsibilities like model taring, evaluation report and other reps must stay in their own module.
This module structure is intentionally simple because it is meant to become the reusable base for later chapters such as:
- prediction CLI
- FastAPI service
- Dockerized inference
- deployment

---


## Section 3 -- Core Inference workflow

The inference workflow should start from raw input data so it should and must remain consistent with training data workflow, which means it must follow the prediction path used during training.

So the workflow should follow this order:
1. load raw input data from a CSV file
2. apply deterministic preprocessing
3. drop excluded non-modeling columns
4. load the saved fitted preprocessor
5. transform the processed input with the saved preprocessor
6. load the saved trained model
7. generate predicted probabilities
8. convert probabilities into predicted classes using a threshold
9. format and return prediction outputs

The deterministic preprocessing must use the same logic function used during training, This is important because the saved preprocessor expects the feature structure produced after those deterministic transformations:
- `basic_cleaning`
- `engineer_issue_date_features`
- `engineer_emp_length`
- `engineer_ratio_features`
  
Also to remain aligned with teh trained feature space, the workflow must also reuse the same excluded column policy.

As declared before, the first inference version should produces outputs containing at least:
- `default_probability`
- `predicted_default`

So far we know what must the workflow contain and what can look like. Also in the same angle we need to explicitly declare and specify what must not contained in the inference workflow, such as:
- retrain the model
- refit the preprocessor
- split train/test
- require the target column
- call the full training pipeline
  
This workflow is designed to become the reusable prediction core for for later ops that will come like:
- prediction CLI
- FastAPI service
- Dockerized inference
- deployment
  