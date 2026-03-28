# Lending Club Credit Risk Prediction

> A machine learning pipeline for loan default risk assessment

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Scikit-learn](https://img.shields.io/badge/Scikit--learn-ML-green) ![Status](https://img.shields.io/badge/Status-In%20Progress-orange)

---

## Project Goal

The goal of this project is to build a clean, reproducible, and well-structured machine learning pipeline for credit risk prediction.

This repository is designed not only to train a baseline model, but also to follow good ML engineering practices:

- Isolated environment setup
- Modular project structure
- Clean data loading and preprocessing
- Reproducible experimentation
- Clear documentation

---

## Dataset

The dataset is stored at:

```
data/raw/LC_loans_granting_model_dataset.csv
```

The dataset contains borrower and loan attributes used to predict default risk.

- Loan amount
- FICO score
- Debt-to-income ratio
- Employment length
- Loan purpose
- Home ownership
- Address information
- Text fields: title and description

**Target variable:** `default`

---

## Project Structure

```
lending-club-credit-risk/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── docs/
│   ├── 00-environment-setup.md
│   ├── 01-project-structure-and-paths.md
│   ├── 02-columns.md
│   └── 03-launch-protocol.md
│
├── notebooks/
│   └── 01-data-loading-and-exploration.ipynb
│
├── src/
│   ├── config.py
│   ├── main.py
│   ├── data/
│   │   └── load.py
│   └── features/
│       └── preprocess.py
│
├── environment.yml
├── pyproject.toml
└── README.md
```

---

## Environment Setup

Create the conda environment with:

```bash
conda env create -f environment.yml
conda activate lending-club-ml
```

---

## How to Run

Run the main pipeline from the project root:

```bash
python -m src.main
```

---
## Current Pipeline Status

| Step | Status |
|---|---|
| Raw data loading | ✅ Complete |
| Basic cleaning | ✅ Complete |
| Target splitting | ✅ Complete |
| Feature dropping (non-useful columns) | ✅ Complete |
| Train / test split | ✅ Complete |
| One-hot encoding | ✅ Complete |
| Feature alignment | ✅ Complete |
| Baseline logistic regression training | ✅ Complete |
| Baseline evaluation (accuracy, ROC-AUC, classification report, confusion matrix) | ✅ Complete |
| Threshold tuning experiment | ✅ Complete |

---

## Planned Improvements

- [ ] Improve feature engineering, especially date-related information such as `issue_d`
- [ ] Try stronger models such as XGBoost or LightGBM
- [ ] Add dedicated model modules for training and evaluation
- [ ] Save processed artifacts and trained models to disk
- [ ] Add clearer result tracking across experiments

---

## Documentation

Additional project notes are available in the `docs/` folder:

| File | Contents |
|---|---|
| `00-environment-setup.md` | Conda environment creation and activation steps |
| `01-project-structure-and-paths.md` | Root path configuration and import patterns |
| `02-columns.md` | Dataset column definitions and feature descriptions |
| `03-launch-protocol.md` | Work session startup checklist and workflow |
| `04-baseline-model-analysis.md` | Baseline model behavior, confusion matrix analysis, and threshold comparison |

---

## Purpose of This Repository

> This repository demonstrates that strong ML projects combine model experimentation with clean engineering, reproducible environments, and clear documentation.

---

## Baseline Model Results

### Logistic Regression (default settings)

- Accuracy: 0.8013
- ROC-AUC: 0.5446
- Recall (default class): 0.00

**Observation:**  
The model achieved high accuracy mainly by predicting almost all clients as non-default.  
In practice, it completely failed to detect the default class, so this result was misleading and not useful for the real objective.

### Logistic Regression (`class_weight="balanced"`)

- Accuracy: 0.5434
- ROC-AUC: 0.5911
- Recall (default class): 0.61
- Precision (default class): 0.24

**Observation:**  
Adding class weighting improved default detection significantly.  
The model became more useful for catching risky clients, but it also created many false positives.

### Threshold Tuning Summary

To better understand model behavior, several thresholds were tested:

| Threshold | Accuracy | Default Recall | Default Precision | Default F1 | Behavior |
|---|---:|---:|---:|---:|---|
| **0.3** | 0.21 | **0.99** | 0.20 | 0.33 | Too aggressive — flags almost everyone |
| **0.5** | 0.54 | 0.61 | 0.24 | 0.35 | More balanced, but still weak |
| **0.7** | **0.80** | 0.00 | 1.00 | 0.00 | Too strict — misses almost all defaults |

### Key Insight

These experiments showed three important things:

- Accuracy alone is misleading in imbalanced classification
- Threshold tuning changes how aggressive the model is
- The threshold changes prediction behavior, but it does not improve the model itself

This is clear because the ROC-AUC stayed around **0.59** across all thresholds, which means the baseline model is still weak overall.

For the full detailed analysis, including confusion matrices and threshold-by-threshold interpretation, see: - `docs/04-baseline-model-analysis.md`

