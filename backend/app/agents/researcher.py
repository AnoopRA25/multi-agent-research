from backend.app.services.llm import generate_answer
from backend.app.services.search import web_search


def research(query: str, research_questions: list[str] | None = None) -> tuple[str, list[dict]]:
    questions = research_questions or [query]

    all_results = []

    for question in questions:
        results = web_search(question)
        all_results.extend(results)

    # Remove duplicate URLs
    unique_results = []
    seen_urls = set()

    for result in all_results:
        url = result["url"]

        if url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(result)

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

    sources = [
        {
            "title": result["title"],
            "url": result["url"],
            "snippet": result["snippet"],
        }
        for result in unique_results
    ]

    return answer, sources