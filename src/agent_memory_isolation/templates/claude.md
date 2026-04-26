# Claude Code Multi-Agent Memory Isolation Rule

Start each multi-agent task by reading a Multi-Agent Memory Isolation handoff:

```bash
agent-memory-isolation handoff --agent claude --task "<task>"
```

Use `note` for local reasoning that should not contaminate other agents. Use `promote` only when the claim has evidence.

Do not copy another agent's draft notes into your prompt as fact.
