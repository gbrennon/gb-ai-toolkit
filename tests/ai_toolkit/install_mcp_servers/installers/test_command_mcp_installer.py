from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.install_mcp_servers.installers.command_mcp_installer import (
    CommandMcpInstaller,
)


class TestCommandMcpInstaller:
    @pytest.mark.unit
    def test_command_install_when_command_exists_then_returns_true(self) -> None:
        with patch(
            "ai_toolkit.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = "/usr/bin/forgejo-mcp"
            installer = CommandMcpInstaller()
            server = McpServerDef(
                name="forgejo",
                command="forgejo-mcp",
                args=("--transport", "stdio"),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is True
            mock_which.assert_called_once_with("forgejo-mcp")

    @pytest.mark.unit
    def test_command_install_when_command_missing_then_returns_false(self) -> None:
        with patch(
            "ai_toolkit.shared_kernel.shell.which"
        ) as mock_which:
            mock_which.return_value = None
            installer = CommandMcpInstaller()
            server = McpServerDef(
                name="missing-cmd",
                command="no-such-command",
                args=(),
                env=(),
                server_type=None,
                url=None,
                disabled=False,
            )
            result = installer.install(server)
            assert result is False
