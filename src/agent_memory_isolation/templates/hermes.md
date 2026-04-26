# Hermes-Style Orchestrator Multi-Agent Memory Isolation Rule

For each routed agent:

1. Generate a handoff with shared memory only.
2. Keep the agent's draft notes under its own agent name.
3. Promote only evidence-backed records after the run.

Suggested commands:

```bash
agent-memory-isolation handoff --agent hermes --task "<route task>"
agent-memory-isolation note --agent hermes --kind observation --text "<private orchestration note>"
agent-memory-isolation promote --agent hermes --kind risk --text "<risk>" --evidence "<receipt, command, file, or issue>"
```

The orchestrator may coordinate agents, but it should not collapse all draft memory into one shared pool.
