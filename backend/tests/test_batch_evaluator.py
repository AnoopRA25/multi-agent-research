from backend.app.database.database import initialize_database
from backend.app.database.research_repository import create_research_run
from backend.app.evaluation.batch_evaluator import evaluate_runs


def test_batch_evaluation_completed_run():
    initialize_database()

    run_id = create_research_run(
        query="What are the major applications of generative AI?",
        report="""
        Generative AI has major applications in software development,
        education, content generation, and healthcare.

        Research and evidence support these applications.
        Available evidence has limitations and uncertainty.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    results = evaluate_runs([run_id])

    assert len(results) == 1
    assert results[0]["run_id"] == run_id
    assert results[0]["status"] == "evaluated"
    assert results[0]["overall_score"] > 0
    assert "evaluation_id" in results[0]


def test_batch_evaluation_missing_run():
    initialize_database()

    results = evaluate_runs([999999])

    assert len(results) == 1
    assert results[0]["run_id"] == 999999
    assert results[0]["status"] == "not_found"


def test_batch_evaluation_unknown_question():
    initialize_database()

    run_id = create_research_run(
        query="This question does not exist in the evaluation dataset",
        report="""
        This is a completed report containing evidence.
        """,
        critique="",
        latency_ms=100,
        status="completed",
    )

    results = evaluate_runs([run_id])

    assert len(results) == 1
    assert results[0]["run_id"] == run_id
    assert results[0]["status"] == "no_matching_dataset_case"


def test_batch_evaluation_no_report():
    initialize_database()

    run_id = create_research_run(
        query="What are the major applications of generative AI?",
        report="",
        critique="",
        latency_ms=100,
        status="completed",
    )

    results = evaluate_runs([run_id])

    assert len(results) == 1
    assert results[0]["run_id"] == run_id
    assert results[0]["status"] == "no_report"