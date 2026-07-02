# GardenGuardian Backend

FastAPI backend for the GardenGuardian MVP.

## Install

From the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

## Run

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

## Test

```powershell
..\.venv\Scripts\python.exe -m pytest tests
```

The app uses SQLite and deterministic local sample data. No external APIs are used.
