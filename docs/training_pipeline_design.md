# Convert current script into reproducible training pipeline that saves fitted model, fitted preprocessor, and evaluation metrics

The goal for this Milestone is to move from a script that trains a model in one block into a clean and reproducible training pipeline.

So far, the logical stages that my script already contains are:

- load raw data
- basic cleaning
- deterministic feature engineering
- split features and target
- split train / test
- fit preprocessing on train only
- transform train / test
- train model
- evaluate model
- save artifacts
- save metadata

Current state: my `src/main.py` mixes all of this together, and there is no explicit separation of each responsibility.

Target structure: make each logical stage become its own clear function or module, so that the training flow becomes easier to read, easier to maintain, and more professional.

So far, the most important methodological issue I’m facing here is leakage-safe preprocessing.

My first step here is to define the pipeline responsibilities.

The main goal of this step is to clarify the training flow that the repo should have.

---

## Scope of Milestone 1

To avoid confusion and feature creep, this milestone is intentionally limited to:

- one dataset: `data/raw/LC_loans_granting_model_dataset.csv`
- one target: `default`
- one model: LightGBM
- one train/test split
- no model comparison
- no hyperparameter search
- no text modeling (`title`, `desc` are excluded)
- no experimental features during refactoring

The goal is not performance optimization.

The goal is to build a **reproducible, leakage-safe training pipeline**.

---

## 1. `Load raw data`

- Question: What file enters the pipeline?

The real question is: which file is accepted as the official input to the pipeline?

It is the original input file that the pipeline consumes before any transformation.

In this project:

`data/raw/LC_loans_granting_model_dataset.csv`

This file is the starting point of the entire pipeline.

---

## 2. `Apply deterministic feature engineering`

- Question: What transformations do not need to learn from the dataset?

At this stage, I apply only transformations that do not compute or learn anything from the data.

These transformations:

- do not require a fit step
- do not compute statistics such as mean, median, or category levels
- can be applied directly row by row

Examples in this project:

- parsing `issue_d` into `issue_year` and `issue_month`
- mapping `emp_length` into numeric form
- creating ratio features from existing columns

These are deterministic transformations.

They are safe to apply before the train/test split.

---

## 3. `Split features and target`

- Question: Where do `X` and `y` get created?

At this stage, the dataset is separated into:

- `y` -> target (`default`)
- `X` -> input features

Then I explicitly define the modeling feature set.

From `X`, I remove:

- `id` (identifier)
- `title`, `desc` (text, excluded in this milestone)
- `zip_code` (excluded for simplicity in this milestone)

This step ensures:

- the target is isolated early
- only relevant features are passed to the pipeline

This happens after deterministic transformations and before any learning step.

---

## 4. `Train/test split`

- Question: At what exact point does the split happen?

The split happens immediately after creating `X` and `y`, and before any transformation that learns from data.

Pipeline order:

1. Load data  
2. Deterministic transformations  
3. Split into `X` and `y`  
4. **Train/test split**

This acts as a **firewall**.

Before this point:
- safe zone, because no learning has happened yet

After this point:
- learning begins

---

## 5. `Fit preprocessing on train only`

- Question: Which transformations must be learned only from `X_train`?

All transformations that need to compute something from data must be fitted on `X_train` only.

These include:

- missing value imputation
- categorical encoding
- any transformation based on data distribution
- any preprocessing step that learns categories, statistics, or structure

These transformations require a fit step.

They must never use `X_test`.

This is the core rule that prevents data leakage.

---

## 6. `Transform train and test`

- Question: How do you guarantee the same feature space?

Same feature space means:

- same columns
- same order
- same encoding
- same preprocessing logic

This is guaranteed by:

- fitting one preprocessor on `X_train`
- reusing the same fitted object on both `X_train` and `X_test`

Critical rule:

> `X_test` must never define new preprocessing structure.

The train set defines the transformation logic.  
The test set only follows it.

That is what makes the transformation reproducible and safe.

---

## 7. `Train model`

- Question: Which single model is trained?

The model trained for this milestone is:

**LightGBM**

This choice is based on previous experiments where it performed better than Logistic Regression.

The goal here is not comparison.

The goal is to build one clean and reproducible pipeline around one model.

---

## 8. `Evaluate`

- Question: Which metrics are computed and kept?

The model is evaluated using metrics adapted to classification and class imbalance.

Main metrics:

- `ROC-AUC` -> primary metric for ranking performance
- `Precision` -> quality of predicted defaults
- `Recall` -> ability to detect defaults
- `F1-score` -> balance between precision and recall

`Accuracy` may still be computed, but it is not treated as a reliable metric because of class imbalance.

Additional diagnostics:

- confusion matrix
- classification threshold used for prediction

For this milestone, the threshold can remain fixed at `0.5` in order to keep the pipeline simple and stable during the refactoring.

Threshold optimization belongs to a later milestone.

All metrics are computed on the test set.

---

## 9. `Save artifacts`

- Question: What is saved after training?

The pipeline saves all elements required to reuse the model without retraining.

Artifacts:

- fitted preprocessing pipeline
- trained LightGBM model
- evaluation metrics file

Artifacts are stored in a dedicated output location, separate from raw data.

Without the preprocessor, the model is unusable.

So both the preprocessor and the model must always be saved together.

---

## 10. `Save run metadata`

- Question: What additional information is recorded?

Metadata describes how the model was trained.

It includes:

- data information  
  (dataset path, number of samples, target)

- train/test split configuration  
  (test size, random seed)

- model configuration  
  (LightGBM parameters)

- preprocessing configuration  
  (feature lists, strategies used)

- evaluation setup  
  (metrics used, threshold)

- run information  
  (timestamp, run ID)

- code version  
  (git commit hash or project version)

Artifacts = what was produced  
Metadata = how it was produced

Both are required for reproducibility.

---

## Final understanding of Step 1

The central rule of this pipeline is:

Deterministic transformations can happen before the split because they do not learn from data.

Any transformation that computes statistics, categories, or parameters must be fitted only on `X_train`.

This is what makes the pipeline:

- leakage-safe
- reproducible
- reusable
- maintainable

The purpose of this milestone is not just cleaner code.

It is to define a **professional training flow** where:

- each step has one responsibility
- the process is traceable
- the outputs can be reused reliably

---

## Next step

The next step is to classify all current transformations into:

- deterministic feature engineering
- train-fitted preprocessing

This will prepare the implementation of the full reproducible training pipeline.
