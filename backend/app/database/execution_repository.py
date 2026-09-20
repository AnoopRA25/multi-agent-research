from backend.app.database.database import get_connection


def create_agent_execution(
    run_id: int,
    agent_name: str,
    status: str,
    latency_ms: float | None = None,
) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO agent_executions
            (run_id, agent_name, status, latency_ms)
            VALUES (?, ?, ?, ?)
            """,
            (run_id, agent_name, status, latency_ms),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()


def list_agent_executions(run_id: int) -> list[dict]:
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                run_id,
                agent_name,
                status,
                latency_ms,
                created_at
            FROM agent_executions
            WHERE run_id = ?
            ORDER BY id ASC
            """,
            (run_id,),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()