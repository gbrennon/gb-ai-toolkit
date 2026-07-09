from enum import StrEnum


class AgentPlatform(StrEnum):
    """MCP agent platforms that can install and receive config deployments."""

    OPENCODE = "opencode"
    PI = "pi"
    VIBE = "vibe"

    @property
    def config_path(self) -> str:
        """Relative path under ~/ for this agent's MCP settings file."""
        _paths = {
            AgentPlatform.OPENCODE: ".config/opencode/mcp.json",
            AgentPlatform.PI: ".config/pi/mcp.json",
            AgentPlatform.VIBE: ".config/vibe/mcp.json",
        }
        return _paths[self]
