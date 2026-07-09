from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ai_toolkit.install_mcp_servers.models.agent_platform import AgentPlatform


@dataclass(frozen=True)
class McpServerDef:
    name: str
    command: str | None
    args: tuple[str, ...]
    env: tuple[tuple[str, str], ...]
    server_type: str | None
    url: str | None
    disabled: bool
    platform: "AgentPlatform | None" = None
