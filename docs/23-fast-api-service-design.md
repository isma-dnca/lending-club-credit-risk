# FastAPI service design

The previous milestone, prediction CLI, made the repository's training and prediction workflows accessible from the command line.

At this point, the project already have a strong local workflow foundation that can:
- train a model
- saved trained artifacts
- reload saved artifacts
- make prediction on new raw CSV input
- exposes training and prediction through explicit CLI commands.

However, the repo still does not exposes prediction through a service interface that other applications can call programmatically over HTTP.


---

## Section 1 - FastAPI Milestone Goal

For that reason this milestone is exactly what was needed to close that gap by introducing a first API layer on top of the existing inference workflow.

Therefore, by the end of this milestone, the project should support:
- a small FastAPI application
- a health or status endpoint
- a prediction endpoint
- structured request and response behavior
- service-level tests

Concretely, the purpose here is to make prediction available as a service before moving into containerization and deployment.


---


## Section 2 - Service Module Structure

FastAPI service should be introduced as its own package inside the main project root.
The new service module area:
```text
src/lending_club_credit_risk/api/
```
At this level the module would be small intentional so we can scale and grow as the project grows:
```text
src/lending_club_credit_risk/api/
├── __init__.py
├── app.py
└── schemas.py
```
`__init__.py`: To make the directory as python package
`app.py`: The main Fast api application should live in this python file, it will be responsible for the creation of the FastAPI app, route definition, endpoint-to-inference wiring, and service local orchestration.
`schemas.py`: This file will be responsible for request and response models.

This structure is intentionally small because it is meant to become the foundation for later service-services milestones such as:
- containerization 
- orchestration
- deployment
- service hardening
- and monitoring


---


## Section 3 - API contract

At this level the version of the FastAPI service we expose a minimal but useful HTTP interface.
so the initial endpoint set should be :
  
  - `GET /health`
  - `POST /predict`

### `GET /health`: 
The purpose of the health endpoint is to confirm that the service is running and reachable.
for example the response can be minimal like:
```json
{
    "status": "ok"
}
```


### `POST /predict`
The prediction endpoint should expose the existing inference capability through JSON input.
In the previous milestone, the CLI workflow is file-based. The API should not expect a CSV file path.
Instead it should accept one raw observation as a JSON request body.

As a summary:

 1. the first version of the prediction endpoint should support:
   - one observation per request
   - raw feature input
   - and prediction output using the project default threshold

1. The response should contain at least:
   - `default_probability`
   - `predicted_default`

If an `id` is included in the request, it should be preserved in the response.

3. Also one other important thing; the API contract should be aligned with the inference contract:
   - the service accept the aw input values
   - the service reuses the deterministic preprocessing
   - the service reuses saved artifacts
   - the service returns both probability and threshold based class output
  
4. Request validation should use Pydantic models as the source of truth. If a request is invalid, the system should return a clear error instead of failing silently.


---


## Section 4 - Inference Integration Strategy

In one sentence for this section, the FastAPI service layer should not re-implement predict-logic.

At this moment, the main entrypoint for the public inference is file-based through `predict_from_csv(..)`.
That works well for local and CLI workflows, but is doesn't match the API contract, because the API shoul accept JSON input rather than  a CSV file.

In order to keep the architecture clean, the inference module must be the single source of prediction logic.

So the approach that I will choose is to to keep `predict_from_csv(..)` for file base-workflows and introduce in the same time in-memory inference helper such as : `predict_from_dataframe(...)`

This helper should reuse the same inference workflow:
- deterministic preprocessing
- excluded-column handling
- saved preprocessor loading
- saved model loading
- probability generation
- threshold-based class generation
- structured output formatting

with that structure:
- The CLI can continue using `predict_from_csv(..)`
- the API can convert validated JSON input into one-raw DataFame and call `predict_from_dataframe(...)`
  
This approach keeps prediction behavior consistent across interfaces and avoids duplicating model-serving logic inside the API layer

the responsibility split should reamin:
- `inference/` owns prediction logic
- `api/` owns HTTP exposure, request validation, and response formatting
  
By doing this we are making sure that API is not another prediction engine. It is new inference on top of existing inference layer.


---


## Section 5 - Test Strategy

As all previous tests, the API tests should live in dedicated file like:
```text
tests/test_api.py
```
The main purpose of this tests is to validate:
- route behavior
- request validation
- prediction response structure
- service to inference integration
- failure clarity for invalid request or missis artifacts

So the first version of tests API should cover the following areas:
1. **Health endpoint tets**
2. **Prediction success Path**
3. **Request validation failure tests**
4. **Artifact related failure test**
5. **Isolated test setup**


---


## Section 6 - Implementation order and definition aof done

The implementation order should be:

1. create the `api/` package structure
2. define request and response schemas
3. add the FastAPI app factory and health endpoint
4. extend the inference layer with an in-memory prediction helper
5. add the prediction endpoint
6. add API tests
7. verify that the full project test suite still passes
8. confirm the service works locally

A more detailed implementation sequence should be:

### Phase A — Service structure
- create `src/lending_club_credit_risk/api/`
- create `__init__.py`
- create `app.py`
- create `schemas.py`

### Phase B — API contract foundation
- define request and response models
- keep the request schema aligned with raw inference input expectations

### Phase C — Inference integration
- add `predict_from_dataframe(...)`
- keep prediction logic centralized in `inference/`
- avoid duplicating prediction logic in the API layer

### Phase D — Route implementation
- implement `GET /health`
- implement `POST /predict`
- connect validated request payloads to the inference layer

### Phase E — Testing
- add `tests/test_api.py`
- test health endpoint behavior
- test prediction success path
- test request validation failures
- test at least one artifact-related failure path

### Phase F — Verification
- run API tests locally
- run the full project test suite
- confirm the FastAPI app responds correctly in local execution

### Definition of done

This milestone is complete when:

- the repository has a dedicated API package
- the FastAPI app can be created successfully
- the health endpoint works
- the prediction endpoint accepts valid requests
- prediction responses contain the expected fields
- invalid requests fail clearly
- API behavior is protected by automated tests
- the full test suite still passes

Once those conditions are true, the repository will be ready for the next milestone:
- containerization / Docker

