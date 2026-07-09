from typing import Protocol

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


class McpInstaller(Protocol):
    def install(self, server: McpServerDef) -> bool: ...
