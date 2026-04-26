# Security Model

Multi-Agent Memory Isolation is local-first and stores plain files in the repository.

That is intentional: reviewers and agents can inspect the memory layer without a server.

## What Multi-Agent Memory Isolation Protects Against

- accidental promotion of draft notes into shared memory;
- evidence-free shared claims;
- stale handoffs with no visible source records;
- agent-to-agent contamination from raw scratch notes;
- obvious secret-shaped strings in Multi-Agent Memory Isolation records;
- absolute local roots in routine command output.

## What It Does Not Protect Against

- malicious contributors editing files directly;
- secrets already committed elsewhere in the repository;
- private data pasted into promoted memory;
- incorrect evidence;
- hallucinated claims outside `.agent-memory/`.

## Public Release Checklist

Before publishing a repository that uses Multi-Agent Memory Isolation:

```bash
agent-memory-isolation doctor
gitleaks detect --source . --redact
```

Use a real secret scanner before public release. The built-in warning scan is a local safety net, not a full audit.

Routine output is intentionally path-minimal, but generated handoffs and memory records can still contain whatever a user typed. Review `.agent-memory/` before sharing logs or artifacts.
