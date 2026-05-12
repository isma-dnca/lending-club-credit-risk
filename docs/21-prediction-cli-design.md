# Prediction CLI Design

---

This is the 2nd milestone. The 1st one was building the inference engine. Milestones started being used after the hardening phase, when the project became more stable and production-ready.

At this point, the core inference works: training from the CLI and running predictions from Python code are possible. But predicting from the CLI cleanly isn't supported yet, training and prediction aren't clearly separated, and inference isn't yet a proper standalone user workflow.

That's what this milestone addresses.

---

## Section 1 - CLI Milestone Goal

The Goal of the prediction CLI milestone is to extend the package entrypoint so that both training and predictions becomes explicit command-line workflows.

So by the end of this milestone the project should support:
- a training command
- a prediction command
- clear command specific arguments
- consistent behavior between package internals and CLI behavior
  
It will essentially focused on command-line usability.
So the purpose here is to turn the current package from: {training entry point plus internal inference code} into {a package with explicit user facing train and predicts commands }

---

## Section 2 - Command Structure

The package entry point was mostly built around training. That made sense before inference existed. But now two distinct workflows are supported:
- training
- prediction

So the CLI should move from single entry point to a multi-command interface, by using explicit subcommands.
The first two subcommands are:
- `train`
- `predict`
That can make the CLI looks like:
```bash
python -m lending_club_credit_risk train
python -m lending_club_credit_risk predict --input-file data.csv
```
Subcommands commands are preferred over flat flags because they are:
- clearer to read
- easier to document
- easier to extend later
- better suited with a package with multiple workflows

So the `train` command stay responsible for:
- running the training workflow
- training the model
- evaluating the model
- saving artifacts
  
Going forward, the CLI should rely on explicit subcommands rather that implicit defaults. Which means the user always chooses and picks the intended workflow instead of training being the silent default.

This also makes the future milestones easier to integrates. New command like `serve` can be added later without making the CLI harder to understand.

---

## Section 3 - Prediction CLI Contract

The `predict` command exposes the existing inference workflow through a  clean CLI.

* Required argument: 
    - `--input-file` : the raw csv file containing new observations to score
  
* Optional argument:
    - `--model-path` override the default saved model location
    - `--preprocessor-path` override the default saved preprocessor
    - `--threshold` override the default decision threshold
    - `--output-file` write prediction results to disk instead of console only
  
  All optional arguments fall back defaults when not provided.
**Typical Usage**:
```bash
python -m lending_club_credit_risk predict --input-file data/new_loans.csv
```

**Fuller example**
```bash
python -m lending_club_credit_risk predict \
  --input-file data/new_loans.csv \
  --output-file outputs/predictions/predictions.csv \
  --threshold 0.3
```
**Internal behavior**
The `predict` command does not re-implement prediction logic. It calls the existing inference workflow, which:
- loads artifacts
- prepares raw input
- generate probabilities
- applies threshold
- returns prediction outputs

**Output Contract**
Prediction results contain at least:
-  `default_probability`
-  `predicted_default`
  
  If an `id` column exists in the input, it is preserved in the output.

  **Failure behavior**
  The command fails clearly when:
  - the input fil is missing
  - required artifacts are missis
  - input data does not satisfy expected schema assumption

---

## Section 4 - Training CLI Alignment

Once prediction becomes an explicit command, training should become one too.
The CLI becomes
```bash
python -m lending_club_credit_risk train
python -m lending_club_credit_risk predict --input-file data/new_loans.csv
```
This keeps both workflows symmetrical and makes the package easier to understand
This milestones only changes how training is exposed through the CLI and not what it does internally.
So the training logic stays the same. The `train` command remains responsible for:
- running the preprocessing pipeline 
- training the model
- evaluating the model
- saving artifacts

### **Supported arguments**
The `train` command keeps its existing configurable arguments:
- `--raw-data-file `
- `--output-dir`
- `--threshold`
  So the flexibility introduced during inference phase is preserved

### **moving a way from implicit defaults**
So the package moves a way from:
```bash
python -m lending_club_credit_risk
```
acting as a hidden training trigger. Instead, the user always states the intended workflow explicitly.
And by doing that, this makes CLI clearer and easier to extend in the future

### **``train vs predict`` commands**
command | responsibility
`train` | creates artifacts
`predict` | reuses artifacts

This gives the package a clean lifecycle structure nad reflects the real separation between model boding an model usage
---

## Section 5 - Test Strategy

The prediction CLI phase should ship with clear and dedicated CLI-test level.

### **File location**
 ```bash
    tests/test_cli.py
 ```
The purpose of this test is:
- subcommand parsing
- command routing
- prediction command behavior
- output writing behavior
- clear failure on invalid usage
  
### **Train command tests**
The internal training workflow is already covered by existing tests. For this milestone, `train` CLI tests only verify:
- the `train` command is recognized
- training arguments are routed correctly
- the command interface stays consistent
  
### **Predict command tests**
The `predict` command gets stronger coverage. The first test cases verify:
 1. Subcommand recognition: `predict` is recognized as a valid subcommand
 2. Required argument behavior: `--input-file` is required and enforced
 3. Happy-path execution: the command runs successfully with:
    - a valid input file
    - a valid model artifact
    - a valid preprocessor artifact
 4. Output file behavior: when `--output-file` is passed, then prediction are written correctly to the disk.
 5. Threshold behavior: when `--threshold` is passed, it is respected during class prediction.
 6. Failure clarify: The CLI fail clearly when:
    - the input file is missing
    - the model artifact is missing
    - the preprocessor artifact is missing
  
### Test design rule
Test should not depends on :
     the full real dataset
     manually created local artifacts
     machine specific states
Instead tests use :
     synthetic training CSV
     synthetic inference CSV
     temporary artifacts paths
     temporary output paths

The preferred approach is to test the real package entry point through argument lists, for example calling `main([...])` rather than teeing isolated parser pieces.

### This phase can considered well tested when:
- `train` and `predict` subcommands behave correctly
- prediction outputs can be writing to disk
- Invalid CLI usage fails cleanly and clearly
- the full project test suite still passes

---

## Section 6 - Implementation Order and Definition Of Done

This milestone is complete when:
 
- the package supports an explicit `train` command
- the package supports an explicit `predict` command
- training behavior remains available through the new CLI structure
- prediction behavior is exposed cleanly through the CLI
- prediction results can optionally be written to disk
- CLI behavior is protected by automated tests
- the full project test suite still passes
- CI still passes successfully
Once all conditions are met, the repository is ready for the next milestone: **API / service layer**.
