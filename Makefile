.PHONY: test lint format-check compile privacy package prepublish smoke

PYTHON ?= $(shell for candidate in python python3 python3.12 python3.11 python3.10; do \
	if command -v $$candidate >/dev/null 2>&1 && $$candidate -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)' >/dev/null 2>&1; then \
		command -v $$candidate; \
		break; \
	fi; \
done)
UV := $(shell command -v uv 2>/dev/null)
SMOKE_ROOT := $(shell mktemp -d /tmp/agent-memory-isolation-smoke.XXXXXX)

ifeq ($(strip $(UV)),)
RUFF = $(PYTHON) -m ruff
PYTEST = $(PYTHON) -m pytest
PYTHON_RUN = $(PYTHON)
AGENT_MEMORY = $(PYTHON) -m agent_memory_isolation
BUILD = $(PYTHON) -m build
else
RUN_DEV = $(UV) run --extra dev --python $(PYTHON)
RUFF = $(RUN_DEV) ruff
PYTEST = $(RUN_DEV) pytest
PYTHON_RUN = $(RUN_DEV) python
AGENT_MEMORY = $(RUN_DEV) agent-memory-isolation
BUILD = $(RUN_DEV) python -m build
endif

test:
	@$(PYTEST)

lint:
	@$(RUFF) check .

format-check:
	@$(RUFF) format --check .

compile:
	@$(PYTHON_RUN) -m compileall -q src tests

privacy:
	@bash scripts/privacy_check.sh

package:
	@if $(BUILD) >$(SMOKE_ROOT)/build.log 2>&1; then \
		if $(PYTHON_RUN) -m twine check dist/* >$(SMOKE_ROOT)/twine.log 2>&1; then \
			echo "package build passed"; \
		else \
			sed "s#$(CURDIR)#<repo>#g" $(SMOKE_ROOT)/twine.log >&2; \
			exit 1; \
		fi; \
	else \
		sed "s#$(CURDIR)#<repo>#g" $(SMOKE_ROOT)/build.log >&2; \
		exit 1; \
	fi

smoke:
	@$(AGENT_MEMORY) --version
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) init --force
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) note --agent codex --text "Private draft note"
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) promote --agent codex --kind decision --text "Use evidence-gated shared memory" --evidence "operator-approved policy"
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) handoff --agent codex --task "Continue safely" --output $(SMOKE_ROOT)/handoff.md
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) schema --kind shared-memory >/tmp/agent-memory-isolation-schema-smoke.json
	@$(AGENT_MEMORY) --root $(SMOKE_ROOT) doctor

prepublish: lint format-check test compile privacy smoke package
