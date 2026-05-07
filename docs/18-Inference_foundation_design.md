# Inference Foundation Design

The hardening phase gave the repository a strong training, testing, packaging, and CI foundation.
The next major capability is inference.

At this point, the project can:
- train a model
- evaluate it
- save the trained model
- save the fitted preprocessor
- save the metrics
- run tests
- build as a package
- pass CI

But it still cannot fully answer one very important practical question:

> how do we use the saved artifacts later to score new data?

That is why the next chapter is inference foundation.

This document defines the design of that chapter before implementation starts.

---

## Why inference is the next step

A machine learning project is not complete when it can only train.

Training is only one side of the workflow.
The other side is prediction on new unseen data.

At the moment, the repository has:
- a training flow
- a saved model
- a saved preprocessor

But it does not yet have:
- a prediction module
- a reusable inference workflow
- a way to load artifacts and score new observations
- tests for prediction behavior

So even though the training side is strong, the project still misses the capability that makes the model reusable after training.

That is why inference foundation is the most logical next chapter.

---

## What this chapter is supposed to achieve

The goal of this chapter is to give the repository a first clean and reusable inference workflow.

By the end of this chapter, the project should be able to:

- load a saved model
- load a saved preprocessor
- accept new raw data
- apply the same deterministic preprocessing logic used during training
- transform the data with the saved preprocessor
- generate probabilities and predicted classes
- save or return prediction outputs
- verify all this through automated tests

So this chapter is not about deployment yet.
It is about making prediction a first-class capability of the package.

---

## What inference means in this project

In this repository, inference should mean:

- taking new data that looks like the raw training data
- applying the same expected preprocessing path
- using the already trained artifacts
- producing prediction outputs without retraining anything

That means inference must be based on:
- saved model
- saved preprocessor
- training-time assumptions that remain consistent

Inference should not:
- retrain the model
- refit the preprocessor
- silently change feature engineering rules
- depend on full training workflow execution

That distinction is important.

---

## Initial design principles

This inference chapter should follow the same principles used in the hardening phase:

- small enough to understand
- small enough to test
- small enough to validate before moving to API or deployment
- explicit about assumptions
- reusable in future chapters

The idea is to build inference as a clean internal foundation, because later chapters will depend on it:
- prediction CLI
- FastAPI service
- Docker
- deployment
- API tests
- service monitoring

So if inference is weak, all later chapters become shaky.

---

## Main problem to solve

Right now, the training workflow fits and saves:
- model
- preprocessor

But there is no dedicated workflow for:
- reloading them
- preparing new data
- producing prediction outputs

This creates several gaps:

- saved artifacts are not yet truly reusable in a clean package flow
- there is no official prediction entrypoint
- there is no prediction contract
- there is no explicit output format
- there is no automated test for inference logic

So the first job of this chapter is to turn saved artifacts into usable prediction infrastructure.

---

## Scope of this chapter

This chapter should include:

- inference module design
- artifact loading logic
- raw input expectations
- deterministic preprocessing reuse
- probability and class prediction generation
- threshold-aware prediction behavior
- automated inference tests

This chapter should not yet include:

- FastAPI
- Docker
- cloud deployment
- request authentication
- service observability
- model registry
- experiment tracking

Those belong to later chapters.

So the scope here is:
**local, package-level, reusable inference foundation**

---

## Input strategy decision

The first important design decision is:
what should inference accept first?

Possible options are:
- a pandas DataFrame in code
- a CSV file path
- JSON payloads
- both DataFrame and file input

For this chapter, the best first input shape is:

- raw CSV file path

### Why this is the best first choice

Because it is:
- simple
- testable
- consistent with how training already loads data
- easy to expose later through CLI
- easier to validate before designing API payloads

This does not mean DataFrame support is bad.
It only means CSV path is the most practical first contract for this repository.

So the first inference workflow should focus on:
- reading new raw data from a CSV file
- validating the structure
- generating predictions

---

## Output strategy decision

The next decision is:
what should inference produce?

The first version should produce at least:

- predicted probability
- predicted class

Optional later additions can include:
- threshold used
- artifact version
- model metadata
- prediction timestamp

But the first chapter should stay focused.

So the minimal useful output should be a table or DataFrame containing:

- original row identity if available
- probability of class 1 / default
- predicted class after applying threshold

This is enough to make inference genuinely useful.

---

## Threshold behavior decision

Threshold behavior must remain explicit.

During training and evaluation, threshold already became a configurable concept.
Inference should continue the same philosophy.

So the inference workflow should:

- support a threshold parameter
- use a default threshold if none is provided
- make the threshold visible in results or metadata when useful

This matters because prediction is not only about probabilities.
It is also about the decision rule used to convert those probabilities into labels.

So threshold should not become hidden logic again.

---

## Artifact strategy

Inference should rely on saved artifacts, not on retraining logic.

That means it should load:

- saved model artifact
- saved preprocessor artifact

Most likely from the current outputs structure:
- `outputs/models/lightgbm_model.joblib`
- `outputs/preprocessors/preprocessor.joblib`

This chapter should also define clear defaults for those artifact locations while still allowing overrides later.

That will make later CLI and API design much cleaner.

