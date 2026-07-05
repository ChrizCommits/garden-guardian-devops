# GardenGuardian

GardenGuardian is a clean MVP web application for a university DevOps case study. It helps users support wild animals in a garden or local environment with small, seasonal, responsible actions.

The app shows a daily wildlife-support tip, lets a user start a username-only demo session, and awards points, streak progress, and matching animal cards after a completed action.

## Safety note

GardenGuardian provides general wildlife-support ideas only. It is not medical or veterinary advice. The tips avoid unsafe feeding and clearly warn against harmful foods such as milk for hedgehogs, bread for birds, chocolate, processed human food, honey water for wild bees, and salty, spicy, or cooked leftovers.

## Demo login

Login is demo-only. Users enter a username, with no password and no email. This is not production authentication.

## Tech stack

- Backend: Python 3.12, FastAPI, SQLite, SQLAlchemy, Pydantic, pytest
- Frontend: React, Vite, TypeScript

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

## Intentionally not included

CI/CD configuration, GitHub Actions workflows, Docker files, docker-compose, deployment configuration, release process, approvals, and DevOps documentation are intentionally not included. They will be implemented manually later as part of the DevOps case study.

## CI/CD Quality Gate

Changes to the main branch are protected by a pull request workflow. The CI pipeline runs backend tests, builds the frontend, and verifies the Docker build before changes can be merged.