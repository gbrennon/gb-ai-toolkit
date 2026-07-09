import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.vibe_installer import VibeMcpInstaller


class TestVibeMcpInstaller:
    @pytest.mark.unit
    def test_when_wrong_platform_then_skips(self, npx_server: McpServerDef) -> None:
        installer = VibeMcpInstaller(platform="linux")
        result = installer.install(npx_server)
        assert result is True

    @pytest.mark.unit
    def test_when_vibe_install_not_on_path_then_false(
        self, npx_server: McpServerDef,
    ) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which", return_value=None):
            installer = VibeMcpInstaller(platform=AgentPlatform.VIBE)
            result = installer.install(npx_server)
            assert result is False

    @pytest.mark.unit
    def test_when_package_resolves_then_true(
        self, npx_server: McpServerDef,
    ) -> None:
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/vibe-install"),
            patch("ai_toolkit.install_mcp_servers.installers.vibe_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 0
            installer = VibeMcpInstaller(platform=AgentPlatform.VIBE)
            result = installer.install(npx_server)
            assert result is True
            mock_run.assert_called_once_with(
                ["vibe-install", "--resolve", "pkg"],
                check=False, stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_when_package_fails_then_false(self) -> None:
        server = McpServerDef(
            name="test", command="npx", args=("broken",), env=(),
            server_type=None, url=None, disabled=False,
        )
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/vibe-install"),
            patch("ai_toolkit.install_mcp_servers.installers.vibe_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 1
            installer = VibeMcpInstaller(platform=AgentPlatform.VIBE)
            result = installer.install(server)
            assert result is False
