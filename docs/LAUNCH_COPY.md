# Multi-Agent Memory Isolation Messaging Notes

Use this when publishing the repository, writing release notes, posting on social platforms, or replying to early users.

## Core Position

Multi-Agent Memory Isolation is for people running more than one coding agent on the same project, including Hermes-style orchestrators, OpenClaw-style local agent stacks, Codex, Claude Code, Cursor, OpenCode, Aider, and Cline.

It keeps the next handoff from inheriting guesses, stale summaries, and another agent's scratchpad.

Private notes stay private. Shared memory has to prove itself.

## Main Hook

```text
The hard part of multi-agent coding is making sure the next agent inherits reality, not vibes.
```

## Primary Problem

The problem is not just forgetting.

It is bad context becoming shared truth:

- one agent's guess becomes the next agent's premise;
- stale summaries survive after the project changes;
- a handoff sounds confident but hides risk;
- private scratchpad notes leak into the next run.

## Operating Rule

```text
Agents can think privately. Shared memory has to prove itself.
```

## GitHub Description

```text
Memory isolation and evidence-gated handoffs for Hermes, OpenClaw, Codex, Claude Code, Cursor, and multi-agent AI systems.
```

## GitHub Topics

```text
ai-agents, multi-agent, agent-memory, context-engineering, handoff, hermes, openclaw, codex, claude-code, cursor, agentops
```

## One-Liner

```text
Shared truth without shared contamination.
```

```text
Reality, not vibes, for the next agent.
```

## Short Launch Post

```text
Multi-agent coding has a weird failure mode:

each agent can be useful on its own,
but the handoff slowly fills with guesses, stale summaries, and half-true context.

Multi-Agent Memory Isolation is a small local guard for that.

Private notes stay private.
Shared memory has to prove itself.

https://github.com/giugiu-a11y/multi-agent-memory-isolation
```

## Direct Technical Post

```text
The hard part of multi-agent coding is not just memory.

It is memory without contamination.

Multi-Agent Memory Isolation gives each agent private notes, then only promotes evidence-backed facts, decisions, risks, and open questions into shared memory.

Agents can think privately.
Shared memory has to prove itself.

https://github.com/giugiu-a11y/multi-agent-memory-isolation
```

## Recommendation-Style Post

```text
If you run multiple coding agents, this is the failure to watch:

one agent's guess quietly becomes the next agent's context.

Multi-Agent Memory Isolation is a small local guard for that:
draft notes stay private, and shared memory has to prove itself.
```

## Recommendation-Style Post For Hermes/OpenClaw Users

```text
If you run Hermes, OpenClaw, or any multi-agent coding setup, watch for this:

one agent's guess quietly becomes the next agent's memory.

Multi-Agent Memory Isolation is a small local guard for that.
Private notes stay private.
Shared memory has to prove itself.
```

## HN / Reddit Style

```text
Multi-Agent Memory Isolation is for a boring but painful failure mode in multi-agent work: the handoff gets polluted.

Each agent may be useful on its own, but shared context slowly collects guesses, stale assumptions, and private scratchpad notes.

Multi-Agent Memory Isolation keeps a local `.agent-memory/` directory with private notes per agent, evidence-gated shared memory, and handoff files for the next run.

It is intentionally small: plain files, JSONL, schemas, tests. No telemetry, no hosted service, no magic memory.
```

## Release Blurb

```text
Multi-Agent Memory Isolation v0.1.0 adds local handoffs for multi-agent coding: private notes per agent, evidence-gated shared memory, schema export, stale handoff warnings, and templates for Codex, Claude Code, Cursor, OpenCode, Aider, Cline, Hermes-style orchestrators, and OpenClaw-style local agent stacks.
```

## DoneProof Relationship

```text
DoneProof answers: did the agent prove what it delivered?

Multi-Agent Memory Isolation answers: does the next agent start with the right context?

They are separate tools, but they fit together naturally: Multi-Agent Memory Isolation before the next run, DoneProof after delivery.
```

## Tone Rules

- Lead with the handoff problem, not generic AI memory.
- Let it sound excited. The enemy is fake certainty, not marketing.
- Keep the hype attached to a concrete pain: polluted handoffs, stale summaries, private scratchpads becoming shared context.
- Prefer "handoff", "private notes", "reality, not vibes", and "shared memory has to prove itself."
- Use "evidence-gated shared memory" as the concrete differentiator.
- Keep DoneProof as a useful pairing, not a dependency.

## Avoid Saying

- "solves hallucination"
- "guarantees correctness"
- "autonomous memory brain"
- "replaces review"
- "AI memory OS"
- "second brain"
- private origin stories
