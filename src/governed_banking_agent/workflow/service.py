from uuid import uuid4

from governed_banking_agent.schemas.enums import Decision
from governed_banking_agent.schemas.requests import AgentQuery
from governed_banking_agent.schemas.responses import AgentResponse


class WorkflowService:
    """Application-facing workflow service.

    The safe scaffold escalates every request until retrieval, authorization,
    generation, and verification nodes have been implemented and validated.
    """

    def invoke(self, request: AgentQuery) -> AgentResponse:
        return AgentResponse(
            answer=(
                "The governed policy workflow is not implemented yet. "
                "This request requires human review."
            ),
            decision=Decision.ESCALATE,
            limitations=["Scaffold only: no policy retrieval or model call was executed."],
            trace_id=str(uuid4()),
        )
