.PHONY: setup install-mcp install-skills install-pi-config install test test-unit deploy-mcp clean help \
        install-systemd uninstall-systemd install-aliases

PYTHON      := .venv/bin/python
UV          := uv
MCP_JSON    := mcp/mcp.json
DOTENV      := .env
TARGET_PATH := $(HOME)/.cline/data/settings/cline_mcp_settings.json

# -------------------------------------------------------------------
# Setup
# -------------------------------------------------------------------
setup:
	$(UV) sync

# -------------------------------------------------------------------
# Install
# -------------------------------------------------------------------
install-mcp:
	$(UV) run install-mcp-servers

install-skills:
	$(UV) run install-skills

install: install-mcp install-skills

# -------------------------------------------------------------------
# Pi Config
# -------------------------------------------------------------------
install-pi-config:
	$(UV) run install-pi-config

# -------------------------------------------------------------------
# Deploy
# -------------------------------------------------------------------
deploy-mcp:
	$(UV) run install-mcp-servers

# -------------------------------------------------------------------
# Systemd (installed mode — requires `uv tool install .` first)
# -------------------------------------------------------------------
install-systemd:
	bash scripts/install-systemd.sh

uninstall-systemd:
	-systemctl --user disable --now gb-mcp-servers.timer 2>/dev/null
	-systemctl --user disable --now gb-skills.timer 2>/dev/null
	-rm -f $(HOME)/.config/systemd/user/gb-mcp-servers.*
	-rm -f $(HOME)/.config/systemd/user/gb-skills.*
	systemctl --user daemon-reload

install-aliases:
	bash scripts/install-aliases.sh

# -------------------------------------------------------------------
# Test
# -------------------------------------------------------------------
test:
	$(UV) run pytest tests/ --tb=short

test-unit:
	$(UV) run pytest tests/ -m unit --tb=short

# -------------------------------------------------------------------
# Clean
# -------------------------------------------------------------------
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.pyc' -delete 2>/dev/null || true
	find . -type d -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage htmlcov/ dist/ build/ *.egg-info/

# -------------------------------------------------------------------
# Help
# -------------------------------------------------------------------
help:
	@echo "Usage: make <target>"
	@echo ""
	@echo "  setup             Install dependencies (uv sync)"
	@echo "  install-mcp       Install & deploy MCP servers (dev mode — uv run)"
	@echo "  install-skills    Install skills (dev mode — uv run)"
	@echo "  install           Install everything (mcp + skills)"
	@echo "  install-pi-config Sync CLINE_API_KEY from .env to Pi's auth.json"
	@echo "  deploy-mcp        Same as install-mcp"
	@echo "  install-systemd   Install systemd user services & timers (installed mode)"
	@echo "  uninstall-systemd Remove systemd user services & timers"
	@echo "  install-aliases   Install shell aliases for CLI commands"
	@echo "  test              Run all tests"
	@echo "  test-unit         Run unit tests only"
	@echo "  clean             Remove build artifacts and caches"
