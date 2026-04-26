from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any

SHARED_KINDS = {"fact", "decision", "risk", "open_question"}
NOTE_KINDS = {"observation", "decision", "risk", "question"}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def record_id(kind: str, agent: str, text: str, created_at: str) -> str:
    digest = sha256(f"{kind}\0{agent}\0{text}\0{created_at}".encode()).hexdigest()
    return digest[:16]


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def ok(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "errors": self.errors,
            "warnings": self.warnings,
        }
