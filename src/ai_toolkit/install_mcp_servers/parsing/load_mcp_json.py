import json
from pathlib import Path

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


def load_mcp_json(file_path: Path) -> list[McpServerDef]:
    if not file_path.exists():
        return []

    data = json.loads(file_path.read_text(encoding="utf-8"))
    servers_data = data.get("mcpServers", {})

    result: list[McpServerDef] = []
    for name, cfg in servers_data.items():
        result.append(
            McpServerDef(
                name=str(name),
                command=cfg.get("command"),
                args=tuple(cfg.get("args", [])),
                env=tuple((str(k), str(v)) for k, v in cfg.get("env", {}).items()),
                server_type=cfg.get("type"),
                url=cfg.get("url"),
                disabled=cfg.get("disabled", False),
                platform=cfg.get("platform"),
            )
        )

    return result
