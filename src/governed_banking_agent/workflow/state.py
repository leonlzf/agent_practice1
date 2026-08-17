from pydantic import BaseModel, Field

from governed_banking_agent.schemas.enums import Decision, UserRole
from governed_banking_agent.schemas.responses import Citation
from governed_banking_agent.schemas.tools import ToolCall, ToolResult


class AgentState(BaseModel):
    trace_id: str
    user_role: UserRole
    query: str
    intent: str | None = None
    step_count: int = Field(default=0, ge=0)
    tool_calls: list[ToolCall] = Field(default_factory=list)
    tool_results: list[ToolResult] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    draft_answer: str | None = None
    decision: Decision | None = None
    errors: list[str] = Field(default_factory=list)
