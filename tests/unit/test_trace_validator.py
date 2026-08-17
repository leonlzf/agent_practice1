from governed_banking_agent.evaluation.trace_validator import TraceStep, validate_trace


def test_trace_validator_detects_event_after_terminal_state() -> None:
    steps = [
        TraceStep(step_number=1, event_type="answer", terminal=True),
        TraceStep(step_number=2, event_type="tool_call", tool_name="search_policy"),
    ]
    errors = validate_trace(steps, max_steps=5, allowed_tools={"search_policy"})
    assert "event found after terminal step: 2" in errors

