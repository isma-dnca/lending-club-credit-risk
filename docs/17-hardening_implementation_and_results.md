# Hardening Implementation and Results

The purpose was to make the repository cleaner, safer, more reproducible, easier to run, easier to test, and closer to a real professional ML project structure.

So this document is the implementation follow-up of the roadmap defined in `docs/16-repository-hardening-roadmap.md`:
- what was done
- why it mattered
- what was verified
- what the project looks like now
- what still remains for the next chapter

---

## Hardening Goal Recap

At the moment the hardening phase started, the project already had a working modular ML pipeline.
It could:
- load data
- preprocess data
- build and fit the preprocessor
- train a LightGBM model
- evaluate it
- save artifacts

That was already a good engineering improvement compared to the previous monolithic version.

But the repository still had important weaknesses:
- `src` was still acting as the package name
- configuration was still too hardcoded
- there was no automated test suite
- packaging was still weak
- CI did not exist
- repo hygiene still needed work
- README and developer workflow were not yet aligned with the real project state

The hardening phase was meant to solve these issues step by step.

---

## Step 0 — Freeze the Working State

Before starting structural changes, the first action was to freeze the current working project state in git.

This was important because:
- the pipeline was already working
- future refactors could break imports, paths, packaging, or execution
- we needed a clean rollback point before making deeper changes

This step created a safe checkpoint before the hardening work began. By doing this it made the project safer to evolve.
Instead of refactoring on top of uncertainty, we refactored on top of a known working state.

---

## Step 1 — Rename the Importable Package

### Initial problem

The project was still imported using patterns like:

```python
from src.config import RANDOM_STATE
```

This meant that `src` was behaving like the package name.

That worked locally, but it is not the professional structure expected for a real Python package.
`src` should act only as a container, not as the actual importable package identity.

### What was implemented

The project was moved under a real package namespace:

```text
src/lending_club_credit_risk/
```

Imports were updated from `src.` to `lending_club_credit_risk.`

A `__main__.py` entrypoint was added so the package can be executed directly as a module.

### Result

The project now runs through:

```bash
python -m lending_club_credit_risk
```

instead of the older:

```bash
python -m src.main
```
This was one of the most important structural improvements of the whole hardening phase because it changed the project from:

- source files living under `src`
into:
- a real package living inside `src`

This makes packaging, testing, CI, installation, and future service exposure much cleaner.

---

## Step 2 — Parametrize Configuration and CLI

### Initial problem

Important settings were still too hardcoded in the codebase, including values such as:
- raw data path
- output directory
- threshold
- test size
- target column
- columns to drop

This made the project less flexible and less reusable.

### What was implemented

The configuration layer was strengthened in `config.py` with:
- `PACKAGE_ROOT`
- `PROJECT_ROOT`
- `DATA_DIR`
- `RAW_DATA_DIR`
- `PROCESSED_DATA_DIR`
- `OUTPUT_DIR`
- `RAW_DATA_FILE`
- `RANDOM_STATE`
- `TEST_SIZE`
- `DEFAULT_THRESHOLD`
- `TARGET_COLUMN`
- `COLUMNS_TO_DROP`

Environment variable overrides were also introduced for several defaults.

The data loader was refactored so it now accepts an explicit file path instead of reconstructing the path internally from a filename.

The training pipeline was refactored so it now accepts configurable parameters with defaults coming from `config.py`.

The CLI entrypoint in `main.py` was upgraded using `argparse`, and the project now supports options such as:
- `--raw-data-file`
- `--output-dir`
- `--threshold`

### Result

The project can now run in a configurable way, for example:

```bash
python -m lending_club_credit_risk
```

and also:

```bash
python -m lending_club_credit_risk --threshold 0.3
```

This step made the project much more reusable and professional.
The code no longer needs to be edited just to change common runtime behavior.

It also made tests and CI easier to support because inputs and defaults became more explicit.

---

## Step 3 — Add Automated Tests

### Initial problem

At the beginning of the hardening phase, the project had no automated test suite.
That meant:
- refactors were riskier
- regressions were harder to detect
- CI could not verify project behavior

### What was implemented

A root-level `tests/` directory was added.

The following test files were created:

#### `tests/test_preprocess.py`

This file validates deterministic preprocessing behavior:
- `basic_cleaning`
- `split_target`
- `engineer_issue_date_features`
- `engineer_emp_length`
- `engineer_ratio_features`

#### `tests/test_evaluate.py`

This file validates the evaluation layer:
- expected metric keys
- threshold preservation
- valid metric ranges

#### `tests/test_persistence.py`

This file validates persistence logic:
- saving metrics
- parent directory creation
- saved JSON content correctness

#### `tests/test_smoke_pipeline.py`

This file validates the full modular pipeline on a small synthetic dataset:
- raw CSV generation
- training pipeline execution
- model training
- evaluation

### Result

The project now has an initial automated test suite covering:
- preprocessing
- evaluation
- persistence
- end-to-end smoke integration

The suite runs successfully with:

```bash
python -m pytest tests
```
This was one of the strongest hardening gains.

The repository moved from:
- "it worked manually"
to:
- "key project behavior is now protected by automated tests"

That is a major trust and maintainability improvement.

---

## Step 4 — Improve Packaging and Environment Setup

### Initial problem

Packaging and environment setup were still too weak or too duplicated.

There was no strong source of truth for:
- dependencies
- dev dependencies
- notebook dependencies
- test configuration
- package build setup

`environment.yml` was also carrying too much of the dependency definition manually.

### What was implemented

The packaging configuration was strengthened through `pyproject.toml`.

