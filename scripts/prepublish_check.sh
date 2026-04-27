#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

choose_python_bin() {
  local candidate
  for candidate in "${PYTHON_BIN:-}" python python3 python3.12 python3.11 python3.10; do
    if [[ -z "$candidate" ]]; then
      continue
    fi
    if ! command -v "$candidate" >/dev/null 2>&1; then
      continue
    fi
    if "$candidate" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 10) else 1)
PY
    then
      command -v "$candidate"
      return 0
    fi
  done
  return 1
}

PYTHON_BIN="$(choose_python_bin)"

"$PYTHON_BIN" - <<'PY'
import sys

if sys.version_info < (3, 10):
    raise SystemExit("Multi-Agent Memory Isolation prepublish checks require Python 3.10+.")
PY

SMOKE_ROOT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-$$"
WHEEL_SMOKE_ROOT="${TMPDIR:-/tmp}/agent-memory-isolation-wheel-smoke-$$"
WHEEL_VENV="${TMPDIR:-/tmp}/agent-memory-isolation-wheel-venv-$$"
INIT_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-init-$$.out"
HANDOFF_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-handoff-$$.out"
SCHEMA_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-schema-$$.out"
STATUS_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-status-$$.json"
DOCTOR_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-doctor-$$.json"
NOTE_ERR="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-note-$$.err"
WHEEL_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-wheel-$$.out"
BUILD_OUT="${TMPDIR:-/tmp}/agent-memory-isolation-prepublish-build-$$.out"

cleanup() {
  rm -rf \
    "$SMOKE_ROOT" \
    "$WHEEL_SMOKE_ROOT" \
    "$WHEEL_VENV" \
    "$INIT_OUT" \
    "$HANDOFF_OUT" \
    "$SCHEMA_OUT" \
    "$STATUS_OUT" \
    "$DOCTOR_OUT" \
    "$NOTE_ERR" \
    "$WHEEL_OUT" \
    "$BUILD_OUT"
}

trap cleanup EXIT

if command -v rg >/dev/null 2>&1; then
  contains_fixed() { rg -F "$1" "${@:2}" >/dev/null; }
else
  contains_fixed() { grep -F "$1" "${@:2}" >/dev/null; }
fi

SECURITY_WORKFLOW=".github/workflows/security.yml"
if [[ ! -f "$SECURITY_WORKFLOW" ]]; then
  echo "Multi-Agent Memory Isolation prepublish checks expected ${SECURITY_WORKFLOW}." >&2
  exit 1
fi
if ! contains_fixed "gitleaks detect --no-git --source . --redact --no-banner" "$SECURITY_WORKFLOW"; then
  echo "Multi-Agent Memory Isolation prepublish checks expected an explicit gitleaks scan command in ${SECURITY_WORKFLOW}." >&2
  exit 1
fi

if command -v uv >/dev/null 2>&1; then
  run_ruff() { uv run --extra dev --python "$PYTHON_BIN" ruff "$@"; }
  run_pytest() { uv run --extra dev --python "$PYTHON_BIN" pytest "$@"; }
  run_python() { uv run --extra dev --python "$PYTHON_BIN" python "$@"; }
  run_agent_memory_isolation() { uv run --extra dev --python "$PYTHON_BIN" agent-memory-isolation "$@"; }
else
  run_ruff() { "$PYTHON_BIN" -m ruff "$@"; }
  run_pytest() { "$PYTHON_BIN" -m pytest "$@"; }
  run_python() { "$PYTHON_BIN" "$@"; }
  run_agent_memory_isolation() { "$PYTHON_BIN" -m agent_memory_isolation "$@"; }
fi

run_ruff check .
run_pytest
run_python -m compileall -q src tests
if ! run_python -m build >"$BUILD_OUT" 2>&1; then
  sed "s#${ROOT}#<repo>#g" "$BUILD_OUT" >&2
  exit 1
fi

