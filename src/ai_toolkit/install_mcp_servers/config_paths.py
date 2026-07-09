import os
from pathlib import Path
from typing import List


class ConfigPaths:
    """Discovers standard MCP config file locations on each platform."""

    def get_standard_config_paths(self, platform: str) -> List[Path]:
        paths: List[Path] = []

        if platform == "windows":
            appdata = os.environ.get("APPDATA")
            if appdata:
                paths.append(Path(appdata) / "mcp" / "mcp.json")
            paths.append(Path(".mcp") / "mcp.json")
        else:
            xdg_config = os.environ.get("XDG_CONFIG_HOME")
            if xdg_config:
                paths.append(Path(xdg_config) / "mcp" / "mcp.json")
            else:
                paths.append(Path.home() / ".config" / "mcp" / "mcp.json")

            paths.append(Path.home() / ".mcp.json")
            paths.append(Path(".mcp") / "mcp.json")

            if platform == "linux":
                paths.append(Path("/etc/opt/mcp/config.json"))
        return paths
