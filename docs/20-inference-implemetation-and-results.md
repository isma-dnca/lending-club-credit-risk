# Inference Foundation Implementation and Results

At this stage, after building the core foundations of the project, the repository receives its first real inference workflow. So the project can do:
- train a model
- evaluate it
- save the trained model
- save the fitted preprocessor
- save metrics
  
  That already a good foundation for for a strong training-oriented ML engineering project. But as documented before, still not fully answer this practical question:
  > how do we reuse the saved artifacts to make predictions on new unseen data?
  At this point that was gap this milestone was designed to answer and close
 
 So this document is to show what was implemented, verified, why it was implemented that way, and also what can be next milestone.

 ---

 ## Milestone Recap

 The first goal was to introduce a first clean, reusable, package-level prediction workflow.
 The design defined in `docs/18-inference-foundation-design.md` established that the first version of inference should:
- consume a raw CSV file path
- load a saved trained model
- load a saved fitted preprocessor
- reuse deterministic preprocessing from the training side
- generate predicted probabilities
- convert probabilities into predicted classes using a configurable threshold
- return structured prediction outputs
- be protected by automated tests
  
And it was not yet meant to include any API endpoints, Docker, deployment, or service monitoring. At this stage it is intentionally scoped to be a local package level inference foundation. In other words, the purpose of this milestone was to make inference real before making it deployable.

---

## What was implemented

### 1. A dedicated inference package
A new package introduced under:
```bash
src/lending_club_credit_risk/inference/
```
The package currently contains : `__init__.py` and `predict.py`

### 2. Artifact loading helpers
To make artifact path exist before loading, and to explicit failure when required artifacts are missing, internal helper functions was needed to this matter and to load the saved trained model and fitted preprocessor.
This is important and matters because the inference depends entirely on artifact reuse.

### 3. Deterministic preprocessing reuse during inference
reuse the same deterministic preprocessing logic that already used during training was one of the most important implementation decision.

this decision makes sure that the inference does not send ra csv data directly to the saved preprocessor. Instead, it first reproduces the deterministic transformation stage and only then applies the fitted preprocessing object.

### 4. Threshold prediction logic
The inference module now returns both predicted probabilities and predicted classes. The predicted classes are not generated directly by the model itself, but by applying a configurable threshold to the predicted probabilities. This keeps the same philosophy already used in the evaluation layer: probabilities and final decisions are two different things. Instead of hiding the decision rule inside fixed logic, the threshold remains explicit and easy to adjust depending on the use case.

### 5.Inference outputs
The first version of the inference workflow now returns a clean prediction DataFrame containing at least the predicted default probability `default_propability` and the final predicted class `predicted_default`, even more precise `default_propability` is raw probability score returned by `predict_proba()` and `predicted_default` is threshold-based binary decision (0 or 1). 

So if the original input file contains an `id` column, it is preserved in the final output so each prediction can still be linked back to its original row. This makes the output easier to use both programmatically inside other systems and manually when inspecting predictions as a human.

---

## What Was Verified

### New inference tests were added
A dedicated test file was introduced:
```bash
tests/test_inference.py
```
The inference tests currently verify the main behavior of the workflow, including successful predictions on a small synthetic CSV file, validation of the expected output structure, correct prediction row count, and proper failure handling when the saved model or preprocessor artifacts are missing. The tests rely on synthetic CSV inputs, temporary artifact paths, and temporary saved model and preprocessor objects instead of depending on external files or manual setup. This keeps the tests isolated, reproducible, and safe to run automatically inside CI environments.

### Full project test suit passes.
After adding the inference workflow, the full project test suite was executed again successfully.
It confirms not only that the new inference layer works correctly, but also that the existing parts of the repository were not damaged by the new addition. In other words, inference was integrated without breaking the current training pipeline, preprocessing logic, or testing infrastructure already in place.

## Next Milestones  

The next logical milestones after this one is :
- prediction CLI 
After that the project can move toward other milestones:
- Fast API
- Docker
- Deployment
- monitoring
- final MLOps touch 

## Conclusion
The inference milestone was successfully implemented. It introduced:
- a dedicated inference package
- artifact loading
- deterministic preprocessing reuse during prediction
- threshold-aware class generation
- structured prediction outputs
- automated inference tests
  
As the result, the repo now support both sides of the ML workflow:
- training
- prediction
