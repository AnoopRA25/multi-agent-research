from backend.app.services.llm import generate_answer


def critique_report(
    query: str,
    analysis: str,
    report: str,
) -> str:
    prompt = f"""
You are a critical research-review agent.

Original research question:
{query}

Analyst findings:
{analysis}

Generated research report:
{report}

Review the report against the analyst findings.

Evaluate:

1. Factual support
   - Are the report's claims supported by the analyst findings?

2. Completeness
   - Does the report address the original research question adequately?

3. Unsupported claims
   - Identify claims that are not supported by the available evidence.

4. Contradictions
   - Identify contradictions or inconsistencies.

5. Clarity
   - Identify unclear, misleading, or poorly structured sections.

6. Limitations
   - Check whether important uncertainty or evidence gaps were preserved.

Return a structured critique containing:

VERDICT:
PASS or NEEDS_REVISION

ISSUES:
List each important issue clearly.

STRENGTHS:
List the strongest aspects of the report.

RECOMMENDATIONS:
Give specific recommendations for improving the report.

Do not invent facts.
Base the critique only on the information provided above.
"""

    return generate_answer(prompt).text