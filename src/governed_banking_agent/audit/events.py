from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class AuditEvent(BaseModel):
    trace_id: str
    event_type: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model_version: str
    prompt_version: str
    index_version: str
    details: dict[str, Any] = Field(default_factory=dict)

