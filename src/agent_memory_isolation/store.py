from __future__ import annotations

import json
import re
from importlib import resources
from pathlib import Path
from typing import Any

from agent_memory_isolation.models import NOTE_KINDS, SHARED_KINDS, now_utc, record_id

CONTEXT_DIR = ".agent-memory"
POLICY_FILE = "policy.json"
SHARED_MEMORY_FILE = "shared/memory.jsonl"
HANDOFF_FILE = "handoffs/latest.md"
NOTE_KIND_TO_SHARED_KIND = {
    "observation": "fact",
    "decision": "decision",
    "risk": "risk",
    "question": "open_question",
}


DEFAULT_POLICY: dict[str, Any] = {
    "schema_version": 1,
    "agent_notes_are_private": True,
    "shared_memory_requires_evidence": True,
    "handoff_includes_only_shared_memory_by_default": True,
    "allowed_shared_kinds": sorted(SHARED_KINDS),
    "allowed_note_kinds": sorted(NOTE_KINDS),
}


def safe_agent_name(agent: str) -> str:
    value = agent.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = value.strip(".-_")
    if not value:
        raise ValueError("agent name cannot be empty")
    if value in {".", ".."}:
        raise ValueError("invalid agent name")
    return value


class AgentMemoryStore:
    def __init__(self, root: str | Path = ".") -> None:
        self.root = Path(root).resolve()
        self.base = self.root / CONTEXT_DIR

    @property
    def policy_path(self) -> Path:
        return self.base / POLICY_FILE

    @property
    def shared_memory_path(self) -> Path:
        return self.base / SHARED_MEMORY_FILE

    @property
    def handoff_path(self) -> Path:
        return self.base / HANDOFF_FILE

    def agent_dir(self, agent: str) -> Path:
        return self.base / "agents" / safe_agent_name(agent)

    def agent_notes_path(self, agent: str) -> Path:
        return self.agent_dir(agent) / "notes.jsonl"

    def init(self, force: bool = False) -> list[Path]:
        created: list[Path] = []
        for directory in [
            self.base,
            self.base / "agents",
            self.base / "shared",
            self.base / "handoffs",
            self.base / "templates",
        ]:
            directory.mkdir(parents=True, exist_ok=True)
            created.append(directory)

        if force or not self.policy_path.exists():
            self.write_json(self.policy_path, DEFAULT_POLICY)
            created.append(self.policy_path)

        if not self.shared_memory_path.exists():
            self.shared_memory_path.write_text("", encoding="utf-8")
            created.append(self.shared_memory_path)

        for keep in [self.base / "agents" / ".gitkeep", self.base / "handoffs" / ".gitkeep"]:
            if not keep.exists():
                keep.write_text("", encoding="utf-8")
                created.append(keep)

        self.copy_templates(force=force)
        return created

    def copy_templates(self, force: bool = False) -> None:
        template_root = resources.files("agent_memory_isolation").joinpath("templates")
        for resource in template_root.iterdir():
            if not resource.name.endswith(".md"):
                continue
            destination = self.base / "templates" / resource.name
            if destination.exists() and not force:
                continue
            destination.write_text(resource.read_text(encoding="utf-8"), encoding="utf-8")

    def ensure_initialized(self) -> None:
        if not self.policy_path.exists():
            raise FileNotFoundError(
                "Multi-Agent Memory Isolation is not initialized in this repository. "
                "Run: agent-memory-isolation init"
            )

    def read_policy(self) -> dict[str, Any]:
        self.ensure_initialized()
        return self.read_json(self.policy_path)

    def create_note(
        self,
        *,
        agent: str,
        kind: str,
        text: str,
        evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        self.ensure_initialized()
        if kind not in NOTE_KINDS:
            raise ValueError(f"invalid note kind: {kind}")
        created_at = now_utc()
        record = {
            "id": record_id(kind, agent, text, created_at),
            "schema_version": 1,
            "kind": kind,
            "agent": safe_agent_name(agent),
            "visibility": "agent_private",
            "status": "draft",
            "text": text,
            "evidence": evidence or [],
            "created_at": created_at,
        }
        path = self.agent_notes_path(agent)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.append_jsonl(path, record)
        return record

    def promote_memory(
        self,
        *,
        agent: str,
        kind: str,
        text: str,
        evidence: list[str],
        source_note: str | None = None,
    ) -> dict[str, Any]:
        self.ensure_initialized()
        if kind not in SHARED_KINDS:
            raise ValueError(f"invalid shared memory kind: {kind}")
        if kind != "open_question" and not evidence:
            raise ValueError("shared memory requires evidence")
        created_at = now_utc()
        record = {
            "id": record_id(kind, agent, text, created_at),
            "schema_version": 1,
            "kind": kind,
            "agent": safe_agent_name(agent),
            "visibility": "shared",
            "status": "promoted",
            "text": text,
            "evidence": evidence,
            "source_note": source_note,
            "created_at": created_at,
        }
        self.append_jsonl(self.shared_memory_path, record)
        return record

    def promote_note(
        self,
        *,
        agent: str,
        note_id: str,
        kind: str | None = None,
        evidence: list[str] | None = None,
    ) -> dict[str, Any]:
        note = self.find_agent_note(agent, note_id)
        shared_kind = kind or NOTE_KIND_TO_SHARED_KIND[str(note["kind"])]
        note_evidence = evidence if evidence is not None else list(note.get("evidence", []))
        return self.promote_memory(
            agent=agent,
            kind=shared_kind,
            text=str(note["text"]),
            evidence=note_evidence,
            source_note=str(note["id"]),
        )

    def read_shared_memory(self) -> list[dict[str, Any]]:
        self.ensure_initialized()
        return self.read_jsonl(self.shared_memory_path)

    def read_agent_notes(self, agent: str) -> list[dict[str, Any]]:
        self.ensure_initialized()
        return self.read_jsonl(self.agent_notes_path(agent))

    def find_agent_note(self, agent: str, note_id: str) -> dict[str, Any]:
        for note in self.read_agent_notes(agent):
            if note.get("id") == note_id:
                return note
        raise ValueError(f"agent note not found: {note_id}")

    @staticmethod
    def write_json(path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    @staticmethod
    def read_json(path: Path) -> dict[str, Any]:
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def append_jsonl(path: Path, record: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True) + "\n")

    @staticmethod
    def read_jsonl(path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        records: list[dict[str, Any]] = []
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL record") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"{path}:{line_number}: JSONL record must be an object")
            records.append(payload)
        return records
