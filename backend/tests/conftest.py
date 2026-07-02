from collections.abc import Generator
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_ROOT))

from app import database  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client(tmp_path: Path) -> Generator[TestClient, None, None]:
    database.configure_database(f"sqlite:///{tmp_path / 'gardenguardian_test.db'}")
    database.init_db()
    with TestClient(app) as test_client:
        yield test_client
    database.Base.metadata.drop_all(bind=database.engine)


@pytest.fixture()
def demo_user(client: TestClient) -> dict[str, object]:
    response = client.post("/api/auth/demo-login", json={"username": "moss"})
    assert response.status_code == 200
    return response.json()
