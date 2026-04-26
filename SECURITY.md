# Security Policy

## Supported Versions

Multi-Agent Memory Isolation is in pre-release. Security fixes target the latest release line.

## Reporting a Vulnerability

Please open a private security advisory on GitHub once the repository is public.

Do not include live secrets or private data in public issues.

## Scope

Security-sensitive areas include:

- secret-looking content in `.agent-memory/`;
- accidental inclusion of personal data in handoffs;
- path traversal in agent names or output paths;
- unsafe parsing of memory files;
- CI or release workflow changes.

## Local Checks

```bash
agent-memory-isolation doctor
gitleaks detect --source . --redact
```
