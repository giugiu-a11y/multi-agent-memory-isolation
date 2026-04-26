from __future__ import annotations

import json
import os
import time

from agent_memory_isolation.cli import main
from agent_memory_isolation.store import AgentMemoryStore


def test_init_creates_storage(tmp_path) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0

    store = AgentMemoryStore(tmp_path)
    assert store.policy_path.exists()
    assert store.shared_memory_path.exists()
    assert (store.base / "templates" / "codex.md").exists()


def test_init_output_does_not_expose_absolute_root(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0

    output = capsys.readouterr().out
    assert "Multi-Agent Memory Isolation initialized at .agent-memory" in output
    assert str(tmp_path) not in output


def test_agent_notes_are_private_and_excluded_from_default_handoff(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "note",
                "--agent",
                "codex",
                "--kind",
                "observation",
                "--text",
                "Draft only",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--kind",
                "decision",
                "--text",
                "Use isolated draft notes",
                "--evidence",
                "policy check",
            ]
        )
        == 0
    )
    assert main(["--root", str(tmp_path), "handoff", "--agent", "openclaw"]) == 0

    output = capsys.readouterr().out
    assert "Use isolated draft notes" in output
    assert "Draft only" not in output


def test_handoff_can_include_current_agent_notes(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "note",
                "--agent",
                "codex",
                "--text",
                "Private current-agent hint",
            ]
        )
        == 0
    )
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "handoff",
                "--agent",
                "codex",
                "--include-agent-notes",
            ]
        )
        == 0
    )

    assert "Private current-agent hint" in capsys.readouterr().out


def test_handoff_output_path_is_relative_when_under_root(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    capsys.readouterr()

    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "handoff",
                "--agent",
                "codex",
                "--output",
                str(tmp_path / "handoff.md"),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "handoff written: handoff.md" in output
    assert str(tmp_path) not in output


def test_schema_output_path_is_relative_when_under_root(tmp_path, capsys) -> None:
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "schema",
                "--kind",
                "shared-memory",
                "--output",
                str(tmp_path / "schema.json"),
            ]
        )
        == 0
    )

    output = capsys.readouterr().out
    assert "schema written: schema.json" in output
    assert str(tmp_path) not in output


def test_promote_requires_evidence_for_non_question(tmp_path) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--kind",
                "fact",
                "--text",
                "Evidence-free fact",
            ]
        )
        == 2
    )


def test_open_question_may_be_promoted_without_evidence(tmp_path) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--kind",
                "open_question",
                "--text",
                "Which reviewer should own this?",
            ]
        )
        == 0
    )


def test_check_fails_for_shared_record_without_evidence(tmp_path) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    store = AgentMemoryStore(tmp_path)
    store.append_jsonl(
        store.shared_memory_path,
        {
            "id": "bad",
            "schema_version": 1,
            "kind": "fact",
            "agent": "codex",
            "visibility": "shared",
            "status": "promoted",
            "text": "Bad record",
            "evidence": [],
            "created_at": "2026-04-21T00:00:00Z",
        },
    )

    assert main(["--root", str(tmp_path), "check"]) == 1


def test_status_json(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    capsys.readouterr()
    assert main(["--root", str(tmp_path), "status", "--format", "json"]) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["shared_records"] == 0
    assert payload["root"] == "."
    assert payload["context_dir"] == ".agent-memory"
    assert str(tmp_path) not in output


def test_doctor_json(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    capsys.readouterr()
    assert main(["--root", str(tmp_path), "doctor", "--format", "json"]) == 0

    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["ok"] is True
    assert payload["shared_records"] == 0
    assert str(tmp_path) not in output


def test_doctor_errors_do_not_expose_absolute_root(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    store = AgentMemoryStore(tmp_path)
    notes_path = store.agent_notes_path("codex")
    notes_path.parent.mkdir(parents=True, exist_ok=True)
    notes_path.write_text("{not-json}\n", encoding="utf-8")
    capsys.readouterr()

    assert main(["--root", str(tmp_path), "doctor", "--format", "json"]) == 1
    output = capsys.readouterr().out
    payload = json.loads(output)
    assert payload["ok"] is False
    assert str(tmp_path) not in output
    assert ".agent-memory/agents/codex/notes.jsonl:1: invalid JSONL record" in payload["errors"][0]


def test_note_error_does_not_expose_absolute_root_before_init(tmp_path, capsys) -> None:
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "note",
                "--agent",
                "codex",
                "--text",
                "Draft without init",
            ]
        )
        == 2
    )

    error_output = capsys.readouterr().err
    assert (
        "Multi-Agent Memory Isolation is not initialized in this repository. "
        "Run: agent-memory-isolation init" in error_output
    )
    assert str(tmp_path) not in error_output


def test_promote_from_note_reuses_note_text_and_evidence(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    capsys.readouterr()
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "note",
                "--agent",
                "codex",
                "--kind",
                "decision",
                "--text",
                "Keep memory evidence-gated",
                "--evidence",
                "test evidence",
                "--format",
                "json",
            ]
        )
        == 0
    )
    note = json.loads(capsys.readouterr().out)

    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--from-note",
                note["id"],
                "--format",
                "json",
            ]
        )
        == 0
    )

    promoted = json.loads(capsys.readouterr().out)
    assert promoted["kind"] == "decision"
    assert promoted["text"] == "Keep memory evidence-gated"
    assert promoted["evidence"] == ["test evidence"]
    assert promoted["source_note"] == note["id"]


def test_schema_command_outputs_json(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "schema", "--kind", "shared-memory"]) == 0

    schema = json.loads(capsys.readouterr().out)
    assert schema["title"] == "Multi-Agent Memory Isolation Shared Memory Record"


def test_doctor_warns_when_shared_memory_has_no_handoff(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--kind",
                "fact",
                "--text",
                "Shared fact",
                "--evidence",
                "test evidence",
            ]
        )
        == 0
    )
    capsys.readouterr()

    assert main(["--root", str(tmp_path), "doctor", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert "handoff missing" in payload["warnings"][0]


def test_doctor_warns_when_handoff_is_stale(tmp_path, capsys) -> None:
    assert main(["--root", str(tmp_path), "init"]) == 0
    assert (
        main(
            [
                "--root",
                str(tmp_path),
                "promote",
                "--agent",
                "codex",
                "--kind",
                "fact",
                "--text",
                "Shared fact",
                "--evidence",
                "test evidence",
            ]
        )
        == 0
    )
    assert main(["--root", str(tmp_path), "handoff", "--agent", "codex"]) == 0

    store = AgentMemoryStore(tmp_path)
    old = time.time() - 120
    os.utime(store.handoff_path, (old, old))
    capsys.readouterr()

    assert main(["--root", str(tmp_path), "doctor", "--format", "json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert any("handoff is older" in warning for warning in payload["warnings"])
