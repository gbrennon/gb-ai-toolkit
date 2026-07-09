import pytest

from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.install_mcp import install_mcp
from tests.ai_toolkit.install_mcp_servers.fakes import FakeMcpInstaller


def _make_server(name, command="npx", server_type=None, platform=None):
    server = McpServerDef(
        name=name, command=command,
        args=("-y", "pkg") if command else (), env=(),
        server_type=server_type,
        url="https://example.com" if server_type == "streamableHttp" else None,
        disabled=False,
        platform=platform,
    )
    return server


class TestInstallMcp:
    @pytest.mark.unit
    def test_when_all_succeed_then_empty(self, fake_installer):
        servers = [_make_server("a"), _make_server("b")]
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, servers)
        assert failed == []
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_when_some_fail_then_failed_list(self, fake_installer):
        fake_installer.fail_on = ["b"]
        servers = [_make_server("a"), _make_server("b")]
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, servers)
        assert failed == ["b"]

    @pytest.mark.unit
    def test_when_empty_then_empty(self, fake_installer):
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, [])
        assert failed == []

    @pytest.mark.unit
    def test_when_disabled_then_skips(self, fake_installer):
        enabled = _make_server("enabled")
        disabled = McpServerDef(name="disabled", command="npx", args=("-y", "pkg"), env=(), server_type=None, url=None, disabled=True)
        failed = install_mcp(fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, fake_installer, [enabled, disabled])
        assert failed == []
        assert fake_installer.installed == [enabled]

    @pytest.mark.unit
    def test_routes_npx(self, fake_installer):
        servers = [_make_server("npx-server", command="npx")]
        noop = FakeMcpInstaller()
        install_mcp(fake_installer, noop, noop, noop, noop, noop, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_uvx(self, fake_installer):
        servers = [_make_server("uvx-server", command="uvx")]
        noop = FakeMcpInstaller()
        install_mcp(noop, fake_installer, noop, noop, noop, noop, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_custom_command(self, fake_installer):
        servers = [_make_server("custom", command="forgejo-mcp")]
        noop = FakeMcpInstaller()
        install_mcp(noop, noop, fake_installer, noop, noop, noop, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_http(self, fake_installer):
        servers = [_make_server("github", command=None, server_type="streamableHttp")]
        noop = FakeMcpInstaller()
        install_mcp(noop, noop, noop, fake_installer, noop, noop, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_opencode_platform(self, fake_installer):
        servers = [_make_server("oc", command="npx", platform=AgentPlatform.OPENCODE)]
        noop = FakeMcpInstaller()
        install_mcp(noop, noop, noop, noop, fake_installer, noop, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_pi_platform(self, fake_installer):
        servers = [_make_server("pi", command="npx", platform=AgentPlatform.PI)]
        noop = FakeMcpInstaller()
        install_mcp(noop, noop, noop, noop, noop, fake_installer, noop, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_routes_vibe_platform(self, fake_installer):
        servers = [_make_server("vibe", command="npx", platform=AgentPlatform.VIBE)]
        noop = FakeMcpInstaller()
        install_mcp(noop, noop, noop, noop, noop, noop, fake_installer, servers)
        assert fake_installer.installed == servers

    @pytest.mark.unit
    def test_platform_priority_over_command(self, fake_installer):
        servers = [_make_server("oc-npx", command="npx", platform=AgentPlatform.OPENCODE)]
        noop = FakeMcpInstaller()
        npx_installer = FakeMcpInstaller()
        install_mcp(npx_installer, noop, noop, noop, fake_installer, noop, noop, servers)
        assert fake_installer.installed == servers
        assert npx_installer.installed == []
