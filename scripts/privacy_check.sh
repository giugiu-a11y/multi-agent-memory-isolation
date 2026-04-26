#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

RG_BIN="$(command -v rg || true)"
GITLEAKS_BIN="$(command -v gitleaks || true)"

SOURCE_GLOBS=(
  --hidden
  --glob '!.git/**'
  --glob '!.venv/**'
  --glob '!dist/**'
  --glob '!build/**'
  --glob '!*.egg-info/**'
  --glob '!__pycache__/**'
  --glob '!.pytest_cache/**'
  --glob '!.ruff_cache/**'
  --glob '!.agent-memory/**'
  --glob '!scripts/privacy_check.sh'
)

PRIVATE_SURFACE_PATTERN='(/Users/|/home/[^[:space:]/]+/|C:\\Users\\|[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}|BEGIN ((RSA|OPENSSH|EC|DSA) )?PRIVATE KEY|api[_-]?key|secret[_-]?key|access[_-]?token|refresh[_-]?token|auth[_-]?token|client[_-]?secret|password[=:]|passwd[=:])'

if [[ -n "${RG_BIN}" ]]; then
  SCAN_CMD=("${RG_BIN}" -n -i "${SOURCE_GLOBS[@]}" "${PRIVATE_SURFACE_PATTERN}" "${ROOT_DIR}")
else
  SCAN_CMD=(
    grep -RInE
    --exclude-dir=.git
    --exclude-dir=.venv
    --exclude-dir=dist
    --exclude-dir=build
    --exclude-dir=__pycache__
    --exclude-dir=.pytest_cache
    --exclude-dir=.ruff_cache
    --exclude-dir=.agent-memory
    --exclude='*.egg-info'
    --exclude='privacy_check.sh'
    "${PRIVATE_SURFACE_PATTERN}"
    "${ROOT_DIR}"
  )
fi

set +e
"${SCAN_CMD[@]}"
SCAN_STATUS=$?
set -e

if [[ "${SCAN_STATUS}" -eq 0 ]]; then
  echo "Privacy check failed: public-facing files contain sensitive-looking content." >&2
  exit 1
elif [[ "${SCAN_STATUS}" -gt 1 ]]; then
  echo "Privacy check failed: scanner returned status ${SCAN_STATUS}." >&2
  exit 1
fi

if [[ -n "${GITLEAKS_BIN}" ]]; then
  "${GITLEAKS_BIN}" detect --source "${ROOT_DIR}" --redact
else
  echo "gitleaks not found; skipped secret detector."
fi

echo "Multi-Agent Memory Isolation privacy checks passed."
