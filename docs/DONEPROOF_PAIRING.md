# DoneProof Pairing

Multi-Agent Memory Isolation and DoneProof solve two different parts of the same operating problem.

## Before Work

Use Multi-Agent Memory Isolation to load the right memory boundary:

```bash
agent-memory-isolation handoff --agent codex --task "Implement the feature"
```

## During Work

Use private notes for local thinking:

```bash
agent-memory-isolation note \
  --agent codex \
  --kind observation \
  --text "The next run should recheck the release workflow."
```

## After Work

Use DoneProof to leave a delivery receipt:

```bash
doneproof new \
  --task "Implement the feature" \
  --changed-file "src/app.py" \
  --command "passed:pytest" \
  --evidence "pytest passed" \
  --risk "Manual UI check not performed"

doneproof check
```

## After Review

Promote only the durable facts worth carrying forward:

```bash
agent-memory-isolation promote \
  --agent codex \
  --kind fact \
  --text "The feature has pytest coverage." \
  --evidence "DoneProof receipt"

agent-memory-isolation doctor
```

## Mental Model

- Multi-Agent Memory Isolation: what should the next agent know?
- DoneProof: what did this agent prove it delivered?

Together, they reduce fake completion and context drift without adding a hosted platform.
