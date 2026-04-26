# Agent Instructions

Multi-Agent Memory Isolation exists to prevent multi-agent memory drift.

## Rules

- Never treat an agent-local note as shared truth.
- Shared memory requires evidence.
- Keep examples generic. Do not mention private people, private companies, local machine paths, internal project names, or private automation details.
- Before claiming readiness, run the real checks in `make prepublish`.
- Update documentation together with behavior changes.

## Local Commands

```bash
python3 -m pip install -e ".[dev]"
make prepublish
```

## Public Positioning

Use this wording:

> Memory layer for multi-agent AI systems with individual context isolation.

Avoid claiming Multi-Agent Memory Isolation verifies correctness or replaces code review.
