# OpenClaw-Style Local Agent Stack Multi-Agent Memory Isolation Rule

Use Multi-Agent Memory Isolation as the local memory boundary:

- shared memory: promoted records only;
- agent memory: draft notes scoped to one agent;
- handoff: compact prompt material for the next run;
- check: guard against evidence-free shared claims.

Recommended start command:

```bash
agent-memory-isolation handoff --agent openclaw --task "<task>"
```

Recommended finish command:

```bash
agent-memory-isolation check
```
