from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from agent_memory_isolation.models import NOTE_KINDS, SHARED_KINDS, ValidationResult
from agent_memory_isolation.store import AgentMemoryStore

SECRETISH_PATTERNS = [
    re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?[^'\"\s]{8,}"),
    re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    re.compile(r"/(?:Users|home)/[^/\s]+"),
]


def validate_store(store: AgentMemoryStore) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    required_paths = [
        store.policy_path,
        store.shared_memory_path,
        store.base / "agents",
        store.base / "handoffs",
        store.base / "templates",
    ]
    for path in required_paths:
        if not path.exists():
            errors.append(f"missing required path: {relative(path, store.root)}")

    try:
        policy = store.read_policy()
    except Exception as exc:
        errors.append(f"policy unreadable: {safe_error_message(exc, store.root)}")
        policy = {}

    if policy.get("agent_notes_are_private") is not True:
        errors.append("policy must keep agent_notes_are_private=true")
    if policy.get("shared_memory_requires_evidence") is not True:
        errors.append("policy must keep shared_memory_requires_evidence=true")

    try:
        shared = store.read_shared_memory()
    except Exception as exc:
        errors.append(safe_error_message(exc, store.root))
        shared = []

    seen_ids: set[str] = set()
    for index, record in enumerate(shared, start=1):
        validate_shared_record(record, index, errors, warnings)
        record_id = str(record.get("id", ""))
        if record_id in seen_ids:
            warnings.append(f"duplicate shared memory id: {record_id}")
        seen_ids.add(record_id)
        scan_public_record(record, f"shared record {index}", warnings)

    validate_handoff_freshness(store, shared, warnings)

    agents_dir = store.base / "agents"
    if agents_dir.exists():
        for notes_file in agents_dir.glob("*/notes.jsonl"):
            notes_label = relative(notes_file, store.root)
            try:
                notes = store.read_jsonl(notes_file)
            except Exception as exc:
                errors.append(safe_error_message(exc, store.root))
                continue
            for index, record in enumerate(notes, start=1):
                validate_note_record(record, notes_label, index, errors, warnings)
                scan_public_record(record, f"{notes_label}:{index}", warnings)

    return ValidationResult(errors=errors, warnings=warnings)


def validate_handoff_freshness(
    store: AgentMemoryStore,
    shared: list[dict[str, Any]],
    warnings: list[str],
) -> None:
    if not shared:
        return
    if not store.handoff_path.exists():
        warnings.append(
            "handoff missing; run agent-memory-isolation handoff before agent continuation"
        )
        return
    if store.shared_memory_path.stat().st_mtime > store.handoff_path.stat().st_mtime:
        warnings.append(
            "handoff is older than shared memory; regenerate it before agent continuation"
        )


def validate_shared_record(
    record: dict[str, Any], index: int, errors: list[str], warnings: list[str]
) -> None:
    for field in ["id", "kind", "agent", "visibility", "status", "text", "evidence", "created_at"]:
        if field not in record:
            errors.append(f"shared record {index} missing field: {field}")
    kind = record.get("kind")
    if kind not in SHARED_KINDS:
        errors.append(f"shared record {index} has invalid kind: {kind}")
    if record.get("visibility") != "shared":
        errors.append(f"shared record {index} must have visibility=shared")
    if record.get("status") not in {"promoted", "canonical"}:
        errors.append(f"shared record {index} must be promoted or canonical")
    evidence = record.get("evidence")
    if kind != "open_question" and not evidence:
        errors.append(f"shared record {index} requires evidence")
    if kind == "open_question" and not evidence:
        warnings.append(f"shared open_question {index} has no evidence; acceptable but weaker")


def validate_note_record(
    record: dict[str, Any],
    notes_label: str,
    index: int,
    errors: list[str],
    warnings: list[str],
) -> None:
    for field in ["id", "kind", "agent", "visibility", "status", "text", "created_at"]:
        if field not in record:
            errors.append(f"{notes_label}:{index} missing field: {field}")
    kind = record.get("kind")
    if kind not in NOTE_KINDS:
        errors.append(f"{notes_label}:{index} has invalid note kind: {kind}")
    if record.get("visibility") != "agent_private":
        errors.append(f"{notes_label}:{index} must have visibility=agent_private")
    if record.get("status") != "draft":
        errors.append(f"{notes_label}:{index} must have status=draft")
    if record.get("evidence") is None:
        warnings.append(f"{notes_label}:{index} has no evidence field")


def scan_public_record(record: dict[str, Any], label: str, warnings: list[str]) -> None:
    content = " ".join(
        str(record.get(field, "")) for field in ["text", "evidence", "agent", "source_note"]
    )
    for pattern in SECRETISH_PATTERNS:
        if pattern.search(content):
            warnings.append(f"{label} contains sensitive-looking text")
            return


def relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def safe_error_message(exc: Exception, root: Path) -> str:
    message = str(exc)
    root_text = str(root)
    return message.replace(f"{root_text}/", "").replace(root_text, ".")
