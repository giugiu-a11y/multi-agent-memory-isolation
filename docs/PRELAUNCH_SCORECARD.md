# Prelaunch Scorecard

Use this as the launch gate before public visibility.

## Product

- [x] README explains the pain in under one minute.
- [x] Quick Start works from a clean checkout.
- [x] A new user can understand private notes vs shared memory without a call.
- [x] `promote --from-note` feels natural.
- [x] `schema` output is useful for integrations.
- [x] `doctor` catches missing or stale handoffs.
- [x] Routine command output does not expose absolute local roots.

## Code

- [x] `make prepublish` passes.
- [x] `scripts/prepublish_check.sh` passes.
- [x] Tests cover isolation, evidence gates, schema export, and from-note promotion.
- [x] Package includes templates and schemas.
- [x] No unused complexity.

## Security

- [x] `gitleaks detect --source . --redact` passes.
- [x] Git history scan has no private names, internal project names, local paths, or personal emails.
- [x] Ignored local files remain untracked.
- [x] Git author uses GitHub noreply.

## GitHub

- [x] Private repo created before public visibility.
- [x] CI passes on GitHub.
- [ ] Branch protection enabled on `main` with required `CI` status checks after the final public-ready push.
- [ ] Secret scanning and push protection verified for the final repository configuration.
- [ ] Release tag created only after final checks.

## Launch

- [x] Launch copy is short and pain-led.
- [x] No claims that Multi-Agent Memory Isolation proves correctness.
- [x] No private origin story.
- [x] DoneProof relationship is clear.
- [x] One external reviewer can understand the repo without explanation.

## Evidence Snapshot

Last full local launch verification baseline: 2026-04-25.

Refresh this scorecard before public visibility.

Required local evidence:

- `make prepublish`
- `scripts/prepublish_check.sh`
- `gitleaks detect --source . --redact`
- `git diff --check`
- privacy scan for local paths, private names, emails, tokens, secrets, cookies, and environment files

GitHub release evidence must be refreshed before public visibility.

GitHub release evidence:

- repository visibility verified for the intended launch state;
- latest `main` CI passed on Python 3.10, 3.11, and 3.12 after release-gate hardening;
- workflow token default set to read-only and PR approval by Actions disabled;
- branch protection enabled on `main` with strict `CI` checks when available;
- secret scanning and push protection verified when available;
- release `v0.1.0` created after final checks.
