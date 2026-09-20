from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_get_run_executions():
    response = client.get("/runs/1/executions")

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == 1
    assert "executions" in data
    assert isinstance(data["executions"], list)


def test_get_run_executions_contains_planner():
    response = client.get("/runs/1/executions")

    assert response.status_code == 200

    executions = response.json()["executions"]

    assert any(
        execution["agent_name"] == "planner"
        for execution in executions
    )


def test_get_executions_for_missing_run():
    response = client.get("/runs/999999/executions")

    assert response.status_code == 404
    assert response.json()["detail"] == "Research run not found"