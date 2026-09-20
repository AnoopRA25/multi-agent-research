import time

from fastapi import APIRouter, HTTPException

from backend.app.agents.analyst import analyze
from backend.app.agents.critic import critique_report
from backend.app.agents.planner import create_plan
from backend.app.agents.researcher import research
from backend.app.agents.writer import write_report
from backend.app.schemas import QueryRequest, QueryResponse

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    start_time = time.perf_counter()

    try:
        # 1. Create research plan
        research_questions = create_plan(request.query)

        # 2. Collect web evidence
        _, sources = research(
            request.query,
            research_questions,
        )

        # 3. Analyze collected evidence
        analysis = analyze(
            request.query,
            research_questions,
            sources,
        )

        # 4. Write research report
        report = write_report(
            request.query,
            analysis,
        )

        # 5. Critique the generated report
        critique = critique_report(
            request.query,
            analysis,
            report,
        )

    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    # 6. Calculate total latency
    latency_ms = (time.perf_counter() - start_time) * 1000

    return QueryResponse(
        answer=report,
        sources=sources,
        critique=critique,
        latency_ms=round(latency_ms, 2),
    )