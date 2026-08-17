from typing import Any

from pydantic import BaseModel, Field

from governed_banking_agent.schemas.enums import ToolStatus


class ToolCall(BaseModel):
    name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    name: str
    status: ToolStatus
    output: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    latency_ms: float | None = Field(default=None, ge=0)

