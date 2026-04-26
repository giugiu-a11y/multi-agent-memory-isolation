# Incubation Plan

Status: completed for the v0.1.0 public alpha candidate. Keep this document as historical incubation context until the final launch gate is refreshed.

Target window: a few days to one week.

## Goal

Make Multi-Agent Memory Isolation feel obvious, useful, and safe before the first public push.

The launch should not feel like "another memory tool." It should feel like the missing safety boundary for people running many AI agents.

## Product Thesis

Multi-agent AI systems fail when agents share too little context or too much unverified context.

Multi-Agent Memory Isolation gives teams:

- individual context isolation;
- shared memory only after evidence;
- compact handoffs for the next agent;
- plain local files that reviewers can inspect.

## This Week

### Day 1: Product Shape

- Confirm the README explains the pain in under one minute.
- Confirm the command set is small enough to remember.
- Keep the product local-first and dependency-light.

### Day 2: Contracts

- Harden JSON schemas.
- Add more invalid-record tests.
- Make schema export useful for external agent stacks.

### Day 3: Integrations

- Improve templates for Codex, Claude Code, Cursor, OpenCode, Aider, Cline, Hermes-style orchestrators, and OpenClaw-style stacks.
- Add one end-to-end guide for running Multi-Agent Memory Isolation with DoneProof.

### Day 4: Release Engineering

- Run full prepublish.
- Verify packaging from wheel.
- Verify CI locally where possible.
- Keep repository private/local until GitHub checks are configured.

### Day 5: Security and Privacy

- Run `gitleaks`.
- Scan git history for local paths, emails, private names, and internal project names.
- Confirm ignored local governance files are not staged.

### Day 6: Copy and Positioning

- Tighten launch copy.
- Prepare short recommendation-style post.
- Prepare README first screen for GitHub visitors.

### Day 7: Launch Decision

- Create private GitHub repo.
- Push privately.
- Let GitHub CI run.
- Configure branch protection and secret scanning.
- Decide whether to open public based on checks, not excitement.

## Cut Before Launch

Do not add before v0.1.0:

- hosted sync;
- vector database;
- dashboard;
- telemetry;
- automatic chat scraping;
- complex policy engine.

## Add Only If It Makes Launch Stronger

- `schema` command improvements;
- `promote --from-note` improvements;
- DoneProof linkage docs;
- better stale handoff warnings;
- examples that make the pain instantly clear.
