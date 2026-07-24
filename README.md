# GardenGuardian

GardenGuardian is an MVP web application for a university DevOps case study. It helps users support wild animals in a garden or local environment with small, seasonal, responsible actions.
The app shows a daily wildlife-support tip, lets a user start a username-only demo session, and awards points, streak progress, and matching animal cards after a completed action.

## Safety note

GardenGuardian provides general wildlife-support ideas only. It is not medical or veterinary advice. The tips avoid unsafe feeding and clearly warn against harmful foods such as milk for hedgehogs, bread for birds, chocolate, processed human food, honey water for wild bees, and salty, spicy, or cooked leftovers.

## Demo login

Login is demo-only. Users enter a username, with no password and no email. This is not production authentication.

## Tech stack

- Backend: Python 3.12, FastAPI, SQLite, SQLAlchemy, Pydantic, pytest
- Frontend: React, Vite, TypeScript
- Containerization: Docker and Docker Compose
- CI/CD: GitHub Actions
- Container registry: GitHub Container Registry / GitHub Packages

## Install

From the project root, install backend and frontend dependencies once:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
cd frontend
npm install
cd ..
```

If npm fails with a local certificate error, use:

```powershell
cd frontend
npm install --strict-ssl false
cd ..
```

## Run the backend

Open a first terminal:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The backend runs at `http://127.0.0.1:8000`.

## Run backend tests

From the project root:

```powershell
.\.venv\Scripts\python.exe -m pytest backend\tests
```

## Run the frontend

Open a second terminal:

```powershell
cd frontend
npm run dev
```

The frontend runs at `http://127.0.0.1:5173` and calls `http://127.0.0.1:8000` by default. You can override that with `VITE_API_BASE_URL` if needed.

## Quick start after install

```powershell
# Terminal 1
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

```powershell
# Terminal 2
cd frontend
npm run dev
```

Then open `http://127.0.0.1:5173`.

## Why SQLite

SQLite keeps the MVP simple, local, and easy to inspect for a university case study. It is enough for the demo data and user flow while leaving room to discuss later production database choices.

## DevOps implementation status

The DevOps implementation is part of the university case study and includes version control, containerization, Continuous Integration, Continuous Delivery, and a protected pull request workflow.

Implemented DevOps components:

- Git and GitHub for version control and repository hosting
- Feature branch workflow with pull requests into `main`
- Protected `main` branch with required status checks
- GitHub Actions CI workflow
- GitHub Actions CD workflow
- Dockerfiles for backend and frontend
- Docker Compose for local multi-container execution
- GitHub Container Registry / GitHub Packages for published container images

## Run with Docker Compose

From the project root:

```powershell
docker compose up --build
```

The Docker Compose setup builds and starts the containerized backend and frontend services from their Dockerfiles.

To stop the containers:

```powershell
docker compose down
```

## CI workflow

The project uses GitHub Actions for Continuous Integration.

The CI workflow runs on pull requests targeting `main` and on pushes to `main`.

The CI pipeline performs these checks:

- Backend dependency installation
- Backend tests with pytest
- Frontend dependency installation
- Frontend production build
- Docker build verification through Docker Compose

This ensures that code changes are automatically built and tested before they can become part of the protected `main` branch.

## Branch protection and quality gate

The `main` branch is protected by a pull request workflow.

Before a pull request can be merged, the required GitHub Actions checks must pass:

- Garden Guardian CI / Backend tests
- Garden Guardian CI / Frontend build
- Garden Guardian CI / Docker build

This creates a quality gate: code changes are reviewed through a pull request and technically validated before integration into `main`.

## CD workflow

The project uses GitHub Actions for Continuous Delivery.

The CD workflow builds Docker images for:

- Backend
- Frontend

In pull requests, the workflow builds the images to verify that they are buildable.

After changes are merged into `main`, the workflow publishes the images to GitHub Container Registry / GitHub Packages.

Published package names:

- `garden-guardian-devops-backend`
- `garden-guardian-devops-frontend`

This provides versioned, deployable container artifacts after successful integration.
After publication, the workflow processes the `staging` environment automatically. The `production` environment requires manual approval before the workflow can continue.

## Delivery status

This project implements Continuous Delivery, not full Continuous Deployment.

That means:

- Code is automatically tested.
- Docker images are automatically built.
- After a merge into `main`, the images are published with `latest` and commit-SHA tags.
- The `staging` environment is processed automatically.
- The `production` environment requires manual approval.
- No deployment to a live server or cloud platform is performed yet.

The GitHub Environments represent controlled delivery stages, not separate running servers. A future extension could deploy the published images to real staging and production systems.


