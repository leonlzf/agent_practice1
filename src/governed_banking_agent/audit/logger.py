import json
from pathlib import Path

from governed_banking_agent.audit.events import AuditEvent


class JsonlAuditLogger:
    """Append-only local logger for development with an explicit output path."""

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path

    def write(self, event: AuditEvent) -> None:
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        with self.output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event.model_dump(mode="json"), ensure_ascii=False) + "\n")

