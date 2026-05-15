# Lending Club Credit Risk Prediction

> A modular machine learning project for credit risk prediction, with reproducible training, saved artifacts, automated tests, and CLI based inference workflows.

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green) ![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

---

## Project Goal

This project is built to develop a clean, reproducible, and modular machine learning workflow for credit risk prediction using Lending Club loan data.

I started from a more script-oriented workflow and has been progressively reorganized into a package-based project  with clearer engineering boundaries. The goal in not only to train a model, but to build the surrounding system the right and professional way as well: preprocessing, training, evaluation, artifact reuse, testing, and command line usability.

In other words, the project is meant to grow as both:
- a credit risk modeling workflow
- a practical ML engineering and MLOps learning project


---

## Current Capabilities

The repo currently supports:
- deterministic preprocessing and fit-ready preprocessing separation
- modular training pipeline
- LightGBM model training
- threshold-based evaluation
- artifact saving for model, preprocessor, and metrics
- artifact reuse for prediction on new raw CSV data
- package execution through explicit CLI subcommands
- training through `python -m lending_club_credit_risk train`
- prediction through `python -m lending_club_credit_risk predict`
- automated unit, integration, and smoke-style tests
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


## Installation: 

Create and activate the project environment:

```bash
conda env create -f environment.yml
conda activate lending-club-ml
```
The environment installs the project in editable mode together with the development and notebook extras declared in `pyproject.toml`.

If you want t refresh the local setup manually, you can also run:
```bash
python -m pip install -e ".[dev]"
```
If notebook-related dependencies are also needed, run:
```bash
python -m pip install -e ".[dev, notebook]"
```

---

## CLI usage

### Train

Run the end-to-end training workflow with:
```bash
python -m lending_club_credit_risk train
```
This command runs:
- raw data loading
- deterministic preprocessing
- train/test split
- fit-ready preprocessing
- LightGBM training
- evaluation
- artifact saving

Also CLI is configured we can run for example :
```bash
python -m lending_club_credit_risk train --threshold 0.3
```

### Predict

Run inference on new raw CSV data with:
```bash
python -m lending_club_credit_risk predict --input-file path/to/new_data.csv
```
This command runs:
- loads the saved model
- loads the saved fitted preprocessor
- applies deterministic preprocessing to new raw data
- generates default probabilities
- convert probabilities into predicted classes using the chosen threshold

You can also write predictions to disk
```bash
python -m lending_club_credit_risk predict --input-file path/to/new_data.csv --output-file outputs/predictions/predictions.csv
```


---

## Tests & Build

Run the full test suite with:
```bash
python -m pytest tests
```
The test suite currently covers:
- preprocessing behavior
- model evaluation behavior
- artifacts persistence
- inference workflow
- CLI behavior
- end-to-end smoke pipeline execution
  
 
Build the package with :
```bash
python -m build
```
Successful builds generate distribution artifacts in: 
```text
dist/
```


---


## Saved Outputs

After a successful training run, the project saves:
- the trained model
- the fitted preprocessor
- the evaluation metrics
  
The default output location are:
```text
outputs/models/lightgbm_model.joblib
outputs/preprocessors/preprocessor.joblib
outputs/reports/metrics.json
```
These saved artifacts make the workflow reusable by allowing later prediction runs to load and use the trained outputs instead of retraining from scratch.


---


## Project Structure

```text
lending-club-credit-risk/
│
├── README.md
├── pyproject.toml
├── environment.yml
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── data/
│   ├── raw/
│   │   └── LC_loans_granting_model_dataset.csv
│   └── processed/
│
├── docs/
│   ├── 00-environment-setup.md
│   ├── 08-training_pipeline_design.md
│   ├── 18-Inference_foundation_design.md
│   ├── 19-Inference_contract_and_spec.md
│   └── 21-prediction-cli-design.md
│
├── notebooks/
│   └── 01-data-loading-and-exploration.ipynb
│
├── outputs/
│   ├── models/
│   │   └── lightgbm_model.joblib
│   ├── preprocessors/
│   │   └── preprocessor.joblib
│   └── reports/
│       └── metrics.json
│
├── src/
│   └── lending_club_credit_risk/
│       │
│       ├── config.py
│       ├── main.py
│       ├── __main__.py
│       │
│       ├── data/
│       │   └── load.py
│       │
│       ├── features/
│       │   ├── preprocess.py
│       │   └── preprocessor.py
│       │
│       ├── pipeline/
│       │   └── train_pipeline.py
│       │
│       ├── modeling/
│       │   ├── train.py
│       │   └── evaluate.py
│       │
│       ├── inference/
│       │   └── predict.py
│       │
│       └── persistence/
│           └── save_artifacts.py
│
└── tests/
    ├── test_cli.py
    ├── test_inference.py
    ├── test_preprocess.py
    ├── test_evaluate.py
    └── test_smoke_pipeline.py
```


---


## Continuous Integration (CI)

Github Actions is configured to automatically:

- install the project with development dependencies
- run the full test suite.
- build the package
  
This helps verify that the training, inference, testing, and packaging workflows continue to work in a clean environment.


---


## Example Metrics From a Training Run

Below is an example of evaluation metrics produced by the current pipeline configuration and decision threshold:

| Metric | Value |
|--------|-------|
| ROC-AUC | 0.6803 |
| Recall | 0.0194 |
| Precision | 0.5668 |


---

## Next Milestones

Planned next steps include:

- improve the README and repository documentation consistency
- polish CLI behavior and command help output
- add a prediction CLI implementation/results milestone document
- expose prediction through an API or service layer
- prepare the project for containerization and deployment
- continue reducing warnings and cleanup noise
- improve metadata and artifact reporting
  

---


## Purpose of the Repository

This repository is not only about training a model and reporting a score.

It is also about learning how to build a machine learning project with stronger engineering discipline:
- modular code structure
- reproducible workflows
- saved reusable artifacts
- test coverage
- package-aware execution
- CI validation
- documented technical decisions

So the project serves two purposes at the same time:

- building a useful credit risk prediction workflow
- building practical ML engineering and MLOps habits through real implementation milestones
