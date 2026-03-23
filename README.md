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
| Baseline logistic regression setup | ✅ Complete |

---

## Planned Improvements

- [ ] Train the baseline logistic regression model
- [ ] Evaluate performance with classification metrics (accuracy, AUC-ROC, F1)
- [ ] Refactor preprocessing into reusable, testable functions
- [ ] Add dedicated model modules for training and evaluation
- [ ] Improve feature documentation and column descriptions
- [ ] Save processed artifacts and trained models to disk

---

## Documentation

Additional project notes are available in the `docs/` folder:

| File | Contents |
|---|---|
| `00-environment-setup.md` | Conda environment creation and activation steps |
| `01-project-structure-and-paths.md` | Root path configuration and import patterns |
| `02-Columns.md` | Dataset column definitions and feature descriptions |
| `03-Launch-Protocol.md` | Work session startup checklist and workflow |

---

## Purpose of This Repository

> This repository demonstrates that strong ML projects combine accurate models with clean engineering, reproducible environments, and clear documentation.

---

## Baseline Model Results

### Logistic Regression (default settings)

- Accuracy : 0.8013
- ROC-AUC : 0.5446
- Recall : 0.00 (for default class)
  
  **Observation:**
  The model achieved high accuracy 80% by predicting mostly the non-default class (class 0)
  It is completely failed to detect the default class (class 1), so it is useless and ineffective for desired outcome and the actual task that we are targeting.
  So the problem here is that our data is not balanced.

  ### Logistic Regression (`class_weight="balanced"`)
  - Accuracy: 0.5434  
  - ROC-AUC: 0.5911  
  - Recall (default class ): 0.61  
  - Precision (default class): 0.24  
  
  **Observation:**
  Adding class weighting improved the detection of default cases significantly. However, precision is low 24%, meaning many predicted defaults are incorrect (detecting false positive)

  ### key insight 
  This experiments highlights the impact of class imbalance.
  We have indeed noticed that *Accuracy* alone is misleading. Thus, a model can appear strong while being useless. *Recall* and *ROC-AUC* gave us a good insight for this problem 

  So, the balanced model is more realistic baseline, even when the accuracy is low.