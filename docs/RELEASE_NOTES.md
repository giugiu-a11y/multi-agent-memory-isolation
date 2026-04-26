# Release Notes

## v0.1.0

Initial public alpha candidate.

### Added

- `.agent-memory/` local storage.
- Agent-private notes.
- Evidence-gated shared memory.
- Markdown handoff rendering.
- `check`, `doctor`, and `status`.
- JSON schema export.
- `promote --from-note`.
- Doctor warnings for missing or stale handoffs after shared memory changes.
- Path-minimal routine command output.
- Prepublish shell checks now enforce path-minimal routine command output.
- Package build and wheel smoke coverage in prepublish checks.
- GitHub Actions CI for Python 3.10, 3.11, and 3.12, including package build and release-path smoke.
- Release gates now work with either `uv` or a standard `pip install -e ".[dev]"` setup.
- Templates for Codex, Claude Code, Cursor, OpenCode, Aider, Cline, Hermes-style orchestrators, and OpenClaw-style local agent stacks.
- Documentation for architecture, integrations, security, and launch.

### Not Included Yet

- PyPI package.
- Hosted service.
- Vector search.
- Dashboard.
