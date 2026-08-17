from fastapi import APIRouter, status

from governed_banking_agent.schemas.requests import AgentQuery
from governed_banking_agent.schemas.responses import AgentResponse, HealthResponse
from governed_banking_agent.workflow.service import WorkflowService

router = APIRouter()
workflow_service = WorkflowService()


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/v1/query",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
)
def query_agent(request: AgentQuery) -> AgentResponse:
    return workflow_service.invoke(request)
