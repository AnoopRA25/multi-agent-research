from backend.app.database.database import get_connection


def create_research_run(
    query: str,
    report: str,
    critique: str,
    latency_ms: float,
    status: str = "completed",
) -> int:
    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO research_runs
            (query, report, critique, latency_ms, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                query,
                report,
                critique,
                latency_ms,
                status,
            ),
        )

        connection.commit()

        return cursor.lastrowid

    finally:
        connection.close()

def update_research_run(
    run_id: int,
    report: str,
    critique: str,
    latency_ms: float,
    status: str = "completed",
) -> None:
    connection = get_connection()

    try:
        connection.execute(
            """
            UPDATE research_runs
            SET
                report = ?,
                critique = ?,
                latency_ms = ?,
                status = ?
            WHERE id = ?
            """,
            (
                report,
                critique,
                latency_ms,
                status,
                run_id,
            ),
        )

        connection.commit()

    finally:
        connection.close()


def get_research_run(run_id: int) -> dict | None:
    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                id,
                query,
                report,
                critique,
                latency_ms,
                status,
                created_at
            FROM research_runs
            WHERE id = ?
            """,
            (run_id,),
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()


def list_research_runs(limit: int = 20) -> list[dict]:
    connection = get_connection()

    try:
        rows = connection.execute(
            """
            SELECT
                id,
                query,
                report,
                critique,
                latency_ms,
                status,
                created_at
            FROM research_runs
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

        return [dict(row) for row in rows]

    finally:
        connection.close()