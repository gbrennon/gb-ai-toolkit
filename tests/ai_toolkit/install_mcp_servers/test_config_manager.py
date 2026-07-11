import json
from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.config_manager import ConfigManager
from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef


class TestConfigManager:
    @pytest.mark.unit
    def test_default_platform_is_linux(self):
        cm = ConfigManager()
        assert cm.platform == "linux"

    @pytest.mark.unit
    def test_custom_platform(self):
        cm = ConfigManager(platform="windows")
        assert cm.platform == "windows"

    @pytest.mark.unit
    def test_get_standard_config_paths_linux_includes_user_and_system(self):
        cm = ConfigManager(platform="linux")
        paths = cm.get_standard_config_paths()
        assert len(paths) >= 3

    @pytest.mark.unit
    def test_find_config_files_no_existing_returns_empty(self, tmp_path):
        cm = ConfigManager(platform="linux")
        cm.get_standard_config_paths = lambda: [tmp_path / "nonexistent.json"]
        existing = cm.find_config_files()
        assert existing == []

    @pytest.mark.unit
    def test_find_config_files_existing_returns_path(self, tmp_path):
        config_path = tmp_path / "mcp.json"
        config_path.write_text('{"mcpServers": {"test": {"command": "echo"}}}')
        cm = ConfigManager(platform="linux")
        cm.get_standard_config_paths = lambda: [config_path]
        existing = cm.find_config_files()
        assert existing == [config_path]

    @pytest.mark.unit
    def test_load_config_hierarchy_empty_returns_empty(self):
        cm = ConfigManager(platform="linux")
        cm.find_config_files = lambda: []
        cm._apply_env_overrides = lambda config: config
        config = cm.load_config_hierarchy()
        assert config == {}

    @pytest.mark.unit
    def test_load_config_hierarchy_single_file(self, tmp_path):
        config_path = tmp_path / "mcp.json"
        config_path.write_text(
            json.dumps(
                {
                    "mcpServers": {"srv1": {"command": "npx", "args": ["pkg1"]}},
                }
            )
        )
        cm = ConfigManager(platform="linux")
        cm.find_config_files = lambda: [config_path]
        cm._apply_env_overrides = lambda config: config
        config = cm.load_config_hierarchy()
        assert "srv1" in config["mcpServers"]

    @pytest.mark.unit
    def test_get_servers_from_config_no_mcp_servers_returns_empty(self):
        cm = ConfigManager(platform="linux")
        cm.load_config_hierarchy = lambda: {}
        servers = cm.get_servers_from_config()
        assert servers == []

    @pytest.mark.unit
    def test_get_servers_from_config_returns_mcp_server_defs(self):
        cm = ConfigManager(platform="linux")
        cm.load_config_hierarchy = lambda: {
            "mcpServers": {"srv1": {"command": "npx", "args": ["pkg"]}},
        }
        servers = cm.get_servers_from_config()
        assert len(servers) == 1
        assert isinstance(servers[0], McpServerDef)
        assert servers[0].name == "srv1"
        assert servers[0].command == "npx"

    @pytest.mark.unit
    def test_load_from_file(self, tmp_path):
        cm = ConfigManager(platform="linux")
        p = tmp_path / "mcp.json"
        p.write_text('{"mcpServers": {"test": {"command": "echo"}}}')
        servers = cm.load_from_file(p)
        assert len(servers) == 1
        assert servers[0].name == "test"

    @pytest.mark.unit
    def test_load_from_missing_file_returns_empty(self):
        cm = ConfigManager(platform="linux")
        servers = cm.load_from_file(Path("/nonexistent/mcp.json"))
        assert servers == []
