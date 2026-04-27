# Repo Hardening Roadmap
## Why documenting this?

At this point, the project already has a working modular machine learning pipeline. So far, our pipeline can do
    - load data
    - apply deterministic transformation
    - build & fit preprocessor
    - train a LightGBM model
    - evaluate the model
    - save the trained model
    - save the fitted preprocessor
    - save the metrics
This workflow confirms that the project is no longer a monolithic script or notebook experiment. It has become a working modular ml pipeline. At this level, it is not yet reflecting a final professional level. That's why I decided that the next step would be repo hardening. Which means taking the actual project that already works and making it stronger, cleaner, professional level, more test able, reproducible, and a project that can be trust.

Because at this step any change on the code will affect a lot of and will be dangerous for the workflow that is builded so far. This doc is for defining the repo hardening roadmap before touching code again.

So the goal here is to improve the project while keeping the detailed understanding of every decision.

-------

## Current state of the project

The code is separated into modules :
- `src/features/preprocess.py`
- `src/features/preprocessor.py`
- `src/pipeline/train_pipeline.py`
- `src/modeling/train.py`
- `src/modeling/evaluate.py`
- `src/persistence/save_artifacts.py`
- `src/main.py`
  
And the pipeline executed successfully from end-to-end, that produced :
- trained model
- fitted preprocessor
- metrics report
  
And the artifacts saved are :
- `outputs/models/lightgbm_model.joblib`
- `outputs/preprocessors/preprocessor.joblib`
- `outputs/reports/metrics.json`

So to this point, the current version of the project is working successfully, so any future change must protect the current behavior while making the repo hardening.

-------

## But why hardening is needed

At this point we build the project and we made it **Modular Working ML Pipeline**. But also it contains a lot of engineering problems, by solving them, the project will upgraded and level up to **Professional, Testable, Reproducible ML Repository**.
So in order to make the project fully pro, we need to fix some engineering problems that are still weak in the current version. Some of them are :
    - the package is currently imported as `src`
    - the project is not yet structured as a real installable python package.
    - the configuration is still to hardcoded, which means values are written directly in the code instead of being stored in a config file or environment variables.
    - there is no automated test suite yet
    - there is no CI yet
    - repo cleaning still needs work
    - README still need improvements to stat aligned with the code
    - generated files should not stay versioned
    - and the project should become easier to run in any other machine not oly mine
  
-------

## Main principles of this hardening phase 

Each hardening phase must be :
- small enough to understand
- small enough to test
- small enough to commit cleanly
- documented before moving to the next step or implementation
- verified then move to the next step
  
By reflecting those small principles, the hardening phase will move smoother and we can build a repeatable and professional blueprint or pattern that can respect and can be reused in future project. Like a template for future ML repo.

-------

## Global hardening order

So the hardening work will follow this order :
1. freeze the current working state
2. rename the importable package properly
3. parametrize configuration and CLI 
4. add automated tests
5. improve packaging and environment setup 
6. add CI
7. clean repo

so : 
I will attack and do CI, MLOps, and README
only after :
the project installs, runs, and has stable commands and tests.

## Step 0 - Freeze the current working state

Before we touch anything else, we need to commit what's working right now. The modular pipeline runs, artifacts get created, and we don't want to lose that clean state before refactoring imports or package structure. This commit is our safety checkpoint, so we can always roll back to a version that actually works.

```bash
(lending-club-ml) PS C:\Users\Utilisateur\...\lending-club-credit-risk> git log --oneline -5
e29c3bd (HEAD -> main, origin/main, origin/HEAD) docs(readme): update README to reflect modular ML pipeline structure
fe071c2 Refactor doc 14 and doc 15
0120fe2 Add first end-to-end execution of modular ML pipeline with artifact saving
c4187d9 Refactor main.py file from  monolithic training script into modular pipeline with artifact saving
339bbd3 Refactor main training entry point: orchestrate pipeline, evaluation, and artifact saving
```

So the checkpoint is in. ``e29c3bd`` is our safety net, modular pipeline committed, pushed to ``origin/main``, and we can always roll back to this working state before we touch anything else. This step protects the current state and it is successfully freezed.

-------

## Step 1 - Rename the importable package
At tis point my project uses imports like :
```bash
from src.config import RANDOM_STATE
```
so from the previous command we actually making `src` acting as the package name.
This fine and works perfectly locally, but professionally, it is not the recommended package structure that is suitable to use.
`src` should act only as a `container``and not as the real package. The real package should have the project name to reflect the the main manner and goal of the project.
So the target option name could be : 
```text
lending_club_credit_risk
```
And the the structure could be similar to this structure :
```text
src/
└── lending_club_credit_risk/
    ├── __init__.py
    ├── __main__.py
    ├── config.py
    ├── main.py
    ├── data/
    ├── features/
    ├── modeling/
    ├── persistence/
    └── pipeline/
