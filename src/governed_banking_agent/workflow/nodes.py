from governed_banking_agent.workflow.state import AgentState


def classify_request(state: AgentState) -> AgentState:
    """Classify scope and risk before deterministic routing.

    This placeholder deliberately avoids an LLM call. Replace it with a tested
    classifier while preserving deterministic high-risk overrides.
    """
    state.intent = "not_implemented"
    return state
