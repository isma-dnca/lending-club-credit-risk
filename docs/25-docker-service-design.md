# Docker Service Design

The previous milestone gave the project a working HTTP prediction interface. Clean endpoints, proper structure, inference running through a real API.

But it still only works on my machine.

The service depends on a local Python environment, local package installation, local setup decisions I made at some point and probably don't fully remember. Hand this to someone else or spin it up on a different machine and things will break in ways that are annoying to debug and hard to explain.

This milestone closes that gap.

The goal is simple: package the FastAPI service into a container image that runs the same way everywhere. Controlled environment, predictable dependencies, a single startup command, no surprises.

By the end of this milestone the project will support:

- a `Dockerfile` for the FastAPI service
- a containerized runtime for the API
- predictable dependency installation inside the container
- a clear container startup command
- verification that the service runs correctly inside the container

Portable before deployable. That's the order that makes sense.

## Section 1 — Container Structure and Files

Two files. That's the whole milestone in terms of new surface area.

A `Dockerfile` at the repository root packages the FastAPI service into a container. A `.dockerignore` at the repository root keeps that container clean, no virtual environments, no caches, no local config bleeding into the image.

I've seen containerization start with six files before the service even runs inside a container once. It always creates confusion that's hard to unwind later. So I'm starting with the minimum, proving it works, and adding more only when there's a real reason to.

### `Dockerfile`

The dockerfile has one job: describe exactly how the FastAPI service gest pack aged into container image. Nothing more than that.

In practice that means 5 things:
1. Picking a base Python image that matches the runtime
2. Setting a working directory so everything inside the container has a predictable home
3. Installing the dependency from the project requirement
4. Copying the application code into the image.
5. Anf finally defining the command that starts the service when the container runs.
   
Tht's the full scoop of this file.

### `.dockerignore`

This is one of those files thats feels minor until you skip it. Small file that has real consequences.
So This file should exclude at minimum:
- `.git/`
- `__pycache__/`
- `.pytest_cache/`
- local virtual environment folders
- notebooks
- local output directories


## Section 2 - Runtime Contract

The container runs one process: the FastAPI server launched through Uvicorn, pointed at:
```text
lending_club_credit_risk.api.app:app
```
The container should run the service through:
- host : `0.0.0.0`, binding to it allows the service to be reached from outside the container
- port: `8000`, is the conventional local runtime target and keeps things predicable across environment.

That's the full runtime contract for this milestone.

PS: The container does not train a model on startup. It does not build artifacts. It does not run the training pipeline. A container that trains and serves at the same time is two things pretending to be one. It makes both harder to reason about.

At  runtime, the external behavior of this container is exactly 3 things:
1. HTTP requests to `/health`
2. HTTP requests to `/predict`
3. Structured HTTP response from those endpoints.


## Section 3 - Service Packaging Strategy

The base image is a slim Python 3.11, minimal runtime, no bloat, aligned with what the project already uses.

Dependencies install through `pyproject.toml`, not editable mode. Editable installs are for development. The container is not a development environment. That distinction is worth being deliberate about.

The build includes 3 things:

- `pyproject.toml`
- `README.md`
- `src/`

The trained model and preprocessor are copied directly into the image. Simple, self-contained, easy to verify locally. Volume mounts and artifact registries come later when there's a real reason for them.

Tests don't run inside the build. The CI pipeline handles that. The container's only job is to package the service and run it cleanly.

Reproducibility. Minimal scope. Nothing in the image that doesn't need to be there.


## Section 4 - Test And Verification Strategy

Verification here is practical. The goal is not a full test suite, it is proof that the service builds, starts, nad responds correctly inside a container.

The minimum verification flow:
1. Build the docker image
2. Run the container
3. Confirm the service starts without crashing
4. Call `GET /health`
5. Call `POST /predict`
6. Confirm both return valid response

### Health verification 

`GET /health` is the first check. if it responds, the container started correctly, Uvicorn is running, and the API is reachable through the exposed port.

If this fails, nothing else worth checking. 

### Prediction verification

`POST /predict` goes further. A valid prediction response confirms that routing work, the inference layer is reachable, and the model and preprocessor are present and loadable inside the container

One request that proves the full path works end to end.


## Section 5 — Implementation Order and Definition of Done

The implementation follows a fixed order. Each phase builds on the previous one and no skipping ahead.

### Phase A — Container setup
- Create `.dockerignore`
- Create `Dockerfile`

### Phase B — Packaging
- Choose the base Python image
- Copy the required project files
- Install dependencies from package metadata
- Define the container startup command

### Phase C — Artifact integration
- Include the trained model artifact
- Include the fitted preprocessor artifact
- Confirm artifact paths are usable inside the container

### Phase D — Local verification
- Build the image
- Run the container
- Call `GET /health`
- Call `POST /predict`

### Phase E — Final validation
- Confirm the containerized service behaves correctly
- Confirm the project still works correctly outside the container

### Definition of Done

This milestone is complete when:

- the repository has a `Dockerfile`
- the repository has a `.dockerignore`
- the image builds successfully
- the container starts without crashing
- the service is reachable through the expected port
- `GET /health` returns a valid response
- `POST /predict` returns a valid prediction
- the required artifacts are present and loadable inside the container

When all of that is true, the service is portable. The next milestone can move toward deployment and runtime hardening.