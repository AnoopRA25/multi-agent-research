from typing import NamedTuple

from google import genai
from google.genai import errors

from backend.app.config import settings


client = genai.Client(api_key=settings.gemini_api_key)


_last_usage = {
    "input_tokens": 0,
    "output_tokens": 0,
}


def get_last_usage() -> tuple[int, int]:
    return (
        _last_usage["input_tokens"],
        _last_usage["output_tokens"],
    )


class LLMResult(NamedTuple):
    text: str
    input_tokens: int
    output_tokens: int


def generate_answer(prompt: str) -> LLMResult:
    try:
        response = client.models.generate_content(
            model=settings.llm_model,
            contents=prompt,
        )

        usage = response.usage_metadata

        _last_usage["input_tokens"] = usage.prompt_token_count or 0
        _last_usage["output_tokens"] = usage.candidates_token_count or 0

        return LLMResult(
            text=response.text or "",
            input_tokens=usage.prompt_token_count or 0,
            output_tokens=usage.candidates_token_count or 0,
        )

    except errors.ClientError as exc:
        if exc.code == 429:
            raise RuntimeError(
                "Gemini API quota has been exceeded. "
                "Please wait for the quota to reset or check your Gemini API usage."
            ) from exc

        raise RuntimeError(
            f"Gemini API client request failed: {exc}"
        ) from exc

    except errors.ServerError as exc:
        if exc.code == 503:
            raise RuntimeError(
                "Gemini API is temporarily unavailable because the model "
                "is experiencing high demand. Please try again later."
            ) from exc

        raise RuntimeError(
            f"Gemini API server request failed: {exc}"
        ) from exc