```
By adopting this structure, the package becomes importable by its real name. The project becomes and respect Python packaging standards. imports, tests, and CI become cleaner. 
So what should be done practically is :
    - we move current project under `src/lending_club_credit_risk/`
    - updates imports firm `src.` to `lending_club_credit_risk.`
    - add `__main__.py`
    - remove old `src/__init__.py`
    - remove generated `egg-info` from version control
  
So what should work after this step is :
```bash
python -m lending_club_credit_risk
```
instead of :
```bash
python -m src.main
```
-------

## Step 2 - Parametrize configurational & CLI 
At this step the main goal is to make the project easier to configure.
We can do that by : 
    - keeping good defaults
    - allow overrides when is needed 
    - avoid changing source code just to change data path or threshold.
Here is our current situation : we have some values are still too hardcode like : threshold, raw data path, test size, target column, column to drop...
Hardcoding is fine for local and learning project, but for professional project, these values should be easier to control. In this professional view, and at this point of the project, the following values should be configurable:
    - `raw_data_file`
    - `output_dir`
    - `threshold`
    - `test_size`
    - `target_column`
    - `columns_to_drop`
  By doing this the CLI can and should allow commands like 
  ```bash
  python -m lending_club_credit_risk
  ```
  And also the CLI should allow :
  ```bash
  python -m lending_club_credit_risk \
    --raw-data-file data/raw/LC_loans_granting_model_dataset.csv \
    --threshold 0.35 \
    --outputs-dir outputs
```
By configuring and doing this : 
    - future users do not need to edit the code to run the project
    - the project becomes easier to run in different environment
    - test and CI becomes easier
    - threshold becomes an explicit decision instead of hidden logic.

So what should work after this step is : 
    - default run works
    - custom data path and custom thresholds also works 
    - custom output directory works.
  
-------
  
## Step 3 - Add automated tests
So after the package name is clean and the configuration and CLI are set up, the next major step is tests.
So the goal of this step by adding automated tests is to :
    - to prove that the project works
    - protect against future refactoring mistakes 
    - and obviously make the repo trustworthy
As prime and a perquisite default; TESTS should not depend on the real Full dataset. Instead, tests should use: small synthetic DataFrames. Temporary CSV files. and Temporary output paths.
This is important because the dataset may be large or containing sensitive data so not public.

So TEST GROUPS to add : 
1. **Preprocessing Tests** 
   The file :
    ```text
    tests/test_preprocess.py
    ```
    Should test : `basic_cleaning` `split_target` `engineer_issue_date_features` `engineer_emp_length` `engineer_ratio_features` . The purpose of this, is to make sure that deterministic transformation behave as expected.

2. **Evaluation Tests**
   The file : 
    ```text
    tests/test_evaluate.py
    ```
    Should test : `evaluate_model` returned metrics, threshold is preserved, and metrics are in valid range. The purpose of this, is to make sure evaluation logic returns a structured and reusable dictionary.

3. **Persistence Tests**
   The file :
   ```text
   tests/test_persistence.py
   ```
   Should test : saving metrics, and automatic parent directory creation. The purpose of this is to make sure saving functions actually write outputs correctly.

4. **Smoke Pipeline Tests**
   The file : 
   ```text
   tests/test_smoke_pipeline.py
   ```
   Should test : create tiny synthetic dataset. run preprocessing pipeline. Train model. evaluate model. The purpose of this is, to make sure the main pieces work together without relying on the real dataset. and the pipeline is stable.

   So what should work after this step is :
   ```bash
   pytest
   ```
-------

## Step 4 - Improve packaging  & environment setup
Once tests exists, the next step is packaging.
the goal of this step is to make the project installable, dependencies clearer, local setup clearer, and also make CI easier.
So the central file should become :
```text
pyproject.toml
```
and this file should define : 
package metadata. runtime dependencies. dev dependencies. optional notebooks dependencies. consol script. And pytest configuration.
So the environment file become simpler. And Instead of duplicating every package manually, `environment.yml` should mainly bootstrap :
    - Python
    - pip
    - editable project install.
By doing this :
    - `pyproject.toml` becomes the source of truth for the Python package.
    - `environement` becomes a conda setup helper
    - dependency management becomes cleaner
    - installation becomes closer to real Python project practice

So what should work after this step is : 
```bash
python -m pip install -e ".[dev]"
python -m pip check
pytest
python -m build
```

-------

## Step 5 - Add CI
After the project installs locally, the tests pass, the next step is CI.
CI means that the project is checked automatically outside my machine and to kill that random excuses :it worked in my machine.
The goal of this step is actually run the tests on github. Verify installation, verify package build and finally prove that the project works in a clean environment.

so we are going to add : 
```text
.github/workflows/ci.yml
```
and then the CI should run : 
- check code
- setup python
- install project with dev dependencies
- run `pip check`
- run `pytest`
- build package

This matters because : external proof of correctness. then more trust fro reviewers. and less dependence on my local machine and giving professional repo signal.

So what should work after this step is : 
GitHub Actions workflow runs successfully and README can show CI badge.

-------

## Step 7 - Repo hygiene & Public polish
After the packages, tests, and CI are stable, the final hardening step is public polish. Which means to make the repo clean and readable for other people. Refactoring README to actually marches the real commands and also improve the Github surface.

This step can include : 
- update ``.gitignore``
- remove _``_pycache__``
- remove ``.ipynb_checkpoints``
- remove ``egg-info``
- decide license
- add GitHub repo description
- add topics
- add CI badge to README
- update README commands after CLI is stable

-------

## Recap :
The hardening phase is about to take My ML pipeline that is already working and making it stronger and professional. 
working modular pipeline
-> importable package
-> configurable CLI
-> tests
-> packaging
-> CI
-> repo polish

