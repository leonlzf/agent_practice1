from dataclasses import dataclass


class WorkflowControlError(RuntimeError):
    """Raised when an agent workflow violates a deterministic control."""


@dataclass(frozen=True)
class WorkflowControls:
    max_steps: int = 5

    def assert_can_continue(self, current_steps: int) -> None:
        if current_steps >= self.max_steps:
            raise WorkflowControlError(
                f"Maximum workflow steps reached: {current_steps}/{self.max_steps}"
            )

    @staticmethod
    def assert_tool_allowed(tool_name: str, allowed_tools: set[str]) -> None:
        if tool_name not in allowed_tools:
            raise WorkflowControlError(f"Tool is not allowed: {tool_name}")
