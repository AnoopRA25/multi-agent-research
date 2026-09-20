from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=3,
        description="Research question from the user",
    )


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []
    latency_ms: float