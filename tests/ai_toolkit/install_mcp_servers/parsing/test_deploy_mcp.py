import json
from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.parsing.deploy_mcp import deploy_mcp


class TestDeployMcp:
    @pytest.mark.unit
    def test_deploy_when_source_missing_then_returns_false(
        self,
        tmp_path: Path,
    ) -> None:
        missing = tmp_path / "nope.json"
        result = deploy_mcp(missing, tmp_path / "out.json")
        assert result is False

    @pytest.mark.unit
    def test_deploy_when_no_secrets_then_writes_identical(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text('{"mcpServers": {"a": {"command": "npx"}}}')
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        assert target.exists()
        written = json.loads(target.read_text())
        assert written == {"mcpServers": {"a": {"command": "npx"}}}

    @pytest.mark.unit
    def test_deploy_when_env_placeholder_resolved_from_dotenv_then_writes_real(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("MY_TOKEN", raising=False)
        source = tmp_path / "mcp.json"
        source.write_text('{"mcpServers":{"srv":{"env":{"MY_TOKEN":"{{ MY_TOKEN or \'YOUR_TOKEN_HERE\' }}"}}}}')
        dotenv = tmp_path / ".env"
        dotenv.write_text("MY_TOKEN=real_value\n")
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target, dotenv_path=dotenv)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["MY_TOKEN"] == "real_value"

    @pytest.mark.unit
    def test_deploy_when_env_placeholder_resolved_from_environ_then_writes_real(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("MY_TOKEN", "from_environ")
        source = tmp_path / "mcp.json"
        source.write_text('{"mcpServers":{"srv":{"env":{"MY_TOKEN":"{{ MY_TOKEN or \'PLACEHOLDER\' }}"}}}}')
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target, dotenv_path=None)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["MY_TOKEN"] == "from_environ"

    @pytest.mark.unit
    def test_deploy_when_env_already_real_then_keeps_it(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text('{"mcpServers":{"srv":{"env":{"KEY":"already_real"}}}}')
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["env"]["KEY"] == "already_real"

    @pytest.mark.unit
    def test_deploy_when_header_placeholder_resolved_from_environ(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setenv("GITHUB_TOKEN", "ghp_real")
        source = tmp_path / "mcp.json"
        source.write_text(
            '{"mcpServers":{"github":{"headers":{' +
            '"Authorization":"Bearer {{ GITHUB_TOKEN or \'YOUR_GITHUB_TOKEN_HERE\' }}"}}}}'
        )
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert (
            written["mcpServers"]["github"]["headers"]["Authorization"]
            == "Bearer ghp_real"
        )

    @pytest.mark.unit
    def test_deploy_when_header_placeholder_unresolved_then_keeps_fallback(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
        source = tmp_path / "mcp.json"
        source.write_text(
            '{"mcpServers":{"github":{"headers":{' +
            '"Authorization":"Bearer {{ GITHUB_TOKEN or \'YOUR_GITHUB_TOKEN_HERE\' }}"}}}}'
        )
        target = tmp_path / "out.json"

        result = deploy_mcp(source, target)
        assert result is True
        written = json.loads(target.read_text())
        assert (
            written["mcpServers"]["github"]["headers"]["Authorization"]
            == "Bearer YOUR_GITHUB_TOKEN_HERE"
        )

    @pytest.mark.unit
    def test_deploy_preserves_extra_fields(
        self,
        tmp_path: Path,
    ) -> None:
        source = tmp_path / "mcp.json"
        source.write_text(
            '{"mcpServers":{"srv":{"command":"npx","autoApprove":[],"disabled":false}}}'
        )
        target = tmp_path / "out.json"

        deploy_mcp(source, target)
        written = json.loads(target.read_text())
        assert written["mcpServers"]["srv"]["autoApprove"] == []
        assert written["mcpServers"]["srv"]["disabled"] is False

    # ---- multi-agent deployment tests ----

    @pytest.mark.unit
    def test_agent_targets_filters_servers_by_platform(
        self,
        tmp_path: Path,
    ) -> None:
        from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform

        source = tmp_path / "mcp.json"
        source.write_text(
            '{"mcpServers":{'
            '"shared":{"command":"npx","args":["shared-pkg"]},'
            '"oc-srv":{"command":"npx","args":["oc-pkg"],"platform":"opencode"},'
            '"pi-srv":{"command":"npx","args":["pi-pkg"],"platform":"pi"}'
            '}}'
        )
        primary = tmp_path / "cline.json"
        oc_target = tmp_path / "opencode.json"
        pi_target = tmp_path / "pi.json"

        result = deploy_mcp(
            source,
            primary,
            agent_targets={AgentPlatform.OPENCODE: oc_target, AgentPlatform.PI: pi_target},
        )
        assert result is True

        # Primary target gets everything
        primary_data = json.loads(primary.read_text())
        assert set(primary_data["mcpServers"].keys()) == {"shared", "oc-srv", "pi-srv"}

        # OpenCode target gets shared + opencode-only
        oc_data = json.loads(oc_target.read_text())
        assert set(oc_data["mcpServers"].keys()) == {"shared", "oc-srv"}

        # Pi target gets shared + pi-only
        pi_data = json.loads(pi_target.read_text())
        assert set(pi_data["mcpServers"].keys()) == {"shared", "pi-srv"}

    @pytest.mark.unit
    def test_agent_targets_when_no_platforms_then_all_get_same_servers(
        self,
        tmp_path: Path,
    ) -> None:
        from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform

        source = tmp_path / "mcp.json"
        source.write_text(
            '{"mcpServers":{"a":{"command":"npx","args":["a"]},"b":{"command":"npx","args":["b"]}}}'
        )
        primary = tmp_path / "cline.json"
        oc_target = tmp_path / "opencode.json"

        result = deploy_mcp(
            source,
            primary,
            agent_targets={AgentPlatform.OPENCODE: oc_target},
        )
        assert result is True

        oc_data = json.loads(oc_target.read_text())
        assert set(oc_data["mcpServers"].keys()) == {"a", "b"}

    @pytest.mark.unit
    def test_agent_targets_preserves_root_keys(
        self,
        tmp_path: Path,
    ) -> None:
        from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform

        source = tmp_path / "mcp.json"
        source.write_text(
            '{"other": "data", "mcpServers":{"srv":{"command":"npx","args":["pkg"],"platform":"opencode"}}}'
        )
        primary = tmp_path / "cline.json"
        oc_target = tmp_path / "opencode.json"

        result = deploy_mcp(
            source,
            primary,
            agent_targets={AgentPlatform.OPENCODE: oc_target},
        )
        assert result is True

        oc_data = json.loads(oc_target.read_text())
        assert oc_data["other"] == "data"
        assert "srv" in oc_data["mcpServers"]

