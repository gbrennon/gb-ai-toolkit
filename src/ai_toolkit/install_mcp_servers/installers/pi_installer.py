import subprocess

from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.shell import shell_command_exists


class PiMcpInstaller:
    def __init__(self, platform: str = AgentPlatform.PI) -> None:
        self.platform = platform

    def install(self, server: McpServerDef) -> bool:
        if self.platform == AgentPlatform.PI:
            if not shell_command_exists("pi-install"):
                print(
                    f"MCP server '{server.name}' requires 'pi-install' "
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
            print(f"Installing MCP server '{server.name}' via pi-install: {pkg}")

            result = subprocess.run(
                ["pi-install", "--arm", pkg],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if result.returncode != 0:
                print(f"MCP server '{server.name}': pi-install failed")
                return False

            print(f"MCP server '{server.name}': installed")
            return True
        else:
            print(
                f"MCP server '{server.name}': platform is '{self.platform}', "
                f"skipping pi install"
            )
            return True