It now defines:
- build system
- project metadata
- runtime dependencies
- optional dependency groups
- package discovery
- pytest configuration
- console script entrypoint

Optional dependencies were separated into groups such as:
- `dev`
- `notebook`

The environment setup was simplified so that `environment.yml` now acts mainly as a bootstrap layer:
- Python
- pip
- editable install with extras

This made `pyproject.toml` the main Python dependency source of truth.

### Result

The project now supports workflows such as:

```bash
python -m pip install -e ".[dev]"
python -m pip install -e ".[dev,notebook]"
python -m build
```

The package can now be built successfully into both:
- source distribution
- wheel

This brought the project much closer to real Python packaging practice.

Instead of being only a local repo that happens to run, it became:
- installable
- buildable
- dependency-aware
- packaging-aware

---

## Step 5 — Add Continuous Integration

### Initial problem

Before CI, all verification happened only on the local machine.

That means the project still lacked:
- clean-machine validation
- automated external proof
- installation verification outside local state

### What was implemented

A GitHub Actions workflow was added under:

```text
.github/workflows/ci.yml
```

The CI workflow was designed to verify both:
- testing
- package build

It now includes separate jobs for:
- test
- build

The CI flow validates:
- repository checkout
- Python setup
- dependency installation
- test execution
- package build

### Result

GitHub Actions now runs successfully and verifies the repository on a clean environment.

That means the project is no longer only saying:
- "it works on my machine"
It is now proving:
- the project installs on a fresh environment
- tests pass
- packaging build succeeds

This was one of the clearest professional signals added during the hardening phase.

The repository now has:
- local verification
- remote verification
- test automation
- package build automation

---

## Step 6 — Repo Hygiene and Public Polish

### Initial problem

The repository still included too much noise and some generated artifacts were not properly treated as such.

README and public-facing workflow documentation were also behind the actual project state.

### What was implemented

Repository hygiene was improved through:
- `.gitignore` cleanup
- ignoring packaging and cache artifacts such as:
  - `build/`
  - `dist/`
  - `*.egg-info/`
  - `.pytest_cache/`

The README was also refreshed to reflect the real project workflow, including:
- correct package command
- current repo structure
- installation workflow
- development workflow
- test workflow
- build workflow
- CI workflow

### Result

The repository surface is now cleaner and more aligned with the actual codebase.

At this stage, the project is no longer only for internal understanding.
It is also starting to become something that another developer, recruiter, reviewer, or future teammate could understand and run more easily.

---

## Important Technical Issues Encountered During Hardening

The hardening phase was not only implementation.
It also revealed important engineering lessons.

### 1. Package move affected path resolution

When `config.py` moved deeper into the package tree, the previous `PROJECT_ROOT` logic became wrong.
This showed that file moves can break path assumptions even when imports are correct.

### 2. Packaging config is stricter in CI than on a local machine

A packaging schema issue around `tool.setuptools.package_dir` versus `package-dir` was exposed by CI.
This was a useful reminder that:
- local success can hide config inconsistencies
- clean CI machines are stricter and more honest

### 3. Dependency synchronization changes the environment state

When the project was installed from `pyproject.toml`, several local package versions were aligned to the declared project versions.
This was an important lesson in what it really means for the package metadata to become the dependency source of truth.

### 4. Tests uncovered project-tooling gaps, not only code gaps

The test phase revealed missing tooling like `pytest`, and later packaging syntax issues in `pyproject.toml`.
This was useful because it showed that hardening includes both:
- code correctness
- toolchain correctness

---

## What the Repository Looks Like After Hardening

After this hardening phase, the repository now has:

- real package structure
- explicit CLI
- configurable project defaults
- automated tests
- package build support
- GitHub Actions CI
- cleaner ignore rules
- stronger README and developer workflow clarity

The project now behaves much more like a real small ML engineering repository than a local experimental script collection.

---

## What Was Verified

The following things were explicitly verified during or after hardening:

### Execution

```bash
python -m lending_club_credit_risk
```

### CLI behavior

```bash
python -m lending_club_credit_risk --help
python -m lending_club_credit_risk --threshold 0.3
```

### Tests

```bash
python -m pytest tests
```

### Packaging

```bash
python -m pip install -e ".[dev]"
python -m pip install -e ".[dev,notebook]"
python -m build
```

### CI

GitHub Actions test and build jobs run successfully.

---

## What Changed in the Engineering Maturity of the Project

Before hardening, the project was already modular and working.

After hardening, the project became:

- importable as a real package
- configurable without editing source
- test-backed
- buildable
- CI-validated
- easier to install and run
- easier to present as a serious engineering project

So the hardening phase did not mainly change the modeling logic.
It changed the **engineering reliability and maturity level** of the repository.

---

## What Still Remains After Hardening

Hardening made the repository strong, but it did not make the project complete.

The biggest remaining gap after hardening is:

- no inference / prediction workflow yet

Other later chapters will also still be needed, such as:
- artifact metadata improvements
- prediction CLI
- API/service layer
- Docker
- deployment
- observability
- final MLOps polish

So the hardening phase should be seen as:
- the completion of the foundation
- not the completion of the whole project

---

## Final Hardening Conclusion

The repository hardening phase was successfully completed.

It transformed the project from:
- a working modular ML training repository

into:
- a stronger, cleaner, testable, buildable, package-aware, CI-validated ML engineering repository

This phase created the technical foundation needed for the next serious chapters.

Because of this work, the project is now in a good position to move into the next major capability:
- inference and prediction workflow

That is the natural next chapter.