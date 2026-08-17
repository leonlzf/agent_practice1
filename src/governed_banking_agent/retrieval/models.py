from datetime import date

from pydantic import BaseModel, Field


class PolicyDocument(BaseModel):
    document_id: str
    title: str
    business_unit: str
    jurisdiction: str
    effective_date: date
    expiry_date: date | None = None
    version: str
    confidentiality_level: str
    supersedes_document_id: str | None = None
    policy_owner: str
    body: str = Field(min_length=1)


class RetrievedChunk(BaseModel):
    document_id: str
    section: str
    version: str
    text: str
    score: float

