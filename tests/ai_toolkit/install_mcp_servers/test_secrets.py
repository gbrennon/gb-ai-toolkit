from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.secrets import check_mcp_secrets


def _server(name: str, **env: str) -> McpServerDef:
    return McpServerDef(
        name=name,
        command="npx",
        args=(),
        env=tuple(env.items()),
        server_type=None,
        url=None,
        disabled=False,
    )


class TestCheckMcpSecrets:
    @pytest.mark.unit
    def test_check_when_all_keys_in_dotenv_then_returns_empty(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        dotenv = tmp_path / ".env"
        dotenv.write_text("GITHUB_TOKEN=abc123\n")
        servers = [_server("github", GITHUB_TOKEN="placeholder")]
        missing = check_mcp_secrets(servers, dotenv_path=dotenv)
        assert missing == []

    @pytest.mark.unit
    def test_check_when_all_keys_in_os_environ_then_returns_empty(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("GH_TOKEN", "xyz")
        servers = [_server("gh", GH_TOKEN="placeholder")]
        missing = check_mcp_secrets(servers, dotenv_path=None)
        assert missing == []

    @pytest.mark.unit
    def test_check_when_key_missing_in_both_then_returns_missing(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("MISSING_KEY", raising=False)
        servers = [_server("bad", MISSING_KEY="placeholder")]
        missing = check_mcp_secrets(servers, dotenv_path=None)
        assert missing == ["MISSING_KEY"]

    @pytest.mark.unit
    def test_check_when_os_environ_overrides_dotenv_then_uses_environ(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("TOKEN", "from-os")
        dotenv = tmp_path / ".env"
        dotenv.write_text("TOKEN=from-file\n")
        servers = [_server("srv", TOKEN="placeholder")]
        missing = check_mcp_secrets(servers, dotenv_path=dotenv)
        assert missing == []

    @pytest.mark.unit
    def test_check_when_server_disabled_then_skips(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("UNUSED_TOKEN", raising=False)
        server = McpServerDef(
            name="off",
            command="npx",
            args=(),
            env=(("UNUSED_TOKEN", "placeholder"),),
            server_type=None,
            url=None,
            disabled=True,
        )
        missing = check_mcp_secrets([server], dotenv_path=None)
        assert missing == []

    @pytest.mark.unit
    def test_check_when_no_servers_then_returns_empty(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        missing = check_mcp_secrets([], dotenv_path=None)
        assert missing == []

    @pytest.mark.unit
    def test_check_when_multiple_servers_then_collects_all_missing(
        self,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("A", raising=False)
        monkeypatch.delenv("B", raising=False)
        monkeypatch.setenv("C", "ok")
        servers = [
            _server("s1", A="p1", C="p2"),
            _server("s2", B="p3", C="p4"),
        ]
        missing = check_mcp_secrets(servers, dotenv_path=None)
        assert missing == ["A", "B"]
