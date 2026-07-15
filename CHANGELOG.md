# Changelog

All notable changes to Multi-Agent Memory Isolation will be documented here.

## Unreleased

- Pinned every external GitHub Action to a verified full commit SHA.
- Upgraded Checkout to v7 and replaced the unverified Gitleaks binary download with the pinned v3 Action.
- Expanded the CI secret scan from the checked-out snapshot to complete Git history and added regression tests for the supply-chain policy.

## 0.1.0 - Public Alpha Candidate

- Added the Multi-Agent Memory Isolation CLI.
- Added agent-private notes and evidence-gated shared memory.
- Added handoff rendering for the next agent run.
- Added validation for isolation rules and stale handoffs.
- Added templates for Codex, Claude Code, Cursor, OpenCode, Aider, Cline, Hermes-style orchestrators, and OpenClaw-style local agent stacks.
- Added local release, privacy, and package gates.