---

## Preprocessing consistency problem

One of the most important design concerns in this chapter is preprocessing consistency.

During training, the pipeline does two kinds of transformation:

1. deterministic preprocessing
2. fitted preprocessing through the saved preprocessor

Deterministic preprocessing includes functions like:
- `basic_cleaning`
- `engineer_issue_date_features`
- `engineer_emp_length`
- `engineer_ratio_features`

The fitted preprocessor then expects the transformed feature structure produced after those deterministic steps.

This means inference cannot simply:
- load the raw CSV
- pass it directly into the saved preprocessor

It must first apply the same deterministic preprocessing logic used during training.

This is one of the key design points of the chapter.

So inference must reuse:
- deterministic preprocessing functions
- saved fitted preprocessor
- saved model

That ordering is essential.

---

## Input schema expectations

Another important design question is:
what raw columns are expected at inference time?

The training path assumes certain raw columns exist in order to support:
- deterministic feature engineering
- dropped-column handling
- downstream transformation

So inference must define its expected input schema clearly.

At minimum, the first version should assume that inference input resembles the same raw schema used during training.

That means the input data should contain the raw columns needed before dropping or transformation.

This chapter should make that assumption explicit.

Later chapters can improve this by introducing stronger input validation and clearer schema contracts.

---

## Module design target

The repository should gain a new inference-focused package area.

A reasonable first structure would be:

```text
src/lending_club_credit_risk/inference/
    __init__.py
    predict.py
```

The purpose of this area would be:
- artifact loading
- deterministic preprocessing reuse for prediction
- preprocessor transformation
- probability and class prediction generation

This keeps inference separate from:
- training
- evaluation
- persistence

That separation is important because prediction is its own responsibility.

---

## Function design target

The first version of inference should expose a function that conceptually does something like:

- accept raw input path
- accept model path
- accept preprocessor path
- accept threshold
- return prediction results

The exact function signature can be decided during implementation, but conceptually the inference contract should be explicit and small.

The function should not:
- mutate training artifacts
- hide threshold behavior
- silently refit anything

It should behave as a clean read-only prediction workflow.

---

## Testing strategy for inference

Inference must be tested from the start.

The test approach should follow the same philosophy used in earlier repo hardening:

- use small synthetic inputs
- avoid dependence on the large real dataset
- use temporary file paths
- isolate inference behavior clearly

A future `tests/test_inference.py` should likely verify:

- saved artifacts can be loaded
- raw CSV can be scored
- predictions contain expected columns
- threshold affects class prediction
- missing artifact paths fail clearly
- invalid input schema fails clearly

This will be important because inference will become the base for:
- prediction CLI
- API endpoint
- Docker service
- deployment workflow

So it should not be added without tests.

---

## Likely implementation order

The chapter should be implemented in this order:

1. define inference input and output contract
2. create inference package and module
3. add artifact loading logic
4. reuse deterministic preprocessing in inference path
5. transform with saved preprocessor
6. generate predicted probabilities
7. convert probabilities into predicted classes using threshold
8. return or save prediction output
9. add inference tests
10. verify local behavior before moving to next chapter

This order matters because it builds from core logic outward.

---

## What this chapter should verify before completion

Before this chapter is considered complete, the following should work:

- a saved model can be loaded
- a saved preprocessor can be loaded
- a new CSV file can be read
- the raw input can pass through the deterministic preprocessing path
- the saved preprocessor can transform the processed input
- the model can produce probabilities
- threshold can produce predicted classes
- inference tests pass

Only after these are true should the project move to:
- prediction CLI
- API layer
- deployment

---

## Risks and design cautions

This chapter must be careful about several things:

### 1. Inference must not retrain anything

Prediction must be read-only with respect to artifacts.

### 2. Preprocessing consistency must be preserved

Training and inference cannot diverge in deterministic transformations.

### 3. Input assumptions must be made explicit

If the raw input schema is expected to match training-time raw data, that should be clear.

### 4. Threshold must stay configurable

It should not disappear into hidden default-only behavior.

### 5. Tests must use synthetic data

Inference tests should remain lightweight and reproducible.

---

## Definition of done

This chapter is done when:

- the repository has a dedicated inference module
- saved artifacts can be reused without retraining
- new raw data can be scored end to end
- probabilities and predicted classes are produced
- threshold is configurable
- inference behavior is covered by automated tests
- the repository is ready to move into prediction CLI design

---

## What comes after this chapter

Once the inference foundation is stable, the next chapter should be:

- prediction CLI

After that, the path can continue toward:
- FastAPI service
- Docker
- deployment
- observability
- final MLOps polish

So this chapter should be seen as:
- the first functional step beyond training
- the base layer for everything user-facing that comes after

---

## Final Design Conclusion

The repository is now strong on the training side.
The next major gap is reusable prediction.

This inference foundation chapter is designed to close that gap by introducing:
- artifact reuse
- prediction workflow
- threshold-aware inference
- test-backed prediction behavior

It does not try to solve deployment yet.
It solves the more fundamental question first:

**how does this project use its trained artifacts to make predictions on new data in a clean, reusable way?**

That is the core purpose of this chapter.