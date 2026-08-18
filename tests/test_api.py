from pathlib import Path
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from api.main import app  # noqa: E402


def test_root_endpoint_returns_health_message():
    client = TestClient(app)
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "HealthGuide AI API Running"
