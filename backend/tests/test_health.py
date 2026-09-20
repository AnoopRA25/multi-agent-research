from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "Multi-Agent Research System"
    assert data["status"] == "running"
    assert data["version"] == "0.1.0"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["environment"] == "development"
    assert data["llm"]["provider"] == "Google Gemini"
    assert data["llm"]["model"] == "gemini-2.5-flash"
    assert data["llm"]["configured"] is True