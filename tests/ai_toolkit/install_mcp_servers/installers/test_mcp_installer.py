import pytest

from ai_toolkit.install_mcp_servers.installers.mcp_installer import McpInstaller


class TestMcpInstaller:
    @pytest.mark.unit
    def test_protocol_when_class_implements_install_then_is_subtype(self) -> None:
        class ConcreteInstaller:
            def install(self, server: object) -> bool:
                return True

        installer: McpInstaller = ConcreteInstaller()
        assert installer.install(object()) is True
