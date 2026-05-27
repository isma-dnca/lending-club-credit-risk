# FastAPI service implementation & results

At this stage, after finishing the and building prediction CLI milestone, the repo already had a working prediction workflow that could be triggered locally from python code and the command line.

But still one practical gap: 

> How can another system call the prediction workflow programmatically oVER HTTP instead of through command line that is done locally?

That was the gap this milestone is designed to close.

So the purpose of this chapter was to introduce a small service layer on top of the existing inference workflow that is already done before.


## Section 1 - What was implemented

### 1. Dedicated API Package

A new service module at `src/lending_club_credit_risk/api/` adds a thin API layer on top of the existing project without modifying its core logic.

This is an initial version (v1). The package currently contains:

- `__init__.py` : package initialization and public exports
- `schemas.py` : Pydantic models for request/response validation
- `app.py` : FastAPI application and route definitions

### 2. Schema-based API contract

Pydantic models define the API contract in `schemas.py`. The first version includes three models:

- `HealthResponse` : confirms the service is live
- `PredictionRequest` : accepts raw JSON with the loan features required by the model
- `PredictionResponse` : returns `default_probability` (float), `predicted_default` (bool), and an optional `id` if provided in the request

These models make the service boundary explicit: input is validated before reaching the model, and output structure is enforced before returning to the caller.

### 3. FastAPI app and health endpoint

The application is initialized in `app.py` using a factory pattern: a `create_app()` function constructs and configures the FastAPI instance, with `app = create_app()` used at runtime.

This pattern makes the app easier to test (the factory can be called with different configs in test fixtures), configure per environment, and extend with additional routers later.

The first route added is:

- `GET /health`: returns a minimal `HealthResponse`, confirming the app can be instantiated, reached, and validated through tests

### 4. Inference integration for in-memory use

The existing inference workflow was built around CSV file input; sufficient for local and CLI use, but not suitable for an API layer that receives JSON over HTTP.

The inference module was extended with a DataFrame-based entry point that allows the API to:

1. Validate the incoming JSON request against the `PredictionRequest` schema
2. Convert it into a single-row DataFrame
3. Pass it through the same prediction logic already used by the CLI workflow
   
### 5. Prediction endpoint

A `POST /predict` endpoint exposes the existing prediction capability over HTTP. It accepts a validated `PredictionRequest`, converts it to a single-row DataFrame, calls the inference layer, and returns a structured `PredictionResponse`.

This is the most important user-facing capability introduced by the milestone. The route it does not:
- Re-implement preprocessing
- Re-implement threshold logic
- Load artifacts independently of the inference layer

Instead, it acts as a service wrapper around the reusable prediction engine already present in the repository. The core architectural goal was to expose prediction through the API without turning the API into a second prediction engine.


## Section 2 — API tests

A dedicated test file was added at `tests/test_api.py`. These tests verify the first service-level behaviors introduced in this chapter:

- Successful `/health` response
- Successful `/predict` response for a valid request
- Validation failure for an invalid `/predict` request

### Verified behaviors

1. **Health endpoint** : the app initializes correctly, returns HTTP 200, and the response matches the expected schema
2. **Prediction endpoint** : a valid request payload is accepted, the saved model and preprocessor artifacts are loaded, and the response contains the expected prediction fields
3. **Validation** : missing required fields cause the request to fail validation before reaching the inference layer
4. **Non-regression** : training, inference, CLI, persistence, preprocessing, and smoke-pipeline behavior are unaffected by the new service layer


## Section 3 - Milestone summary

After this milestone is completed, the repo supports 4 distinct layers of workflow:

- Training
- Artifact persistence
- Reusable inference
- Service exposure through FastAPI
  
In practical terms, the project can now:

- Train a model from structured project code
- Save model, preprocessor, and metrics artifacts
- Reload saved artifacts for prediction
- Expose prediction locally through CLI commands
- Expose prediction programmatically through HTTP endpoints


## Section 4 - Conclusion 

## Conclusion

This milestone introduced the FastAPI service layer: a dedicated API package, schema-based request and response models, an app factory, a health endpoint, a prediction endpoint, and API-level tests covering both success and validation behavior.

The repository now supports not only training and reusable inference, but also service-level prediction exposure over HTTP; a meaningful step beyond internal Python code and CLI use.

The project can now act as a small prediction service, which makes the path toward Docker, deployment, and broader MLOps work concrete.

