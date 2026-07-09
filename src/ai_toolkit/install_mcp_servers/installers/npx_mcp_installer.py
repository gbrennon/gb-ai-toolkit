import subprocess

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.shell import shell_command_exists


class NpxMcpInstaller:
    def __init__(self, npx_command: str | None = None) -> None:
        self._npx_command = npx_command or "npx"

    def install(self, server: McpServerDef) -> bool:
        if not shell_command_exists(self._npx_command):
            print(
                f"MCP server '{server.name}' requires '{self._npx_command}' "
                f"which is not on PATH"
            )
            return False

        non_flag_args = [a for a in server.args if not a.startswith("-")]
        if not non_flag_args:
            print(
                f"MCP server '{server.name}': no package name found "
                f"in args {server.args}"
            )
            return False

        pkg = non_flag_args[0]
        print(f"Installing MCP server '{server.name}' via npx: {pkg}")

        try:
            subprocess.run(
                [self._npx_command, "--force", "--package", pkg, "--", "true"],
                check=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except subprocess.CalledProcessError:
            print(f"MCP server '{server.name}': npx install failed")
            return False

        print(f"MCP server '{server.name}': installed")
        return True
