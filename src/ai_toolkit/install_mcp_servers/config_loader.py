import json
from pathlib import Path
from typing import Any, Dict, List

from ai_toolkit.install_mcp_servers.config_paths import ConfigPaths


class ConfigLoader:
    """Finds existing config files and merges them hierarchically."""

    def __init__(self, config_paths: ConfigPaths | None = None) -> None:
        self._config_paths = config_paths or ConfigPaths()

    def find_config_files(self, platform: str) -> List[Path]:
        standard_paths = self._config_paths.get_standard_config_paths(platform)
        return [path for path in standard_paths if path.exists()]

    def load_config_hierarchy(self, config_files: List[Path]) -> Dict[str, Any]:
        merged_config: Dict[str, Any] = {}

        for config_file in reversed(config_files):
            try:
                with open(config_file, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    if "mcpServers" in config_data:
                        if "mcpServers" not in merged_config:
                            merged_config["mcpServers"] = {}
                        for server_name, server_config in config_data[
                            "mcpServers"
                        ].items():
                            merged_config["mcpServers"][server_name] = server_config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load config file {config_file}: {e}")

        return merged_config
