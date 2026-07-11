import os
from pathlib import Path
from unittest.mock import patch

import pytest

from ai_toolkit.install_mcp_servers.config_paths import ConfigPaths


class TestConfigPaths:
    @pytest.mark.unit
    @patch.dict(os.environ, {"APPDATA": "C:\\Users\\test\\AppData\\Roaming"})
    def test_get_standard_config_paths_windows_with_appdata(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("windows")

        assert paths == [
            Path("C:\\Users\\test\\AppData\\Roaming") / "mcp" / "mcp.json",
            Path(".mcp") / "mcp.json",
        ]

    @pytest.mark.unit
    @patch.dict(os.environ, {}, clear=True)
    def test_get_standard_config_paths_windows_without_appdata(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("windows")

        assert paths == [
            Path(".mcp") / "mcp.json",
        ]

    @pytest.mark.unit
    @patch.dict(os.environ, {"XDG_CONFIG_HOME": "/home/user/.config"})
    def test_get_standard_config_paths_linux_with_xdg(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("linux")

        assert Path("/home/user/.config") / "mcp" / "mcp.json" in paths
        assert Path.home() / ".mcp.json" in paths
        assert Path(".mcp") / "mcp.json" in paths
        assert Path("/etc/opt/mcp/config.json") in paths
        assert len(paths) == 4

    @pytest.mark.unit
    @patch.dict(os.environ, {}, clear=True)
    def test_get_standard_config_paths_linux_without_xdg(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("linux")

        assert Path.home() / ".config" / "mcp" / "mcp.json" in paths
        assert Path.home() / ".mcp.json" in paths
        assert Path(".mcp") / "mcp.json" in paths
        assert Path("/etc/opt/mcp/config.json") in paths
        assert len(paths) == 4

    @pytest.mark.unit
    @patch.dict(os.environ, {"XDG_CONFIG_HOME": "/home/user/.config"})
    def test_get_standard_config_paths_darwin_without_etc(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("darwin")

        assert Path("/home/user/.config") / "mcp" / "mcp.json" in paths
        assert Path.home() / ".mcp.json" in paths
        assert Path(".mcp") / "mcp.json" in paths
        assert Path("/etc/opt/mcp/config.json") not in paths
        assert len(paths) == 3

    @pytest.mark.unit
    @patch.dict(os.environ, {"XDG_CONFIG_HOME": "/home/user/.config"})
    def test_get_standard_config_paths_else_platform_defaults_to_linux_behaviour(
        self,
    ) -> None:
        paths = ConfigPaths().get_standard_config_paths("freebsd")

        assert Path("/home/user/.config") / "mcp" / "mcp.json" in paths
        assert len(paths) == 3

    @pytest.mark.integration
    @patch.dict(os.environ, {}, clear=True)
    def test_get_standard_config_paths_linux_no_env_uses_home_fallback(
        self,
    ) -> None:
        paths = ConfigPaths().get_standard_config_paths("linux")

        assert Path.home() / ".config" / "mcp" / "mcp.json" == paths[0]

    @pytest.mark.integration
    def test_get_standard_config_paths_windows_no_appdata_returns_only_dotmcp(
        self,
    ) -> None:
        paths = ConfigPaths().get_standard_config_paths("windows")

        assert paths == [Path(".mcp") / "mcp.json"]

    @pytest.mark.unit
    @patch.dict(os.environ, {"XDG_CONFIG_HOME": "/home/user/.config"}, clear=True)
    def test_get_standard_config_paths_linux_order_is_predictable(self) -> None:
        paths = ConfigPaths().get_standard_config_paths("linux")

        assert paths[0] == Path("/home/user/.config") / "mcp" / "mcp.json"
        assert paths[1] == Path.home() / ".mcp.json"
        assert paths[2] == Path(".mcp") / "mcp.json"
        assert paths[3] == Path("/etc/opt/mcp/config.json")
        assert len(paths) == 4
