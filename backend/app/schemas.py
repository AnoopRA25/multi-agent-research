from pydantic import BaseModel, Field


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


class QueryResponse(BaseModel):
    run_id: int
    answer: str
    sources: list[Source] = []
    critique: str
    latency_ms: float