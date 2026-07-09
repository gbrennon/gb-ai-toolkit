import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.opencode_installer import (
    OpenCodeMcpInstaller,
)


class TestOpenCodeMcpInstaller:
    @pytest.mark.unit
    def test_when_wrong_platform_then_skips(self, npx_server: McpServerDef) -> None:
        installer = OpenCodeMcpInstaller(platform="linux")
        result = installer.install(npx_server)
        assert result is True

    @pytest.mark.unit
    def test_when_opencode_not_on_path_then_false(
        self, npx_server: McpServerDef,
    ) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which", return_value=None):
            installer = OpenCodeMcpInstaller(platform=AgentPlatform.OPENCODE)
            result = installer.install(npx_server)
            assert result is False

    @pytest.mark.unit
    def test_when_package_resolves_then_true(
        self, npx_server: McpServerDef,
    ) -> None:
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/opencode"),
            patch("ai_toolkit.install_mcp_servers.installers.opencode_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 0
            installer = OpenCodeMcpInstaller(platform=AgentPlatform.OPENCODE)
            result = installer.install(npx_server)
            assert result is True
            mock_run.assert_called_once_with(
                ["opencode", "install", "pkg"],
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
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/opencode"),
            patch("ai_toolkit.install_mcp_servers.installers.opencode_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 1
            installer = OpenCodeMcpInstaller(platform=AgentPlatform.OPENCODE)
            result = installer.install(server)
            assert result is False
