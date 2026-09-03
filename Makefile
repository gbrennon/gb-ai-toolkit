.DEFAULT_GOAL := help

PYTHON      := .venv/bin/python
UV          := uv
MCP_JSON    := mcp/mcp.json
DOTENV      := .env
TARGET_PATH := $(HOME)/.cline/data/settings/cline_mcp_settings.json

# ── Auto-generated help ─────────────────────────────────────────────────────
help:  ## Show this help
	@awk -F ':.*?## ' '/^[a-zA-Z0-9_-]+:.*?## / {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST) | sort
	@echo ""
	@echo "  make install   runs all install targets"

# ── Setup ────────────────────────────────────────────────────────────────────
setup:  ## Install dependencies (uv sync)
	$(UV) sync

# ── Install ──────────────────────────────────────────────────────────────────
install-mcp:  ## Install & deploy MCP servers
	$(UV) run install-mcp-servers

install-skills:  ## Install skills
	$(UV) run install-skills

install-agent-rules:  ## Compose agent_rules/ into manifest-listed AGENTS.md targets
	$(UV) run install-agent-rules

install-omp-commands:  ## Install OMP Cline auth commands & scripts
	$(UV) run install-omp-commands

install-provider-blocks:  ## Block OpenAI & Anthropic access on OMP + Cline
	$(UV) run install-provider-blocks

install: install-skills install-agent-rules install-omp-commands install-provider-blocks  ## Run all install targets

# ── Pi Config ────────────────────────────────────────────────────────────────
install-pi-config:  ## Sync CLINE_API_KEY from .env into Pi + OpenCode
	$(UV) run install-pi-config

# ── Deploy ───────────────────────────────────────────────────────────────────
deploy-mcp:  ## Alias for install-mcp
	$(UV) run install-mcp-servers

# ── Systemd ──────────────────────────────────────────────────────────────────
install-systemd:  ## Install systemd user services & timers
	bash scripts/install-systemd.sh

uninstall-systemd:  ## Remove systemd user services & timers
	-systemctl --user disable --now gb-mcp-servers.timer 2>/dev/null
	-systemctl --user disable --now gb-skills.timer 2>/dev/null
	-rm -f $(HOME)/.config/systemd/user/gb-mcp-servers.*
	-rm -f $(HOME)/.config/systemd/user/gb-skills.*
	systemctl --user daemon-reload

install-aliases:  ## Install shell aliases for CLI commands
	bash scripts/install-aliases.sh

# ── Test ─────────────────────────────────────────────────────────────────────
test:  ## Run all tests
	$(UV) run pytest tests/ --tb=short

test-unit:  ## Run unit tests only
	$(UV) run pytest tests/ -m unit --tb=short

# ── Clean ────────────────────────────────────────────────────────────────────
clean:  ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info/
