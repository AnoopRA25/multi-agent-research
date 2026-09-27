from backend.app.api.routes import run_research_job
from backend.app.database.database import initialize_database
from backend.app.database.research_repository import (
    create_research_run,
    get_research_run,
)


initialize_database()


def test_successful_job_lifecycle(monkeypatch):
    run_id = create_research_run(
        query="Test research question",
        report="",
        critique="",
        latency_ms=0,
        status="queued",
    )

    class FakeGraph:
        def invoke(self, state):
            return {
                "report": "# Test Research Report",
                "critique": "VERDICT: PASS",
            }

    monkeypatch.setattr(
        "backend.app.api.routes.research_graph",
        FakeGraph(),
    )

    run_research_job(
        run_id,
        "Test research question",
    )

    run = get_research_run(run_id)

    assert run["status"] == "completed"
    assert run["report"] == "# Test Research Report"
    assert run["critique"] == "VERDICT: PASS"


def test_failed_job_lifecycle():
    run_id = create_research_run(
        query="__TEST_FAILURE__",
        report="",
        critique="",
        latency_ms=0,
        status="queued",
    )

    run_research_job(
        run_id,
        "__TEST_FAILURE__",
    )

    run = get_research_run(run_id)

    assert run["status"] == "failed"
    assert run["critique"] == "Intentional test failure"