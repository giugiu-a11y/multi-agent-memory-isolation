# Publishing Checklist

Multi-Agent Memory Isolation should not be published until every item below has real evidence.

## Code

```bash
make prepublish
bash scripts/prepublish_check.sh
```

Required:

- lint passes;
- tests pass;
- compile check passes;
- CLI smoke passes;
- package build passes;
- built wheel installs and runs from a clean virtual environment;
- `agent-memory-isolation doctor` passes.

## Privacy

Run:

```bash
agent-memory-isolation doctor
bash scripts/privacy_check.sh
gitleaks detect --no-git --source . --redact --no-banner
```

Required:

- no local machine paths;
- no personal emails;
- no tokens or keys;
- no private project names;
- no private people names;
- no internal system details.

## Repository

Required before public visibility:

- README explains the pain in under one minute;
- GitHub description names the category: memory isolation and evidence-gated handoffs for Hermes, OpenClaw, Codex, Claude Code, Cursor, and multi-agent AI systems;
- GitHub topics include `ai-agents`, `multi-agent`, `agent-memory`, `context-engineering`, `handoff`, `hermes`, `openclaw`, `codex`, `claude-code`, `cursor`, and `agentops`;
- docs include architecture, integrations, demo, security, roadmap;
- private GitHub repo exists before public visibility;
- CI passes on Python 3.10, 3.11, and 3.12;
- Security workflow passes with `gitleaks detect --no-git --source . --redact --no-banner`;
- branch protection is enabled after pushing;
- secret scanning and push protection are enabled if available;
- release notes are written;
- first tag is created only after a clean prepublish run.

Publication order:

1. push privately;
2. wait for GitHub CI;
3. configure branch protection and secret scanning if available;
4. rerun the privacy checklist;
5. only then switch the repository to public.

## Launch

Do not overexplain.

Lead with the pain:

> Multi-agent systems fail when agents share too little context or too much unverified context.

Then show the simple rule:

> Agents can think privately. Shared memory needs evidence.
