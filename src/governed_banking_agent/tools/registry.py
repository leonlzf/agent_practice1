from governed_banking_agent.schemas.tools import ToolResult
from governed_banking_agent.tools.base import GovernedTool
from governed_banking_agent.workflow.controls import WorkflowControls


class ToolRegistry:
    def __init__(self, tools: list[GovernedTool] | None = None) -> None:
        tools = tools or []
        self._tools = {tool.name: tool for tool in tools}

    @property
    def names(self) -> set[str]:
        return set(self._tools)

    def invoke(
        self,
        tool_name: str,
        arguments: dict[str, object],
        allowed_tools: set[str],
    ) -> ToolResult:
        WorkflowControls.assert_tool_allowed(tool_name, allowed_tools)
        tool = self._tools.get(tool_name)
        if tool is None:
            raise KeyError(f"Unknown tool: {tool_name}")
        validated = tool.input_model.model_validate(arguments)
        return tool.invoke(validated.model_dump())
