import json
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from ai_toolkit.install_mcp_servers.env_override_applier import EnvOverrideApplier


class TestEnvOverrideApplier:
    @pytest.mark.unit
    def test_when_env_var_not_set_then_config_unchanged(self):
        applier = EnvOverrideApplier()
        config = {"key": "value"}

        with patch.dict("os.environ", {}, clear=True):
            result = applier.apply_env_overrides(config)

        assert result == {"key": "value"}

    @pytest.mark.unit
    def test_when_env_var_set_but_file_missing_then_config_unchanged(self):
        applier = EnvOverrideApplier()
        config = {"key": "value"}

        with patch.dict(
            "os.environ", {"MCP_CONFIG_PATH": "/nonexistent/override.json"}
        ):
            with patch.object(Path, "exists", return_value=False):
                result = applier.apply_env_overrides(config)

        assert result == {"key": "value"}

    @pytest.mark.unit
    def test_when_file_has_mcp_servers_and_config_has_mcp_servers_then_merged(self):
        applier = EnvOverrideApplier()
        config = {"mcpServers": {"existing": {"command": "echo"}}}
        env_content = json.dumps({"mcpServers": {"new_one": {"command": "npx"}}})

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=env_content)):
                    result = applier.apply_env_overrides(config)

        assert result == {
            "mcpServers": {
                "existing": {"command": "echo"},
                "new_one": {"command": "npx"},
            }
        }

    @pytest.mark.unit
    def test_when_file_has_mcp_servers_but_config_has_no_mcp_servers_then_assigned_directly(
        self,
    ):
        applier = EnvOverrideApplier()
        config = {"other": "value"}
        env_content = json.dumps({"mcpServers": {"srv": {"command": "npx"}}})

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=env_content)):
                    result = applier.apply_env_overrides(config)

        assert result == {"other": "value", "mcpServers": {"srv": {"command": "npx"}}}

    @pytest.mark.unit
    def test_when_file_has_non_mcp_servers_keys_then_assigned_directly(self):
        applier = EnvOverrideApplier()
        config = {"existing": "old"}
        env_content = json.dumps({"new_key": "new_value", "another": 42})

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=env_content)):
                    result = applier.apply_env_overrides(config)

        assert result == {"existing": "old", "new_key": "new_value", "another": 42}

    @pytest.mark.unit
    def test_when_file_has_mixed_keys_then_mcp_servers_merged_and_others_assigned(self):
        applier = EnvOverrideApplier()
        config = {"mcpServers": {"s1": {"command": "a"}}, "keep": "me"}
        env_content = json.dumps(
            {
                "mcpServers": {"s2": {"command": "b"}},
                "extra": "value",
            }
        )

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open(read_data=env_content)):
                    result = applier.apply_env_overrides(config)

        assert result == {
            "mcpServers": {"s1": {"command": "a"}, "s2": {"command": "b"}},
            "keep": "me",
            "extra": "value",
        }

    @pytest.mark.unit
    def test_when_file_contains_invalid_json_then_warning_and_config_unchanged(
        self, capsys
    ):
        applier = EnvOverrideApplier()
        config = {"key": "value"}

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open(read_data="not json")):
                    result = applier.apply_env_overrides(config)

        captured = capsys.readouterr()
        assert result == {"key": "value"}
        assert "Warning: Could not load env config file /fake/path.json" in captured.out

    @pytest.mark.unit
    def test_when_file_read_fails_with_ioerror_then_warning_and_config_unchanged(
        self, capsys
    ):
        applier = EnvOverrideApplier()

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": "/fake/path.json"}):
            with patch.object(Path, "exists", return_value=True):
                with patch("builtins.open", mock_open()) as m:
                    m.side_effect = IOError("Permission denied")
                    result = applier.apply_env_overrides({"key": "value"})

        captured = capsys.readouterr()
        assert result == {"key": "value"}
        assert "Warning: Could not load env config file /fake/path.json" in captured.out

    @pytest.mark.integration
    def test_with_real_file_on_disk(self, tmp_path):
        applier = EnvOverrideApplier()
        config = {"mcpServers": {"s1": {"command": "a"}}}
        override_file = tmp_path / "override.json"
        override_file.write_text(
            json.dumps({"mcpServers": {"s2": {"command": "b"}}, "other": "val"})
        )

        with patch.dict("os.environ", {"MCP_CONFIG_PATH": str(override_file)}):
            result = applier.apply_env_overrides(config)

        assert result == {
            "mcpServers": {"s1": {"command": "a"}, "s2": {"command": "b"}},
            "other": "val",
        }
