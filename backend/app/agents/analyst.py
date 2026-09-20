from backend.app.services.llm import generate_answer


def analyze(
    query: str,
    research_questions: list[str],
    sources: list[dict],
) -> str:
    evidence = "\n\n".join(
        [
            f"Title: {source['title']}\n"
            f"URL: {source['url']}\n"
            f"Snippet: {source['snippet']}"
            for source in sources
        ]
    )

    prompt = f"""
You are an analytical research agent.

Original research question:
{query}

Research questions:
{chr(10).join(f"- {question}" for question in research_questions)}

Collected evidence:
{evidence}

Analyze the evidence.

Identify:
1. Key findings
2. Evidence supporting each finding
3. Contradictions or disagreements between sources
4. Important gaps or missing information
5. Uncertainty or limitations

Do not invent information.

Return a structured analytical summary that another agent can use to write the final report.
"""

    return generate_answer(prompt)