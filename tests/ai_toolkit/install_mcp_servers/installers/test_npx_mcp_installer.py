import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.npx_mcp_installer import (
    NpxMcpInstaller,
)


class TestNpxMcpInstaller:
    @pytest.mark.unit
    def test_install_when_package_resolves_then_returns_true(
        self, npx_server: McpServerDef,
    ) -> None:
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/npx"),
            patch("ai_toolkit.install_mcp_servers.installers.npx_mcp_installer.subprocess.run") as mock_run,
        ):
            installer = NpxMcpInstaller()
            result = installer.install(npx_server)
            assert result is True
            mock_run.assert_called_once_with(
                ["npx", "--force", "--package", "pkg", "--", "true"],
                check=True, stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_install_when_npx_not_on_path_then_returns_false(
        self, npx_server: McpServerDef,
    ) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which", return_value=None):
            installer = NpxMcpInstaller()
            result = installer.install(npx_server)
            assert result is False

    @pytest.mark.unit
    def test_install_when_package_fails_then_returns_false(self) -> None:
        server = McpServerDef(
            name="test", command="npx", args=("broken",), env=(),
            server_type=None, url=None, disabled=False,
        )
        with (
            patch("ai_toolkit.shared_kernel.shell.which", return_value="/usr/bin/npx"),
            patch("ai_toolkit.install_mcp_servers.installers.npx_mcp_installer.subprocess.run") as mock_run,
        ):
            mock_run.side_effect = subprocess.CalledProcessError(
                1, ["npx", "--force", "--package", "broken", "--", "true"],
            )
            installer = NpxMcpInstaller()
            result = installer.install(server)
            assert result is False
