from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


class FakeMcpInstaller:
    def __init__(self) -> None:
        self.installed: list[McpServerDef] = []
        self.fail_on: list[str] = []
        self.skipped: list[str] = []

    def install(self, server: McpServerDef) -> bool:
        self.installed.append(server)
        if server.name in self.fail_on:
            return False
        return True
