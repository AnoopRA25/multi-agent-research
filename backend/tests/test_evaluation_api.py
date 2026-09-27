from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.database.database import initialize_database
from backend.app.database.research_repository import create_research_run


client = TestClient(app)


def test_evaluate_missing_run():
    response = client.post("/evaluate/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Research run not found"


def test_evaluate_run_without_report():
    initialize_database()

    run_id = create_research_run(
        query="Test research question",
        report="",
        critique="",
        latency_ms=0,
        status="running",
    )

    response = client.post(f"/evaluate/{run_id}")

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "Research run does not contain a report"
    )


def test_get_missing_evaluation():
    response = client.get("/evaluate/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Research run not found"

def test_evaluate_completed_run():
    initialize_database()

    run_id = create_research_run(
        query="What are the major applications of generative AI?",
        report="""
        # Research Report

        ## Executive Summary
        Generative AI has major applications across software development,
        content generation, education, healthcare, and business.

        ## Key Findings
        Key findings include content generation and software development.

        ## Evidence and Analysis
        Research and evidence indicate that these applications are expanding.

        ## Gaps and Limitations
        Available evidence has limitations and uncertainty.

        ## Conclusion
        Generative AI has applications across multiple domains.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    response = client.post(f"/evaluate/{run_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == run_id
    assert 0 <= data["relevance_score"] <= 10
    assert 0 <= data["completeness_score"] <= 10
    assert 0 <= data["evidence_score"] <= 10
    assert 0 <= data["factuality_score"] <= 10
    assert 0 <= data["overall_score"] <= 10
    assert data["feedback"]


def test_get_existing_evaluation():
    initialize_database()

    run_id = create_research_run(
        query="What are the major applications of generative AI?",
        report="""
        # Research Report

        ## Key Findings
        Research evidence supports the findings.

        ## Limitations
        There are limitations and uncertainty.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    create_response = client.post(f"/evaluate/{run_id}")

    assert create_response.status_code == 200

    response = client.get(f"/evaluate/{run_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == run_id
    assert "overall_score" in data

def test_evaluate_uses_matching_dataset_case():
    initialize_database()

    run_id = create_research_run(
        query="What are the major applications of generative AI?",
        report="""
        Generative AI has major application areas including
        software development, education, and content generation.

        Research and evidence indicate that these use cases are
        expanding, although available evidence has limitations
        and uncertainty.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    response = client.post(f"/evaluate/{run_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["run_id"] == run_id
    assert data["completeness_score"] > 0
    assert data["overall_score"] > 0

def test_evaluate_unknown_question():
    initialize_database()

    run_id = create_research_run(
        query="This question does not exist in the evaluation dataset",
        report="""
        This is a completed research report with some evidence.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    response = client.post(f"/evaluate/{run_id}")

    assert response.status_code == 400
    assert response.json()["detail"] == (
        "No evaluation criteria found for this research question"
    )

def test_evaluation_summary():
    response = client.get("/evaluate/summary")

    assert response.status_code == 200

    data = response.json()

    assert "total_evaluations" in data
    assert "avg_relevance" in data
    assert "avg_completeness" in data
    assert "avg_evidence" in data
    assert "avg_factuality" in data
    assert "avg_overall" in data