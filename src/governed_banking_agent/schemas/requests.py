from pydantic import BaseModel, Field, field_validator

from governed_banking_agent.schemas.enums import UserRole


class AgentQuery(BaseModel):
    query: str = Field(min_length=3, max_length=4_000)
    user_role: UserRole

    @field_validator("query")
    @classmethod
    def query_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("query must not be blank")
        return value
