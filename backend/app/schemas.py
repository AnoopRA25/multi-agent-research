from typing import Literal

from pydantic import BaseModel, Field


RunStatus = Literal[
    "queued",
    "running",
    "completed",
    "failed",
]


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Research question from the user",
    )


class Source(BaseModel):
    title: str
    url: str
    snippet: str


class JobResponse(BaseModel):
    run_id: int
    status: RunStatus


class QueryResponse(BaseModel):
    run_id: int
    answer: str
    sources: list[Source] = []
    critique: str
    latency_ms: float