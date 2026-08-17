from fastapi.testclient import TestClient

from governed_banking_agent.api.app import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_safely_escalates_while_agent_is_unimplemented() -> None:
    response = client.post(
        "/v1/query",
        json={"query": "Which policy applies?", "user_role": "analyst"},
    )
    assert response.status_code == 200
    assert response.json()["decision"] == "escalate"
    assert response.json()["citations"] == []

