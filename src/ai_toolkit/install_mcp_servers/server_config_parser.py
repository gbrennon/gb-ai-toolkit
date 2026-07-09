from typing import Any, Dict, List

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


class ServerConfigParser:
    """Parses a merged config dict into McpServerDef instances."""

    def get_servers_from_config(self, config: Dict[str, Any]) -> List[McpServerDef]:
        if "mcpServers" not in config:
            return []

        servers_data = config["mcpServers"]
        result: List[McpServerDef] = []

        for name, cfg in servers_data.items():
            result.append(McpServerDef(
                name=str(name),
                command=cfg.get("command"),
                args=tuple(cfg.get("args", [])),
                env=tuple(
                    (str(k), str(v))
                    for k, v in cfg.get("env", {}).items()
                ),
                server_type=cfg.get("type"),
                url=cfg.get("url"),
                disabled=cfg.get("disabled", False),
            ))
        return result
