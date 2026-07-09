from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.shell import shell_command_exists


class CommandMcpInstaller:
    def install(self, server: McpServerDef) -> bool:
        if not server.command:
            print(f"MCP server '{server.name}' has no command — skipping")
            return False

        if not shell_command_exists(server.command):
            print(
                f"MCP server '{server.name}' requires '{server.command}' "
                f"which is not on PATH"
            )
            return False

        print(f"MCP server '{server.name}': command '{server.command}' found on PATH")
        return True
