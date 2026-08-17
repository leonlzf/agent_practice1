from pydantic import BaseModel, Field


class TraceStep(BaseModel):
    step_number: int = Field(ge=1)
    event_type: str
    tool_name: str | None = None
    terminal: bool = False


def validate_trace(
    steps: list[TraceStep], *, max_steps: int, allowed_tools: set[str]
) -> list[str]:
    errors: list[str] = []
    if len(steps) > max_steps:
        errors.append(f"trace exceeds max steps: {len(steps)}/{max_steps}")

    terminal_seen = False
    for expected_number, step in enumerate(steps, start=1):
        if step.step_number != expected_number:
            errors.append(f"non-contiguous step number: expected {expected_number}")
        if terminal_seen:
            errors.append(f"event found after terminal step: {step.step_number}")
        if step.tool_name and step.tool_name not in allowed_tools:
            errors.append(f"forbidden tool at step {step.step_number}: {step.tool_name}")
        terminal_seen = terminal_seen or step.terminal
    return errors

