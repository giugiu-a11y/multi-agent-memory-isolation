# Multi-Agent Memory Isolation For Hermes, OpenClaw, Codex, And Claude Code

Evidence-gated context handoffs so AI agents inherit verified state, not stale summaries or another worker's scratchpad.

Multi-Agent Memory Isolation is a local memory boundary for Hermes-style orchestrators, OpenClaw-style local agent stacks, Codex, Claude Code, Cursor, OpenCode, Aider, Cline, and custom multi-agent AI systems.

Run two coding agents on the same repo for long enough and you learn the weird part fast:

the hard part is not starting another agent.

It is making sure the next one inherits reality, not vibes.

One agent leaves a guess. Another treats it as fact. A stale summary becomes the starting point for the next run. That is how a useful agent team slowly turns into context soup.

Multi-Agent Memory Isolation gives that handoff a spine:

- private notes stay private;
- shared memory has to earn its place with evidence;
- the next agent gets a handoff you can inspect, diff, and test.

No cloud dashboard. No telemetry. No magic memory.

Just files in `.agent-memory/`: JSONL records, handoffs, templates, and schemas.

It works with Codex, Claude Code, Cursor, OpenCode, Aider, Cline, and local orchestrators.

## Who It Is For

- Hermes and OpenClaw users who need memory shared across agents without contaminating every worker.
- Codex, Claude Code, Cursor, OpenCode, Aider, and Cline users running parallel or sequential agent work.
- Teams where one agent's guess can quietly become another agent's starting context.
- Local-first operators who want plain files, inspectable handoffs, and no hosted memory service.

## Why It Exists

Multi-agent systems do not fail only because agents forget.

They fail when the wrong thing gets carried forward:

- one agent's guess becomes another agent's premise;
- old context survives after the project changed;
- a handoff sounds confident but hides open risks;
- draft notes from one run leak into a different task;
- the next agent starts from a summary instead of verifiable state.

Multi-Agent Memory Isolation adds one rule:

> Agents can think privately. Shared memory has to prove itself.

## What You Get

- local `.agent-memory/` memory storage;
- agent-private notes scoped by agent name;
- evidence-gated shared memory;
- compact handoff files for the next agent run;
- validation that catches evidence-free shared claims;
- templates for Codex, Claude Code, Cursor, OpenCode, Aider, Cline, Hermes-style orchestrators, and OpenClaw-style local agent stacks.

## Quick Start

Requires Python 3.10+.

Local development install:

```bash
python3 -m pip install -e ".[dev]"
```

Initialize a repository:

```bash
agent-memory-isolation init
```

Save a private note for the current agent:

```bash
agent-memory-isolation note \
  --agent codex \
  --kind observation \
  --text "This needs a migration check before the next edit."
```

Promote shared memory only when there is evidence:

```bash
agent-memory-isolation promote \
  --agent codex \
  --kind decision \
  --text "Use evidence-gated shared memory for handoffs." \
  --evidence "docs/ARCHITECTURE.md reviewed"
```

Promote a private note after it becomes worth sharing:

```bash
agent-memory-isolation promote --agent codex --from-note "<note-id>"
```

Generate a handoff for the next agent:

```bash
agent-memory-isolation handoff --agent claude --task "Continue the release review"
```

Validate the memory boundary:

```bash
agent-memory-isolation doctor
```

`doctor` warns when shared memory changed after the latest handoff, so the next agent does not start from stale context.

Routine command output avoids printing absolute local roots, which makes pasted logs safer for public issues and reviews.

## The Model

Multi-Agent Memory Isolation separates memory into two layers.

### Agent-Private Memory

Private notes are useful scratch space for one agent. They can contain uncertainty, hypotheses, partial observations, or local planning.

They are not included in other agents' handoffs by default.

### Shared Memory

Shared memory is the canonical layer. It contains only promoted records:

- `fact`
- `decision`
- `risk`
- `open_question`

Every shared record except an open question requires evidence.

## Example Handoff

```text
# Multi-Agent Memory Isolation Handoff

- Agent: `claude`
- Task: Continue the release review

## Shared Truth

Only promoted records appear here.
Agent-local draft notes from other agents are excluded.

### Decisions
- Use evidence-gated shared memory for handoffs.
  Evidence: docs/ARCHITECTURE.md reviewed
```

## How It Fits With DoneProof

DoneProof answers:

> Did the agent prove what it delivered?

Multi-Agent Memory Isolation answers:

> Does the next agent start with the right context?

Used together:

- Multi-Agent Memory Isolation before work: load the right memory boundary.
- DoneProof after work: leave a receipt for what changed.
- Multi-Agent Memory Isolation after review: promote only the facts worth carrying forward.

## Commands

```bash
agent-memory-isolation init
agent-memory-isolation note --agent codex --text "Private draft note"
agent-memory-isolation promote --agent codex --kind fact --text "Shared fact" --evidence "test output"
agent-memory-isolation promote --agent codex --from-note "<note-id>"
agent-memory-isolation handoff --agent claude --task "Next task"
agent-memory-isolation check
agent-memory-isolation doctor
agent-memory-isolation schema --kind shared-memory
agent-memory-isolation status --format json
```

## Design Principles

- Local-first. No hosted service required.
- No telemetry.
- No private prompt scraping.
- No global write-everything memory.
- Evidence beats confidence.
- Isolation first, sharing second.
- Plain files over hidden state.

## Documentation

- [Architecture](docs/ARCHITECTURE.md)
- [Agent integrations](docs/INTEGRATIONS.md)
- [Security model](docs/SECURITY_MODEL.md)
- [Demo](docs/DEMO.md)
- [DoneProof pairing](docs/DONEPROOF_PAIRING.md)
- [Publishing checklist](docs/PUBLISHING_CHECKLIST.md)
- [Launch copy](docs/LAUNCH_COPY.md)
- [Changelog](CHANGELOG.md)
- [Support](SUPPORT.md)
- [Roadmap](ROADMAP.md)

## Status

Multi-Agent Memory Isolation is a v0.1.0 public alpha.

Every public release should pass `make prepublish`, the privacy scan, package checks, and GitHub CI before tagging.
