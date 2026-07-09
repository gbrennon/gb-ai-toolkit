import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.uvx_mcp_installer import (
    UvxMcpInstaller,
)


class TestUvxMcpInstaller:
    @pytest.mark.unit
    def test_install_when_package_resolves_then_returns_true(
        self, uvx_server: McpServerDef,
    ) -> None:
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/uvx"),
            patch("ai_toolkit.install_mcp_servers.installers.uvx_mcp_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 0
            installer = UvxMcpInstaller()
            result = installer.install(uvx_server)
            assert result is True
            mock_run.assert_called_once_with(
                ["uvx", "--reinstall", "--quiet", "mcp-server-fetch", "--help"],
                check=False, stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_install_when_uvx_not_on_path_then_returns_false(
        self, uvx_server: McpServerDef,
    ) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which", return_value=None):
            installer = UvxMcpInstaller()
            result = installer.install(uvx_server)
            assert result is False

    @pytest.mark.unit
    def test_install_when_package_fails_then_returns_false(
        self, uvx_server: McpServerDef,
    ) -> None:
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/uvx"),
            patch("ai_toolkit.install_mcp_servers.installers.uvx_mcp_installer.subprocess.run") as mock_run,
        ):
            mock_run.return_value.returncode = 1
            installer = UvxMcpInstaller()
            result = installer.install(uvx_server)
            assert result is False
