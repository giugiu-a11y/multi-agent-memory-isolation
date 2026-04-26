from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence
from importlib import resources
from pathlib import Path

from agent_memory_isolation import __version__
from agent_memory_isolation.render import render_handoff, write_handoff
from agent_memory_isolation.store import AgentMemoryStore
from agent_memory_isolation.validation import validate_store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-memory-isolation",
        description="Memory layer for multi-agent AI systems with individual context isolation.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"agent-memory-isolation {__version__}",
    )
    parser.add_argument(
        "--root",
        default=".",
        help="Repository root. Defaults to current directory.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create .agent-memory storage and templates.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite policy and templates.")

    note_parser = subparsers.add_parser("note", help="Write an agent-private draft note.")
    note_parser.add_argument("--agent", required=True)
    note_parser.add_argument("--kind", default="observation")
    note_parser.add_argument("--text", required=True)
    note_parser.add_argument("--evidence", action="append", default=[])
    note_parser.add_argument("--format", choices=["text", "json"], default="text")

    promote_parser = subparsers.add_parser("promote", help="Promote evidence-backed memory.")
    promote_parser.add_argument("--agent", required=True)
    promote_parser.add_argument("--kind")
    promote_parser.add_argument("--text")
    promote_parser.add_argument("--evidence", action="append", default=[])
    promote_parser.add_argument("--from-note")
    promote_parser.add_argument("--source-note")
    promote_parser.add_argument("--format", choices=["text", "json"], default="text")

    handoff_parser = subparsers.add_parser("handoff", help="Render a compact handoff context.")
    handoff_parser.add_argument("--agent", required=True)
    handoff_parser.add_argument("--task")
    handoff_parser.add_argument("--include-agent-notes", action="store_true")
    handoff_parser.add_argument("--output", help="Write to a file instead of stdout.")

    check_parser = subparsers.add_parser(
        "check",
        help="Validate isolation and shared memory rules.",
    )
    check_parser.add_argument("--format", choices=["text", "json"], default="text")

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check local Multi-Agent Memory Isolation readiness.",
    )
    doctor_parser.add_argument("--format", choices=["text", "json"], default="text")

    status_parser = subparsers.add_parser("status", help="Show memory counts.")
    status_parser.add_argument("--format", choices=["text", "json"], default="text")

    schema_parser = subparsers.add_parser(
        "schema",
        help="Print a Multi-Agent Memory Isolation JSON schema.",
    )
    schema_parser.add_argument(
        "--kind",
        choices=["shared-memory", "agent-note", "policy"],
        default="shared-memory",
    )
    schema_parser.add_argument("--output", help="Write the schema to a file instead of stdout.")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = AgentMemoryStore(args.root)

    try:
        if args.command == "init":
            created = store.init(force=args.force)
            print(
                "Multi-Agent Memory Isolation initialized at "
                f"{display_path(store.base, store.root)}"
            )
            print(f"created_or_verified={len(created)}")
            return 0

        if args.command == "note":
            record = store.create_note(
                agent=args.agent,
                kind=args.kind,
                text=args.text,
                evidence=args.evidence,
            )
            emit_record(record, args.format, f"private note saved: {record['id']}")
            return 0

        if args.command == "promote":
            if args.from_note:
                record = store.promote_note(
                    agent=args.agent,
                    note_id=args.from_note,
                    kind=args.kind,
                    evidence=args.evidence or None,
                )
            else:
                if not args.text:
                    raise ValueError("promote requires --text unless --from-note is used")
                record = store.promote_memory(
                    agent=args.agent,
                    kind=args.kind or "fact",
                    text=args.text,
                    evidence=args.evidence,
                    source_note=args.source_note,
                )
            emit_record(record, args.format, f"shared memory promoted: {record['id']}")
            return 0

        if args.command == "handoff":
            agent_notes = store.read_agent_notes(args.agent) if args.include_agent_notes else None
            content = render_handoff(
                agent=args.agent,
                task=args.task,
                shared_memory=store.read_shared_memory(),
                agent_notes=agent_notes,
            )
            if args.output:
                output_path = Path(args.output)
                write_handoff(output_path, content)
                print(f"handoff written: {display_path(output_path, store.root)}")
            else:
                print(content)
            write_handoff(store.handoff_path, content)
            return 0

        if args.command == "check":
            result = validate_store(store)
            if args.format == "json":
                print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
            else:
                print(
                    "Multi-Agent Memory Isolation: PASS"
                    if result.ok
                    else "Multi-Agent Memory Isolation: FAIL"
                )
                for warning in result.warnings:
                    print(f"warning: {warning}")
                for error in result.errors:
                    print(f"error: {error}")
            return 0 if result.ok else 1

        if args.command == "doctor":
            result = validate_store(store)
            payload = status_payload(store)
            payload.update(result.to_dict())
            if args.format == "json":
                print(json.dumps(payload, indent=2, sort_keys=True))
            else:
                print(
                    "Multi-Agent Memory Isolation doctor: PASS"
                    if result.ok
                    else "Multi-Agent Memory Isolation doctor: FAIL"
                )
                print(f"shared_records={payload['shared_records']}")
                print(f"agents={len(payload['agents'])}")
                for warning in result.warnings:
                    print(f"warning: {warning}")
                for error in result.errors:
                    print(f"error: {error}")
            return 0 if result.ok else 1

        if args.command == "status":
            payload = status_payload(store)
            if args.format == "json":
                print(json.dumps(payload, indent=2, sort_keys=True))
            else:
                print(f"shared_records={payload['shared_records']}")
                print(f"agents={len(payload['agents'])}")
            return 0

        if args.command == "schema":
            content = schema_text(args.kind)
            if args.output:
                output_path = Path(args.output)
                output_path.write_text(content, encoding="utf-8")
                print(f"schema written: {display_path(output_path, store.root)}")
            else:
                print(content)
            return 0

    except Exception as exc:
        print(f"error: {safe_error_message(exc, store.root)}", file=sys.stderr)
        return 2

    parser.error("unknown command")
    return 2


def emit_record(record: dict[str, object], fmt: str, message: str) -> None:
    if fmt == "json":
        print(json.dumps(record, indent=2, sort_keys=True))
    else:
        print(message)


def display_path(path: Path, root: Path) -> str:
    try:
        return str(path.resolve().relative_to(root))
    except ValueError:
        if path.is_absolute():
            return path.name
        return str(path)


def safe_error_message(exc: Exception, root: Path) -> str:
    message = str(exc)
    root_text = str(root)
    return message.replace(f"{root_text}/", "").replace(root_text, ".")


def status_payload(store: AgentMemoryStore) -> dict[str, object]:
    shared = store.read_shared_memory()
    agents_root = store.base / "agents"
    agent_dirs = sorted(agents_root.glob("*")) if agents_root.exists() else []
    return {
        "shared_records": len(shared),
        "agents": [path.name for path in agent_dirs if path.is_dir()],
        "root": ".",
        "context_dir": str(store.base.relative_to(store.root)),
    }


def schema_text(kind: str) -> str:
    resource_name = f"{kind}.schema.json"
    schema = resources.files("agent_memory_isolation").joinpath("schemas", resource_name)
    return schema.read_text(encoding="utf-8")
