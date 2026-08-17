import pytest

from governed_banking_agent.workflow.controls import WorkflowControlError, WorkflowControls


def test_step_limit_blocks_additional_work() -> None:
    controls = WorkflowControls(max_steps=5)
    with pytest.raises(WorkflowControlError, match="Maximum workflow steps"):
        controls.assert_can_continue(current_steps=5)


def test_tool_allowlist_blocks_unknown_tool() -> None:
    with pytest.raises(WorkflowControlError, match="not allowed"):
        WorkflowControls.assert_tool_allowed("customer_database", {"search_policy"})
