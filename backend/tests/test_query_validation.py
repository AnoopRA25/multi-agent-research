from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_query_too_short():
    response = client.post("/query", json={"query": "AI"})

    assert response.status_code == 422


def test_query_missing():
    response = client.post("/query", json={})

    assert response.status_code == 422


def test_query_valid_format():
    from backend.app.schemas import QueryRequest

    request = QueryRequest(
        query="What are the applications of generative AI?"
    )

    assert request.query == "What are the applications of generative AI?"