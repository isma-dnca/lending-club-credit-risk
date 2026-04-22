# Lending Club Credit Risk Prediction

> A modular machine learning pipeline for loan default risk prediction

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green) ![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

---

## Project Goal

The goal of this project is to build a clean, reproducible, and modular machine learning pipeline for credit risk prediction.
At the beginning, the project was driven mostly as one main script. Step by step, it was refactored into separate modules so that each responsibility has its own place.

The current goal is not only to train a model, but to build the project in a way that is closer to real ML engineering practice:
    - modular preprocessing
    - leakage-safe train/test workflow
    - separated training and evaluation logic
    - reproducible saved artifacts
    - clear project structure
    - documentation of each important step

---

## Dataset

The dataset used in this project is stored at:
```text
data/raw/LC_loans_granting_model_dataset.csv
```

It contains borrower and loan information used to predict default risk. Some of the available columns include:

    - loan amount
    - fico score
    - debt-to-income ratio
    - employment length
    - loan purpose
    - address state
    - home ownership
    - text columns such as title and desc
    - Target variable: `default`

---

## Current Project Structure
```bash
lending-club-credit-risk/
├── data/
│   ├── processed/
│   └── raw/
│       └── LC_loans_granting_model_dataset.csv
├── docs/
│   ├── 00-environment-setup.md
│   ├── 01-project-structure-and-paths.md
│   ├── 02-columns.md
│   ├── 03-launch-protocol.md
│   ├── 04-baseline-model-analysis.md
│   ├── 05-lightgbm-model-analysis.md
│   ├── 06-project-roadmap.md
│   ├── 07-feature-engineering.md
│   ├── 08-training_pipeline_design.md
│   ├── 09-build-preprocessor-object.md
│   ├── 10-build-train_pipeline-script.md
│   ├── 11-build-train-module.md
│   ├── 12-model-evaluation.md
│   ├── 13-artifact-saving.md
│   ├── 14-transition-monolith-to-modular-ml-pipeline.md
│   └── 15-first-end-to-end-modular-pipeline-run.md
├── notebooks/
│   ├── 01-data-loading-and-exploration.ipynb
│   └── 02-exp_lightgbm_model_state_before_after_fit.ipynb
├── outputs/
│   ├── models/
│   │   └── lightgbm_model.joblib
│   ├── preprocessors/
│   │   └── preprocessor.joblib
│   └── reports/
│       └── metrics.json
├── src/
│   ├── config.py
│   ├── main.py
│   ├── data/
│   │   └── load.py
│   ├── features/
│   │   ├── preprocess.py
│   │   └── preprocessor.py
│   ├── modeling/
│   │   ├── evaluate.py
│   │   └── train.py
│   ├── persistence/
│   │   └── save_artifacts.py
│   └── pipeline/
│       └── train_pipeline.py
├── environment.yml
├── pyproject.toml
└── README.md
```

---

## What Each Module Does

### `src/data/load.py`
Responsible for loading raw data from `data/raw/`.

### `src/features/preprocess.py`
Contains deterministic preprocessing steps that do not learn from data, such as:
- basic cleaning
- issue date feature engineering
- employment length transformation
- ratio feature engineering
- target split

### `src/features/preprocessor.py`
Builds the fit-ready preprocessing object using:
- numeric branch
- categorical branch
- ColumnTransformer

This file only builds the object. It does not fit it yet.

### `src/pipeline/train_pipeline.py`
Orchestrates the preprocessing workflow:
- load data
- apply deterministic transformations
- split target
- split train/test
- identify numeric and categorical columns from `X_train`
- build preprocessor
- fit on `X_train`
- transform `X_train` and `X_test`

### `src/modeling/train.py`
Contains model training logic. Right now, it trains a LightGBM classifier.

### `src/modeling/evaluate.py`
Contains model evaluation logic. It computes metrics such as:
- ROC-AUC
- accuracy
- precision
- recall
- f1-score
- confusion matrix
- classification report

### `src/persistence/save_artifacts.py`
Handles persistence of:
- trained model
- fitted preprocessor
- metrics

### `src/main.py`
Acts now only as the entry point. Its role is to:
- call preprocessing pipeline
- call training module
- call evaluation module
- call artifact saving module

So `main.py` no longer contains the whole project logic inside itself.

---

## How the New Pipeline Works

The current training flow is:

1. load raw data
2. apply deterministic transformations
3. split features and target
4. drop excluded columns
5. split train/test
6. detect numeric and categorical columns from `X_train`
7. build the fit-ready preprocessor
8. fit the preprocessor on `X_train`
9. transform `X_train` and `X_test`
10. train the LightGBM model
11. evaluate the model on test data
12. save artifacts and metrics

This design is important because it keeps learned preprocessing steps inside the training workflow and avoids fitting them on the full dataset. That is one of the key improvements compared to the old one-file version.

---

## Environment Setup

Create the conda environment with:

```bash
conda env create -f environment.yml
conda activate lending-club-ml
```

---

## How to Run

Run the project from the root of the repository:

```bash
python -m src.main
```

This command now launches the full modular workflow:
    - preprocessing pipeline
    - LightGBM training
    - model evaluation
    - artifact saving

---

## Saved Outputs

After a successful run, the project saves:
  - trained model
  - fitted preprocessor
  - metrics report

Current output locations:
```
outputs/models/lightgbm_model.joblib
outputs/preprocessors/preprocessor.joblib
outputs/reports/metrics.json
```
This is an important step toward reproducibility, because results are no longer only printed to the console.

---

## Current Status

At this stage, the modular training pipeline has been implemented and executed successfully end to end.
That means the project now already has:
  - modular preprocessing
  - modular training
  - modular evaluation
  - artifact saving
  - clean entry point
  - documented refactoring process

The architecture is now much closer to a real ML engineering project than it was at the beginning.

### First End-to-End Run of the New Modular Pipeline

The first successful run of the modular architecture produced the following main metrics:

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.6803 |
| Recall | 0.0194 |
| Precision | 0.5668 |

**What this means:**

From an engineering point of view, this is a success because the new architecture now works from start to finish.

From a modeling point of view, the current threshold still makes the model too conservative for detecting defaults. So the pipeline is technically working, but the decision behavior still needs improvement. This is now a modeling decision issue, not an architecture issue.

---

## Documentation

This repository contains step-by-step documentation of the refactoring and building process inside the `docs/` folder.
The documentation tracks the project from:
  - old monolithic script
  - pipeline design
  - preprocessor builder
  - train pipeline creation
  - training module
  - evaluation module
  - saving artifacts
  - main entrypoint refactoring

So the project is not only code, but also a written record of the reasoning behind each step.

---

## Planned Next Improvements

The next improvements planned for this project are:

    - inspect and improve the saved metrics workflow
    - improve threshold handling in the modular architecture
    - update metadata saving
    - improve README and repo hygiene continuously
    - add tests for pipeline stability
    - build an inference / prediction workflow
    - prepare the project for API exposure later
    - move gradually toward MLOps-ready structure

---

## Purpose of This Repository

This repository is not only about getting a model score.
It is also about learning how to build a machine learning project properly:
  - with separation of concerns
  - with reproducible workflow
  - with saved artifacts
  - with modular structure
  - with documentation of the engineering decisions

So the purpose is both:
  - build a useful credit risk model
  - build strong ML engineering foundations for future real projects