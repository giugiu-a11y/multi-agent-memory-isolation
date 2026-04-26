# Demo

This transcript shows the core flow.

```bash
agent-memory-isolation init
```

```text
Multi-Agent Memory Isolation initialized at .agent-memory
```

Add a private note:

```bash
agent-memory-isolation note \
  --agent codex \
  --kind observation \
  --text "The next agent should check branch protection before release."
```

Promote a shared decision with evidence:

```bash
agent-memory-isolation promote \
  --agent codex \
  --kind decision \
  --text "Release work must pass prepublish before tagging." \
  --evidence "Makefile prepublish target"
```

Promote from a private note:

```bash
agent-memory-isolation note \
  --agent codex \
  --kind decision \
  --text "Shared memory must not include raw scratchpads." \
  --evidence "architecture rule"

agent-memory-isolation promote --agent codex --from-note "<note-id>"
```

Generate a handoff:

```bash
agent-memory-isolation handoff --agent claude --task "Review the release"
```

The handoff includes the promoted decision. It does not include the private Codex note.

Run the doctor:

```bash
agent-memory-isolation doctor
```

```text
Multi-Agent Memory Isolation doctor: PASS
shared_records=1
agents=1
```
