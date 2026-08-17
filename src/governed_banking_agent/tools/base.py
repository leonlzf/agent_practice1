from typing import Protocol

from pydantic import BaseModel

from governed_banking_agent.schemas.tools import ToolResult


class GovernedTool(Protocol):
    name: str
    input_model: type[BaseModel]

    def invoke(self, arguments: dict[str, object]) -> ToolResult: ...

