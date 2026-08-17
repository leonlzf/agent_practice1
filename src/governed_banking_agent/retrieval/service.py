from datetime import date
from typing import Protocol

from governed_banking_agent.retrieval.models import RetrievedChunk


class PolicyRetriever(Protocol):
    def search(
        self,
        query: str,
        *,
        effective_on: date,
        jurisdiction: str | None = None,
        business_unit: str | None = None,
        top_k: int = 5,
    ) -> list[RetrievedChunk]: ...

