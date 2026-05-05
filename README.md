# Lending Club Credit Risk Prediction

> A modular machine learning pipeline for loan default risk prediction, packaging, testing, and reproducible training workflows.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green) ![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

---

## Project Goal

The goal of this project is to build a clean, reproducible, and modular machine learning workflow for credit risk prediction.
At the beginning, the project was driven mostly as one main script. Over time, it was progressively refactored into separate modules so that each responsibility has a clear place in the codebase.

The current goal is not only to train a model, but also to structure the repo closer to real ML engineering practice:
  - modular preprocessing
  - leakage-safe train/test workflow
  - separated training and evaluation logic
  - reproducible saved artifacts
  - clear project structure / package structure
  - automated tests
  - CI validation
  - documentation of each important step

---

## Current Capabilities

The repo currently supports:
- modular training pipeline
- deterministic preprocessing and fit-ready preprocessing separation
- LightGBM model training 
- threshold-based evaluation
- artifact saving for model, preprocessor, and metrics
- package execution through `python -m lending_club_credit_risk`
- automated unit and smoke tests
- package build validation
- GitHub Actions CI for test and build checks 

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
  
  Target variable:
  - `default`

---

## Project Structure

```text
lending-club-credit-risk/
├── .github/
│   └── workflows/
│       └── ci.yml
├── data/
│   ├── processed/
│   └── raw/
│       └── LC_loans_granting_model_dataset.csv
├── docs/
├── notebooks/
├── outputs/
│   ├── models/
│   ├── preprocessors/
│   └── reports/
├── src/
│   └── lending_club_credit_risk/
│       ├── data/
│       │   ├── __init__.py
│       │   └── load.py
│       ├── features/
│       │   ├── __init__.py
│       │   ├── preprocess.py
│       │   └── preprocessor.py
│       ├── modeling/
│       │   ├── evaluate.py
│       │   └── train.py
│       ├── persistence/
│       │   └── save_artifacts.py
│       ├── pipeline/
│       │   └── train_pipeline.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── config.py
│       └── main.py
├── tests/
│   ├── test_evaluate.py
│   ├── test_persistence.py
│   ├── test_preprocess.py
│   └── test_smoke_pipeline.py
├── .gitignore
├── environment.yml
├── pyproject.toml
└── README.md
```

---

## Installation: 
Create and activate the `conda` environment:
```bash
conda env create -f environment.yml
conda activate lending-club-ml
```
This environment installs the project in editable mode together with `dev` and `notebook` extras declared in `pyproject.toml`.

--- 


## Development Workflow

If you want to install or refresh the local devolvement setup manually, run:
```bash
python -m pip install -e ".[dev]"
```
If notebook-related tools are also needed, run:
```bash
python -m pip install -e ".[dev,notebook]"
```

---

## How To Run Training

To run the training workflow from the repository root, use:
```bash
python -m lending_club_credit_risk
```
This command lunches the full pipeline:
- raw data loading
- deterministic preprocessing
- train/test split
- fit ready preprocessing
- LightGBM training
- evaluation
- artifact saving

Also CLI is configured we can run for example :
```bash
python -m lending_club_credit_risk --threshold 0.3
```

---

## How To Run Tests

Run the full test suite with:
```bash
python -m pytest tests
```
The repo currently includes:
- preprocessing unit tests
- evaluation unit tests
- persistence tests
- ent to end smoke pipeline tests
  

---

## How to build the package 

Build teh source distribution and wheel with :
```bash
python -m build
```
Successful builds generate artifacts in: 
```text
dist/
```

---


## Continuous Integration (CI)

Github Actions is configured to automatically:

- install the project with development dependencies
- run the full test suite.
- build the package
  
This helps verify that both the training code and the packaging workflow work on clean environment.


---


## Saved outputs

After a successful training run, the project saves:

- trained model
- fitted preprocessor
- evaluation metrics

Current output locations:
```text
outputs/models/lightgbm_model.joblib
outputs/preprocessors/preprocessor.joblib
outputs/reports/metrics.json
```
This improves reproducibility by turning training results into reusable artifacts instead of console-only output.

---

## Current Status

At this stage the repository provides:
- modular training pipeline
- package structure for the project
- artifact persistence
- Configurable CLI entrypoints
- automated tests
- package build support
- Github Actions CI validation
The project is no longer just a notebook experiment or a single script thrown together.
It now acts like a real small ML engineering repo, with structure, logic separation, and a pipeline that actually holds together.

### Example End-to-End Metrics

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.6803 |
| Recall | 0.0194 |
| Precision | 0.5668 |

---

## Documentation 

The `docs/` folder contains step-by-step notes covering the evolution of the project, including:

- environment setup
- project structure and path design
- feature engineering
- preprocessing pipeline design
- training module creation
- evaluation module creation
- artifact saving
- package refactoring
- repository hardening decisions

The goal is not only to keep code, but also to preserve the reasoning behind important engineering steps.

---

## Next Improvements

Planned next steps include:

- improve threshold selection strategy
- add inference / prediction workflow
- reduce remaining warnings and cleanup noise
- improve metadata and artifact reporting
- continue polishing documentation and repository hygiene
- prepare the project for future API or service exposure

---

## Purpose of This Repository

This repository is not only about obtaining a model score. It is also about learning how to build a machine learning project properly:
- with separation of concerns
- with reproducible workflows
- with saved artifacts
- with package-aware structure
- with tests
- with CI
- with documented engineering decisions

So the purpose is both:

- to build a useful credit risk model
- to build strong ML engineering foundations for future projects
