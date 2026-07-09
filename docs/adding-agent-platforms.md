# Adding a New Agent Platform

This guide walks through adding support for a new agent (e.g., "Claude Code",
"Gemini CLI", etc.) so it can receive MCP server configs and install packages.

## Step 1: Add to `AgentPlatform` enum

**File:** `src/ai_toolkit/install_mcp_servers/models/agent_platform.py`

```python
class AgentPlatform(StrEnum):
    OPENCODE = "opencode"
    PI = "pi"
    VIBE = "vibe"
    MY_AGENT = "my-agent"            # <-- add

    @property
    def config_path(self) -> str:
        _paths = {
            AgentPlatform.OPENCODE: ".config/opencode/mcp.json",
            AgentPlatform.PI: ".config/pi/mcp.json",
            AgentPlatform.VIBE: ".config/vibe/mcp.json",
            AgentPlatform.MY_AGENT: ".config/my-agent/mcp.json",  # <-- add
        }
        return _paths[self]
```

The value (`"my-agent"`) must match the `"platform"` string used in `mcp/mcp.json`.

## Step 2: Create an installer

**File:** `src/ai_toolkit/install_mcp_servers/installers/my_agent_installer.py`

Use `opencode_installer.py` as a template. The class needs:

- Constructor accepting `platform` (defaulting to your `AgentPlatform` member)
- `install(server: McpServerDef) -> bool` method that runs the agent's install command
- Skip with `True` if `self.platform` doesn't match (another agent's turn)

```python
import subprocess

from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.shell import shell_command_exists


class MyAgentMcpInstaller:
    def __init__(self, platform: str = AgentPlatform.MY_AGENT) -> None:
        self.platform = platform

    def install(self, server: McpServerDef) -> bool:
        if self.platform == AgentPlatform.MY_AGENT:
            if not shell_command_exists("my-agent"):
                print(f"MCP server '{server.name}' requires 'my-agent' which is not on PATH")
                return False

            non_flag_args = [a for a in server.args if not a.startswith("-")]
            if not non_flag_args:
                print(f"MCP server '{server.name}': no package name found in args {server.args}")
                return False

            pkg = non_flag_args[0]
            print(f"Installing MCP server '{server.name}' via my-agent: {pkg}")

            result = subprocess.run(
                ["my-agent", "mcp-add", pkg],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if result.returncode != 0:
                print(f"MCP server '{server.name}': my-agent install failed")
                return False

            print(f"MCP server '{server.name}': installed")
            return True
        else:
            print(f"MCP server '{server.name}': platform is '{self.platform}', skipping my-agent install")
            return True
```

## Step 3: Wire into `main.py`

**File:** `src/ai_toolkit/install_mcp_servers/main.py`

1. Import your installer
2. Instantiate it
3. Pass it to `install_mcp()`

```python
from ai_toolkit.install_mcp_servers.installers.my_agent_installer import (
    MyAgentMcpInstaller,
)
# ...
    my_agent_installer = MyAgentMcpInstaller(platform=platform)

    failed = install_mcp(
        NpxMcpInstaller(),
        UvxMcpInstaller(),
        CommandMcpInstaller(),
        HttpMcpInstaller(dotenv_path=dotenv),
        opencode_installer,
        pi_installer,
        vibe_installer,
        my_agent_installer,          # <-- add
        servers,
    )
```

## Step 4: Wire into `install_mcp.py`

**File:** `src/ai_toolkit/install_mcp_servers/installers/install_mcp.py`

Add the parameter and the routing branch:

```python
def install_mcp(
    ...
    my_agent_installer: McpInstaller,
    servers: list[McpServerDef],
) -> list[str]:
    ...
        elif platform == AgentPlatform.MY_AGENT:
            success = my_agent_installer.install(server)
```

## Step 5: Add tests

1. Create `tests/.../installers/test_my_agent_installer.py` (follow `test_opencode_installer.py`)
2. Add routing tests to `test_install_mcp.py`
3. The deploy tests don't need changes — `AgentPlatform` iteration covers new members automatically.

## Step 6: Update docs

- `README.md` — add the agent to the supported platforms table
- `docs/mcp-servers.md` — add the agent to the platforms table
