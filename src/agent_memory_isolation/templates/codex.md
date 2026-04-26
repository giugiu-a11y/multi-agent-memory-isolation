# Codex Multi-Agent Memory Isolation Rule

Before starting work:

```bash
agent-memory-isolation handoff --agent codex --task "<task>"
```

During work:

```bash
agent-memory-isolation note --agent codex --kind observation --text "<draft note>"
```

Before promoting shared memory:

```bash
agent-memory-isolation promote --agent codex --kind decision --text "<decision>" --evidence "<file, command, issue, or reviewer evidence>"
```

Rule: private notes are useful thinking, not shared truth.
