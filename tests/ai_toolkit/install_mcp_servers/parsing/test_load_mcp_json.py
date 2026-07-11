from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.parsing.load_mcp_json import load_mcp_json


class TestLoadMcpJson:
    @pytest.mark.unit
    def test_load_when_json_has_servers_then_returns_list(
        self,
        sample_mcp_json: Path,
    ) -> None:
        servers = load_mcp_json(sample_mcp_json)
        assert len(servers) == 4
        names = {s.name for s in servers}
        assert names == {"github", "memory", "fetch", "forgejo"}

    @pytest.mark.unit
    def test_load_when_json_has_npx_server_then_parses_correctly(
        self,
        sample_mcp_json: Path,
    ) -> None:
        servers = load_mcp_json(sample_mcp_json)
        memory = next(s for s in servers if s.name == "memory")
        assert memory.command == "npx"
        assert memory.args == ("-y", "@modelcontextprotocol/server-memory")
        assert memory.env == ()
        assert memory.server_type is None
        assert memory.url is None
        assert memory.disabled is False

    @pytest.mark.unit
    def test_load_when_json_has_uvx_server_then_parses_correctly(
        self,
        sample_mcp_json: Path,
    ) -> None:
        servers = load_mcp_json(sample_mcp_json)
        fetch = next(s for s in servers if s.name == "fetch")
        assert fetch.command == "uvx"
        assert fetch.args == ("mcp-server-fetch",)

    @pytest.mark.unit
    def test_load_when_json_has_http_server_then_parses_correctly(
        self,
        sample_mcp_json: Path,
    ) -> None:
        servers = load_mcp_json(sample_mcp_json)
        github = next(s for s in servers if s.name == "github")
        assert github.server_type == "streamableHttp"
        assert github.url == "https://api.githubcopilot.com/mcp/"
        assert github.command is None

    @pytest.mark.unit
    def test_load_when_json_has_server_with_env_then_parses_correctly(
        self,
        sample_mcp_json: Path,
    ) -> None:
        servers = load_mcp_json(sample_mcp_json)
        forgejo = next(s for s in servers if s.name == "forgejo")
        assert forgejo.command == "forgejo-mcp"
        assert forgejo.env == (("FORGEJO_ACCESS_TOKEN", "YOUR_CODEBERG_TOKEN_HERE"),)

    @pytest.mark.unit
    def test_load_when_json_empty_then_returns_empty_list(self, tmp_path: Path) -> None:
        p = tmp_path / "mcp.json"
        p.write_text('{"mcpServers": {}}')
        servers = load_mcp_json(p)
        assert servers == []

    @pytest.mark.unit
    def test_load_when_json_missing_mcp_servers_key_then_returns_empty_list(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / "mcp.json"
        p.write_text('{"other": "data"}')
        servers = load_mcp_json(p)
        assert servers == []

    @pytest.mark.unit
    def test_load_when_server_has_disabled_true_then_flag_is_set(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / "mcp.json"
        p.write_text(
            '{"mcpServers": {"off": {"command": "npx", '
            '"args": ["pkg"], "disabled": true}}}'
        )
        servers = load_mcp_json(p)
        assert servers[0].disabled is True

    @pytest.mark.unit
    def test_load_when_server_has_platform_then_parses_correctly(
        self,
        tmp_path: Path,
    ) -> None:
        from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform

        p = tmp_path / "mcp.json"
        p.write_text(
            '{"mcpServers": {"oc": {"command": "npx", '
            '"args": ["pkg"], "platform": "opencode"}}}'
        )
        servers = load_mcp_json(p)
        assert servers[0].platform == AgentPlatform.OPENCODE

    @pytest.mark.unit
    def test_load_when_server_has_no_platform_then_defaults_to_none(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / "mcp.json"
        p.write_text('{"mcpServers": {"srv": {"command": "npx", "args": ["pkg"]}}}')
        servers = load_mcp_json(p)
        assert servers[0].platform is None
