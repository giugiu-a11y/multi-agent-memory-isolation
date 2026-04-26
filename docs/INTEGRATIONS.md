# Agent Integrations

Multi-Agent Memory Isolation is tool-agnostic. Any agent that can run shell commands can use it.

It ships practical rules for Hermes-style orchestrators, OpenClaw-style local agent stacks, Codex, Claude Code, Cursor, OpenCode, Aider, and Cline. These are templates, not official integrations.

## Universal Start Prompt

Add this to agent instructions:

```text
Before starting work, run:

agent-memory-isolation handoff --agent <agent-name> --task "<task>"

Use promoted shared memory as context. Do not treat another agent's private notes as truth.
Promote new shared memory only with evidence.
```

## Codex

```bash
agent-memory-isolation handoff --agent codex --task "<task>"
agent-memory-isolation note --agent codex --kind observation --text "<private note>"
agent-memory-isolation promote --agent codex --kind decision --text "<decision>" --evidence "<proof>"
agent-memory-isolation promote --agent codex --from-note "<note-id>"
agent-memory-isolation doctor
```

## Claude Code

Use a handoff at the start of each continuation:

```bash
agent-memory-isolation handoff --agent claude --task "<task>"
```

At the end, promote only records that should survive into the next agent run.

## Cursor

Keep the latest handoff visible:

```bash
agent-memory-isolation handoff --agent cursor --task "<task>" --output .agent-memory/handoffs/cursor.md
```

Cursor rules should say: shared memory is canonical, private notes are not.

## OpenCode

```bash
agent-memory-isolation handoff --agent opencode --task "<task>"
agent-memory-isolation doctor
```

Use `doctor` as a pre-handoff and pre-PR gate.

## Hermes-Style Orchestrators

For orchestrators that route work across many agents:

1. Generate a clean handoff for the target agent.
2. Let the target agent write private notes under its own name.
3. Promote only evidence-backed results after the run.

```bash
agent-memory-isolation handoff --agent hermes --task "<route task>"
agent-memory-isolation promote --agent hermes --kind risk --text "<risk>" --evidence "<receipt or command>"
```

This keeps the orchestrator from turning every draft thought into global truth.

## OpenClaw-Style Local Agent Stacks

Use Multi-Agent Memory Isolation as the memory boundary between local agents:

```bash
agent-memory-isolation handoff --agent openclaw --task "<task>"
agent-memory-isolation check
```

Recommended policy:

- one agent name per worker role;
- private notes stay scoped;
- shared memory is promoted only after evidence;
- handoffs should be regenerated before task continuation.

## DoneProof Pairing

Recommended sequence:

```bash
agent-memory-isolation handoff --agent codex --task "<task>"
# agent works
doneproof new --task "<task>" --changed-file "<file>" --command "passed:<cmd>" --evidence "<proof>"
doneproof check
agent-memory-isolation promote --agent codex --kind fact --text "<what should persist>" --evidence "DoneProof receipt <id>"
agent-memory-isolation doctor
```

Multi-Agent Memory Isolation handles the next agent's context. DoneProof handles the finished work receipt.
