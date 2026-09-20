from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_query_too_short():
    response = client.post(
        "/query",
        json={"query": "AI"},
    )

    assert response.status_code == 422


def test_query_missing():
    response = client.post(
        "/query",
        json={},
    )

    assert response.status_code == 422


def test_query_valid_format():
    response = client.post(
        "/query",
        json={
            "query": "What are the applications of generative AI?"
        },
    )

    # The request is structurally valid.
    # Gemini may currently return 503 because the free-tier quota is exhausted.
    assert response.status_code != 422