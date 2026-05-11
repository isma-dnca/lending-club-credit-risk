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
  
---

## Test Strategy

The inference tests should live in the same root test suite structure as the rest of the project.
so the file could live here:
```text
tests/test_inference.py
```
this place is a must and logic because inference is part the core package, it belongs to `\tests` folder which is logic, and it should run the SAME `pytest` and CI workflow as the rest of the repo.
Also the tests should rely on small synthetics CSV files, temporary saved artifacts, and temporary output paths. But Never the full real dataset or existing local artifacts from manual runs.


1. Positive & Happy Inference test:
   if the inference test can :
    - load a raw CSV input file
    - apply deterministic preprocessing
    - load the saved fitted preprocessor
    - load the saved trained model
    - generate predicted probabilities 
    - generate predicted classes
    - return outputs with the expected structure
  then the inference can be considered happy and positive
  Also the output should contain at least:
    - `default_probability`
    - `predicted_default`

2. Threshold behavior test
    The model should use the threshold to decide which class to predict. A test should check that this is actually happening and not being skipped.

3. Missing artifact failure tests
    When the model runs, it needs certain saved files to work. Tests should check that if one of these files is missing, either the model file or the preprocessor file, the process fails with a clear error message, not a confusing one. So failures should produce explicit and understandable errors.

4. Invalid Input schema test
    When bad or incomplete data is given as input, for example, a required column is missing, the model should fail with a clear error. At least one test should check this, to make sure invalid inputs are caught early.

5. Output contract test

    The inference output should be validated structurally.

    Tests should verify:
    - expected columns exist 
    - output row count matches input row count
    - probability output is present
    - class predictions are present
  
    At this level of this project, this first version of inference testing does not need to include:
    - API endpoint tests
    - deployment tests
    - performance tests
  The purpose of this test strategy is to protect the local package-level inference workflow before prediction CLI, API, and deployment layers are added.

  ---

  ## Implementation order and Definition of Done

  The inference layer should be implemented in controlled order by following a logic workflow and a clear boundaries step by step.

  So the implementation order can be as follow:
   1. create the `inference/` package structure
   2. add artifact loading helpers
   3. add raw input preparation and deterministic preprocessing reuse
   4. add the main prediction workflow
   5. add inference tests
   6. verify local inference behavior
   7. verify that the full project test suite still passes

The detailed implementation can be as follow
### Phase A: Structure
- create `src/lending_club_credit_risk/inference/`
- create `__init__.py`
- create `predict.py`

### Phase B: Artifact loading
- load saved model
- load saved fitted preprocessor

### Phase C: Input preparation
- load raw inference CSV
- apply deterministic preprocessing
- drop excluded non-modeling columns

### Phase D: Prediction logic
- transform input using the saved preprocessor
- generate predicted probabilities
- convert probabilities into predicted classes using threshold
- format prediction outputs

### Phase E: Testing
- add happy-path inference test
- add threshold behavior test
- add missing artifact tests
- add invalid input tests
- validate output contract
  
### Phase F: Verification
- run inference tests locally
- run the full project test suite
- confirm the repository still behaves correctly as a whole

### Definition of Done
- the repository has a dedicated inference module
- saved model and preprocessor artifacts can be reused
- new raw CSV input can be scored
- probabilities and predicted classes are returned
- threshold is configurable and respected
- inference behavior is protected by automated tests
- the full project test suite still passes

Once all those conditions are true then the repo will be ready to move to the next chapter :
- prediction CLI.