WHEEL_PATH="$(find dist -maxdepth 1 -name 'multi_agent_memory_isolation-*-py3-none-any.whl' | sort | tail -n 1)"
if [[ -z "$WHEEL_PATH" ]]; then
  echo "Multi-Agent Memory Isolation prepublish checks expected a built wheel in dist/." >&2
  exit 1
fi

"$PYTHON_BIN" -m venv "$WHEEL_VENV"
"$WHEEL_VENV/bin/python" -m pip install --quiet --no-deps --disable-pip-version-check "$WHEEL_PATH"
"$WHEEL_VENV/bin/agent-memory-isolation" --version >"$WHEEL_OUT"
"$WHEEL_VENV/bin/agent-memory-isolation" --root "$WHEEL_SMOKE_ROOT" init --force >>"$WHEEL_OUT"
"$WHEEL_VENV/bin/agent-memory-isolation" --root "$WHEEL_SMOKE_ROOT" schema --kind shared-memory >/dev/null
"$WHEEL_VENV/bin/agent-memory-isolation" --root "$WHEEL_SMOKE_ROOT" doctor >>"$WHEEL_OUT"

run_agent_memory_isolation --version
run_agent_memory_isolation --root "$SMOKE_ROOT" init --force >"$INIT_OUT"
run_agent_memory_isolation --root "$SMOKE_ROOT" promote \
  --agent codex \
  --kind fact \
  --text "Multi-Agent Memory Isolation keeps shared memory evidence-gated." \
  --evidence "prepublish smoke"
run_agent_memory_isolation --root "$SMOKE_ROOT" handoff \
  --agent codex \
  --task "Prepublish smoke" \
  --output "$SMOKE_ROOT/handoff.md" >"$HANDOFF_OUT"
run_agent_memory_isolation --root "$SMOKE_ROOT" schema \
  --kind shared-memory \
  --output "$SMOKE_ROOT/schema.json" >"$SCHEMA_OUT"
run_agent_memory_isolation --root "$SMOKE_ROOT" status --format json >"$STATUS_OUT"
run_agent_memory_isolation --root "$SMOKE_ROOT" doctor --format json >"$DOCTOR_OUT"

if run_agent_memory_isolation --root "$SMOKE_ROOT/uninitialized" note \
  --agent codex \
  --text "prepublish privacy smoke" >/dev/null 2>"$NOTE_ERR"; then
  echo "Multi-Agent Memory Isolation prepublish checks expected note-before-init to fail." >&2
  exit 1
fi

run_python - "$STATUS_OUT" "$DOCTOR_OUT" <<'PY'
import json
import sys

for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as handle:
        payload = json.load(handle)
    if payload.get("root") != ".":
        raise SystemExit(f"unexpected root field in {path}: {payload.get('root')!r}")
    if payload.get("context_dir") != ".agent-memory":
        raise SystemExit(f"unexpected context_dir field in {path}: {payload.get('context_dir')!r}")
PY

if contains_fixed "$SMOKE_ROOT" "$INIT_OUT" "$HANDOFF_OUT" "$SCHEMA_OUT" "$STATUS_OUT" "$DOCTOR_OUT" "$NOTE_ERR"; then
  echo "Multi-Agent Memory Isolation prepublish privacy smoke failed: absolute local root leaked into command output." >&2
  exit 1
fi

if contains_fixed "$WHEEL_SMOKE_ROOT" "$WHEEL_OUT"; then
  echo "Multi-Agent Memory Isolation prepublish wheel smoke failed: absolute local root leaked into wheel command output." >&2
  exit 1
fi

if ! contains_fixed "Multi-Agent Memory Isolation is not initialized in this repository. Run: agent-memory-isolation init" "$NOTE_ERR"; then
  echo "Multi-Agent Memory Isolation prepublish privacy smoke failed: unexpected note-before-init error." >&2
  exit 1
fi

echo "Multi-Agent Memory Isolation prepublish checks passed."
