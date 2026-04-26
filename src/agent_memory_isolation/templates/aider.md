# Aider Multi-Agent Memory Isolation Rule

Before editing, generate a handoff:

```bash
agent-memory-isolation handoff --agent aider --task "<task>"
```

After editing, promote only the facts that have evidence:

```bash
agent-memory-isolation promote --agent aider --kind fact --text "<fact>" --evidence "<test or file evidence>"
```
