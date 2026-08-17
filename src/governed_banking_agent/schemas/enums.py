from enum import StrEnum


class Decision(StrEnum):
    ANSWER = "answer"
    ABSTAIN = "abstain"
    ESCALATE = "escalate"
    REFUSE = "refuse"


class UserRole(StrEnum):
    ANALYST = "analyst"
    REVIEWER = "reviewer"
    VALIDATOR = "validator"


class ToolStatus(StrEnum):
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    DENIED = "denied"

