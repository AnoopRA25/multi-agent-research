from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_list_runs():
    response = client.get("/runs")

    assert response.status_code == 200

    data = response.json()

    assert "runs" in data
    assert isinstance(data["runs"], list)


def test_get_existing_run():
    response = client.get("/runs/1")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 1
    assert data["query"] == "Test research query"
    assert data["report"] == "Test report"
    assert data["critique"] == "PASS"
    assert data["status"] == "completed"


def test_get_missing_run():
    response = client.get("/runs/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Research run not found"