# GardenGuardian

GardenGuardian is an MVP web application for a university DevOps case study. It helps users support wild animals in a garden or local environment with small, seasonal, responsible actions.
The app shows a daily wildlife-support tip, lets a user start a username-only demo session, and awards points, streak progress, and matching animal cards after a completed action.

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

## Run with Docker Compose

From the project root:

```powershell
docker compose up --build
```

The Docker Compose setup builds and starts the containerized backend and frontend services from their Dockerfiles.
The application is available at `http://localhost:8080`.

To stop the containers:

```powershell
docker compose down
```

## DevOps workflow

The project uses GitHub Actions, Docker, and GitHub Container Registry to implement Continuous Integration and Continuous Delivery.

On pull requests and pushes to `main`, the CI workflow:

- runs the backend tests,
- builds the frontend,
- verifies the Docker Compose build.

The protected `main` branch requires successful status checks before merging.

The CD workflow verifies the container images during pull requests. After a merge into `main`, it publishes backend and frontend images with `latest` and commit-SHA tags.

The `staging` environment is processed automatically, while `production` requires manual approval. These environments represent controlled delivery stages; no deployment to a live server is performed yet.
