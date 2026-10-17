
from urllib.parse import urlsplit, urlunsplit

from backend.app.services.llm import generate_answer
from backend.app.services.search import web_search


def normalize_source_url(value: str) -> tuple[str, str] | None:
    """Return a display URL and deduplication key for valid HTTP(S) URLs."""
    if not isinstance(value, str) or not value.strip():
        return None

    try:
        parsed = urlsplit(value.strip())

        if parsed.scheme.lower() not in {"http", "https"}:
            return None

        if not parsed.hostname:
            return None

        # Reject URLs containing invalid ports.
        try:
            parsed.port
        except ValueError:
            return None

        scheme = parsed.scheme.lower()
        hostname = parsed.hostname.lower()
        port = parsed.port

        # Remove default ports from the normalized URL.
        if port and not (
            (scheme == "http" and port == 80)
            or (scheme == "https" and port == 443)
        ):
            hostname = f"{hostname}:{port}"

        path = parsed.path.rstrip("/") or "/"

        normalized = urlunsplit(
            (scheme, hostname, path, parsed.query, "")
        )

        return normalized, normalized

    except (TypeError, ValueError):
        return None


def research(
    query: str,
    research_questions: list[str] | None = None,
) -> tuple[str, list[dict]]:
    questions = research_questions or [query]
    all_results = []

    for question in questions:
        results = web_search(question)
        all_results.extend(results)

    unique_results = []
    seen_urls = set()

    for result in all_results:
        normalized = normalize_source_url(result.get("url", ""))

        if normalized is None:
            continue

        display_url, deduplication_key = normalized

        if deduplication_key in seen_urls:
            continue

        seen_urls.add(deduplication_key)

        unique_results.append(
            {
                "title": result.get("title", "").strip(),
                "url": display_url,
                "snippet": result.get("snippet", "").strip(),
            }
        )

    context = "\n\n".join(
        [
            f"Title: {result['title']}\n"
            f"URL: {result['url']}\n"
            f"Snippet: {result['snippet']}"
            for result in unique_results
        ]
    )

    prompt = f"""
You are a research assistant.

User research question:
{query}

Research questions investigated:
{chr(10).join(f"- {question}" for question in questions)}

WEB SEARCH RESULTS:
{context}

Instructions:
1. Use the search results to answer the original question.
2. Synthesize information across the results.
3. Do not invent facts or sources.
4. Clearly explain the key findings.
5. Mention uncertainty when the available evidence is insufficient.
6. Do not include a separate Sources section because the API returns sources separately.

Provide a concise but useful research answer.
"""

    answer = generate_answer(prompt)
    return answer, unique_results
