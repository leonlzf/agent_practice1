from datetime import date

from pydantic import BaseModel, Field

from governed_banking_agent.schemas.enums import ToolStatus
from governed_banking_agent.schemas.tools import ToolResult


class PolicySearchInput(BaseModel):
    query: str = Field(min_length=3, max_length=2_000)
    jurisdiction: str | None = None
    business_unit: str | None = None
    effective_on: date | None = None
    top_k: int = Field(default=5, ge=1, le=20)


class PolicySearchTool:
    name = "search_policy"
    input_model = PolicySearchInput

    def invoke(self, arguments: dict[str, object]) -> ToolResult:
        return ToolResult(
            name=self.name,
            status=ToolStatus.ERROR,
            error="Policy index is not configured.",
        )

