# Contributing

Thanks for helping improve Multi-Agent Memory Isolation.

## Local Setup

```bash
python3 -m pip install -e ".[dev]"
make prepublish
```

## Pull Request Standard

Before opening a PR:

- explain the problem;
- keep the change small;
- add or update tests;
- update docs when behavior changes;
- run `make prepublish`;
- do not include secrets, personal data, private paths, or internal project details.

## Design Standard

Multi-Agent Memory Isolation should stay small.

Prefer:

- local files;
- inspectable JSONL;
- deterministic checks;
- explicit evidence;
- simple agent instructions.

Avoid:

- hosted dependencies by default;
- telemetry;
- hidden state;
- global memory that mixes all agents' drafts;
- broad claims that Multi-Agent Memory Isolation verifies correctness.
