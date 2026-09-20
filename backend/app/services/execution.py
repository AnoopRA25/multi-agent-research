import time

from backend.app.database.execution_repository import create_agent_execution


def track_agent_execution(
    run_id: int,
    agent_name: str,
    function,
    *args,
    **kwargs,
):
    start_time = time.perf_counter()

    try:
        result = function(*args, **kwargs)

        latency_ms = (time.perf_counter() - start_time) * 1000

        create_agent_execution(
            run_id=run_id,
            agent_name=agent_name,
            status="completed",
            latency_ms=round(latency_ms, 2),
        )

        return result

    except Exception:
        latency_ms = (time.perf_counter() - start_time) * 1000

        create_agent_execution(
            run_id=run_id,
            agent_name=agent_name,
            status="failed",
            latency_ms=round(latency_ms, 2),
        )

        raise