import subprocess

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.shell import shell_command_exists


class UvxMcpInstaller:
    def install(self, server: McpServerDef) -> bool:
        if not shell_command_exists("uvx"):
            print(f"MCP server '{server.name}' requires 'uvx' which is not on PATH")
            return False

        non_flag_args = [a for a in server.args if not a.startswith("-")]
        if not non_flag_args:
            print(
                f"MCP server '{server.name}': no package name found "
                f"in args {server.args}"
            )
            return False

        pkg = non_flag_args[0]
        print(f"Installing MCP server '{server.name}' via uvx: {pkg}")

        result = subprocess.run(
            ["uvx", "--reinstall", "--quiet", pkg, "--help"],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode != 0:
            print(f"MCP server '{server.name}': uvx install failed")
            return False

        print(f"MCP server '{server.name}': installed")
        return True
