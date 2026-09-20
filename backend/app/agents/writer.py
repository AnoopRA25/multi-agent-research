from backend.app.services.llm import generate_answer


def write_report(
    query: str,
    analysis: str,
) -> str:
    prompt = f"""
You are a professional research report writer.

Original research question:
{query}

Analyst findings:
{analysis}

Write a clear, well-structured research report based ONLY on the
analyst findings provided above.

Use this structure:

# Research Report

## Executive Summary
Give a concise summary of the main findings.

## Key Findings
Explain the most important findings in detail.

## Evidence and Analysis
Explain what the evidence indicates and how the findings relate
to the research question.

## Gaps and Limitations
Clearly describe missing information, uncertainty, and limitations.

## Conclusion
Provide a concise conclusion based only on the available evidence.

Rules:
1. Do not invent facts.
2. Do not introduce information that is not present in the analyst findings.
3. Preserve important uncertainty and limitations.
4. Use clear professional language.
5. Do not add a Sources section because sources are returned separately.
"""

    return generate_answer(prompt)