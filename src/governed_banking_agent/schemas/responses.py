from pydantic import BaseModel, Field

from governed_banking_agent.schemas.enums import Decision


class Citation(BaseModel):
    document_id: str
    section: str
    version: str
    evidence: str


class AgentResponse(BaseModel):
    answer: str
    citations: list[Citation] = Field(default_factory=list)
    decision: Decision
    limitations: list[str] = Field(default_factory=list)
    trace_id: str


class HealthResponse(BaseModel):
    status: str

