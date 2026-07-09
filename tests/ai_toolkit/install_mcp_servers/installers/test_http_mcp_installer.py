from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.http_mcp_installer import (
    HttpMcpInstaller,
)


def _with_env(base, env):
    return McpServerDef(
        name=base.name, command=base.command, args=base.args,
        env=env, server_type=base.server_type, url=base.url,
        disabled=base.disabled,
    )


class TestHttpMcpInstaller:
    @pytest.mark.unit
    def test_install_when_no_env_then_returns_true(self, http_server):
        installer = HttpMcpInstaller(dotenv_path=None)
        result = installer.install(http_server)
        assert result is True

    @pytest.mark.unit
    def test_install_when_env_in_environ_then_returns_true(self, http_server, monkeypatch):
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_real_value")
        installer = HttpMcpInstaller(dotenv_path=None)
        server = _with_env(http_server, (("GITHUB_TOKEN", "PLACEHOLDER"),))
        result = installer.install(server)
        assert result is True

    @pytest.mark.unit
    def test_install_when_env_in_dotenv_then_returns_true(self, http_server, tmp_path, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        dotenv = tmp_path / ".env"
        dotenv.write_text("GITHUB_TOKEN=ghp_real_value\n")
        installer = HttpMcpInstaller(dotenv_path=dotenv)
        server = _with_env(http_server, (("GITHUB_TOKEN", "PLACEHOLDER"),))
        result = installer.install(server)
        assert result is True

    @pytest.mark.unit
    def test_install_when_env_placeholder_then_returns_true(self, http_server, monkeypatch):
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        installer = HttpMcpInstaller(dotenv_path=None)
        server = _with_env(http_server, (("GITHUB_TOKEN", "YOUR_GITHUB_TOKEN_HERE"),))
        result = installer.install(server)
        assert result is True
