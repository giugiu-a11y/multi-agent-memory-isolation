# Field Lessons

Multi-Agent Memory Isolation is built from recurring failures seen in real multi-agent work.

The details are intentionally generic so the project stays safe to publish.

## 1. Memory Without Isolation Becomes Contamination

If every agent writes into one shared pile, draft guesses become future assumptions.

Multi-Agent Memory Isolation response:

- agent notes are private by default;
- only promoted records enter shared memory;
- handoffs exclude other agents' draft notes.

## 2. No Memory Becomes Rework

Without a durable handoff, the next agent rereads, misreads, or reinvents state.

Multi-Agent Memory Isolation response:

- `handoff` renders compact current context;
- shared facts are portable between agents;
- open questions stay visible.

## 3. Confidence Is Not Evidence

Agents often write summaries that sound final while the real state is still unverified.

Multi-Agent Memory Isolation response:

- shared facts, decisions, and risks require evidence;
- `doctor` fails or warns when memory shape is unsafe;
- open questions can stay unresolved without pretending to be facts.

## 4. Orchestrators Need Boundaries

An orchestrator can coordinate many agents, but it should not merge every worker's scratchpad into canonical memory.

Multi-Agent Memory Isolation response:

- each agent has a scoped namespace;
- the orchestrator promotes only reviewed results;
- the next handoff contains shared truth, not raw execution noise.

## 5. Small Protocols Beat Big Dashboards Early

The first useful version is not a memory platform. It is a repeatable rule that can run in any repository.

Multi-Agent Memory Isolation response:

- plain files;
- no server;
- no telemetry;
- simple CLI;
- easy Git diff review.
