import json
import os
from pathlib import Path
from typing import Any, Dict


class EnvOverrideApplier:
    """Applies MCP_CONFIG_PATH environment variable overrides to a config dict."""

    def apply_env_overrides(self, config: Dict[str, Any]) -> Dict[str, Any]:
        override_config_path = os.environ.get("MCP_CONFIG_PATH")
        if override_config_path and Path(override_config_path).exists():
            try:
                with open(override_config_path, 'r', encoding='utf-8') as f:
                    env_config = json.load(f)
                    for key, value in env_config.items():
                        if key == "mcpServers" and "mcpServers" in config:
                            for server_name, server_config in value.items():
                                config["mcpServers"][server_name] = server_config
                        else:
                            config[key] = value
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load env config file {override_config_path}: {e}")
        return config
