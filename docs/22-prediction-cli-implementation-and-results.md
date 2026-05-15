# Prediction CLI Implementation and Results

At this stage, after building the inference foundation, the repository already has a working prediction workflow at the package level. That meant the project could now:
- train a model
- evaluate it
- save the trained model
- save the fitted preprocessor
- reload artifacts and score new unseen data

That is already a meaningful step forward. But it still does not fully answer a practical question:
> How does a user actually trigger a prediction from the command line without writing Python code?

At this point that was the gap this milestone was designed to answer and close.

This document records what was implemented, what was verified, why the milestone was implemented this way, and what the next milestone can be.


---


## Milestone Recap

The goal of this milestone was to evolve the package entrypoint from a mostly training-oriented interface into a clearer multi-command CLI.
The design defined in `docs/21-prediction-cli-design.md` established that the CLI should support two explicit workflows:
- `train`
- `predict`

And it was not yet meant to include any API endpoints, Docker, deployment, or service monitoring. At this stage it is intentionally scoped to local package-level command-line usability. In other words, the purpose of this milestone was to make prediction accessible before making it deployable.

---

## What Was Implemented

### 1. Explicit CLI subcommands
The package entrypoint was restructured to support two explicit subcommands:
```bash
python -m lending_club_credit_risk train
python -m lending_club_credit_risk predict --input-file path/to/new_data.csv
```
This is the most important user-facing change of the milestone. Before this, the CLI was implicitly training-oriented. Now both workflows are visible and reachable without touching Python code.

### 2. Training CLI alignment
Training was moved into an explicit `train` subcommand instead of remaining an implicit default behavior.
The training workflow itself was not redesigned in this milestone. Its internal behavior still remains responsible for deterministic preprocessing, train/test split, model training, evaluation, and artifact saving. The main change was at the CLI surface, making `train` and `predict` structurally symmetrical inside the command structure.

### 3. Prediction CLI integration
A new `predict` command was introduced to expose the existing inference workflow from the command line.
The prediction command now supports:
- raw CSV input through `--input-file`
- optional model artifact override
- optional preprocessor artifact override
- optional threshold override
- optional output file writing

Internally, the CLI does not duplicate prediction logic. Instead, it delegates prediction work to the existing inference module. This keeps responsibilities clean: the CLI handles command parsing and workflow routing, the inference module handles data preparation and prediction. That separation is one of the strongest architectural outcomes of the milestone.

### 4. Shared artifact path defaults
As part of the CLI work, default artifact paths were centralized more clearly in the configuration layer.
This matters because as the number of user-facing entrypoints increases, a shared understanding of where canonical artifacts live becomes more important. Training outputs, inference defaults, and CLI prediction behavior now all point to the same configuration source.

### 5. Prediction output writing
The prediction command now supports writing results to disk through an `--output-file` argument.
This matters because predictions are often meant to be inspected later, reused by another workflow, archived, or compared across runs. So the CLI is now useful not only for previewing predictions interactively, but also for producing reusable prediction output files.

---

## What Was Verified

### New CLI tests were added
A dedicated test file was introduced:
```text
tests/test_cli.py
```
The CLI tests currently verify the main behavior of the workflows, including `train` command recognition, `predict` command recognition, required `--input-file` behavior, successful CLI prediction execution, and prediction output file writing. The tests rely on synthetic CSV inputs, temporary artifact paths, and temporary output file paths instead of depending on external files or manual setup. This keeps the tests isolated, reproducible, and safe to run automatically inside CI environments.

### Full project test suite passes
After adding the CLI layer, the full project test suite was executed again successfully.
It confirms not only that the new CLI behavior works correctly, but also that the existing parts of the repository were not damaged by the new addition. In other words, the interface grew without breaking the current training pipeline, preprocessing logic, inference workflow, or testing infrastructure already in place.


---


## Next Milestones

The next logical milestone after this one is:
- FastAPI service layer

After that the project can move toward other milestones:
- Docker
- Deployment
- Monitoring
- Final MLOps polish


---


## Conclusion
The prediction CLI milestone was successfully implemented. It introduced:
- explicit `train` and `predict` subcommands
- CLI-level prediction exposure
- shared configuration cleanup for artifact defaults
- prediction output writing
- automated CLI tests

As a result, the repository now exposes its two core workflows more clearly:
- training
- prediction

The project is no longer only modular internally. It is now also becoming clearer and more usable from the outside.