from __future__ import annotations

from collections import defaultdict
from pathlib import Path


def render_handoff(
    *,
    agent: str,
    task: str | None,
    shared_memory: list[dict[str, object]],
    agent_notes: list[dict[str, object]] | None = None,
) -> str:
    grouped: dict[str, list[dict[str, object]]] = defaultdict(list)
    for record in shared_memory:
        grouped[str(record.get("kind", "fact"))].append(record)

    lines = [
        "# Multi-Agent Memory Isolation Handoff",
        "",
        f"- Agent: `{agent}`",
        f"- Task: {task or 'Not specified'}",
        "",
        "## Shared Truth",
        "",
        "Only promoted records appear here.",
        "Agent-local draft notes from other agents are excluded.",
        "",
    ]

    sections = [
        ("decision", "Decisions"),
        ("fact", "Facts"),
        ("risk", "Risks"),
        ("open_question", "Open Questions"),
    ]
    for kind, title in sections:
        lines.append(f"### {title}")
        records = grouped.get(kind, [])
        if not records:
            lines.append("")
            lines.append("- None recorded.")
            lines.append("")
            continue
        for record in records:
            text = str(record.get("text", "")).strip()
            evidence = record.get("evidence", [])
            evidence_text = "; ".join(str(item) for item in evidence) if evidence else "none"
            lines.append(f"- {text}")
            lines.append(f"  Evidence: {evidence_text}")
        lines.append("")

    if agent_notes is not None:
        lines.extend(
            [
                "## Current Agent Private Notes",
                "",
                "These notes belong to the requesting agent only. They are not shared truth.",
                "",
            ]
        )
        if not agent_notes:
            lines.append("- None recorded.")
        for note in agent_notes:
            lines.append(f"- [{note.get('kind', 'note')}] {note.get('text', '')}")
        lines.append("")

    lines.extend(
        [
            "## Start Rule",
            "",
            "Use shared truth as context. Verify files and commands before acting.",
            "Promote new facts only with evidence.",
            "",
        ]
    )
    return "\n".join(lines)


def write_handoff(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
