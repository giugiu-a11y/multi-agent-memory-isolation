# Basic Flow

```bash
agent-memory-isolation init

agent-memory-isolation note \
  --agent codex \
  --kind observation \
  --text "Need to verify CI names before release."

agent-memory-isolation promote \
  --agent codex \
  --kind decision \
  --text "Shared memory requires evidence before handoff." \
  --evidence "Multi-Agent Memory Isolation policy"

agent-memory-isolation handoff --agent claude --task "Review release readiness"
agent-memory-isolation doctor
```
