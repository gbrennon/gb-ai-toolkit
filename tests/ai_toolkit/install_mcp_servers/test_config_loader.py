import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_toolkit.install_mcp_servers.config_loader import ConfigLoader
from ai_toolkit.install_mcp_servers.config_paths import ConfigPaths


class TestConfigLoader:
    @pytest.mark.unit
    def test_find_config_files_when_none_exist_returns_empty(
        self,
    ) -> None:
        paths = [
            Path("/nonexistent/mcp.json"),
            Path("/nonexistent/.mcp.json"),
        ]
        loader = ConfigLoader(config_paths=_fake_config_paths(paths))

        found = loader.find_config_files("linux")

        assert found == []

    @pytest.mark.unit
    def test_find_config_files_when_one_exists_returns_it(
        self,
        tmp_path: Path,
    ) -> None:
        existing = tmp_path / "mcp.json"
        existing.write_text("{}")
        missing = tmp_path / ".mcp.json"
        loader = ConfigLoader(
            config_paths=_fake_config_paths([existing, missing])
        )

        found = loader.find_config_files("linux")

        assert found == [existing]

    @pytest.mark.integration
    def test_find_config_files_when_multiple_exist_returns_all(
        self,
        tmp_path: Path,
    ) -> None:
        a = tmp_path / "a.json"
        b = tmp_path / "b.json"
        a.write_text("{}")
        b.write_text("{}")
        loader = ConfigLoader(
            config_paths=_fake_config_paths([a, b])
        )

        found = loader.find_config_files("linux")

        assert found == [a, b]

    @pytest.mark.unit
    def test_load_config_hierarchy_single_file_returns_servers(self) -> None:
        config_file = _config_file({"mcpServers": {"server-a": {"command": "uvx"}}})
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([config_file])

        assert result == {"mcpServers": {"server-a": {"command": "uvx"}}}

    @pytest.mark.unit
    def test_load_config_hierarchy_first_wins(self) -> None:
        first = _config_file({"mcpServers": {"shared": {"key": "first"}, "unique-a": {"key": "a"}}})
        second = _config_file({"mcpServers": {"shared": {"key": "second"}, "unique-b": {"key": "b"}}})
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([first, second])

        assert result == {
            "mcpServers": {
                "shared": {"key": "first"},
                "unique-a": {"key": "a"},
                "unique-b": {"key": "b"},
            },
        }

    @pytest.mark.unit
    def test_load_config_hierarchy_first_file_has_highest_priority(
        self,
    ) -> None:
        first = _config_file({"mcpServers": {"srv": {"setting": "first"}}})
        second = _config_file({"mcpServers": {"srv": {"setting": "second"}}})
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([first, second])

        assert result["mcpServers"]["srv"]["setting"] == "first"

    @pytest.mark.unit
    def test_load_config_hierarchy_empty_list_returns_empty_dict(self) -> None:
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([])

        assert result == {}

    @pytest.mark.unit
    def test_load_config_hierarchy_file_without_mcp_servers_key_ignored(
        self,
    ) -> None:
        cfg = _config_file({"other": "data"})
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([cfg])

        assert result == {}

    @pytest.mark.unit
    def test_load_config_hierarchy_io_error_skips_file(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        bad_path = Path("/nonexistent/mcp.json")
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([bad_path])

        assert result == {}
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    @pytest.mark.unit
    def test_load_config_hierarchy_json_decode_error_skips_file(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        cfg = _config_file("not valid json")
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([cfg])

        assert result == {}
        captured = capsys.readouterr()
        assert "Warning" in captured.out

    @pytest.mark.unit
    def test_load_config_hierarchy_io_error_among_valid_returns_partial(
        self,
        capsys: pytest.CaptureFixture[str],
    ) -> None:
        valid = _config_file({"mcpServers": {"good": {"key": "val"}}})
        bad = Path("/nonexistent/mcp.json")
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([valid, bad])

        assert result == {"mcpServers": {"good": {"key": "val"}}}

    @pytest.mark.integration
    def test_find_and_load_config_paths_integration(
        self,
        tmp_path: Path,
    ) -> None:
        high = tmp_path / "high_priority.json"
        low = tmp_path / "low_priority.json"
        high.write_text(json.dumps({"mcpServers": {"srv": {"cmd": "npx"}}}))
        low.write_text(json.dumps({"mcpServers": {"srv": {"cmd": "uvx"}}}))

        with patch.object(ConfigPaths, "get_standard_config_paths", return_value=[high, low]):
            loader = ConfigLoader()
            config_files = loader.find_config_files("linux")
            result = loader.load_config_hierarchy(config_files)

        assert result == {"mcpServers": {"srv": {"cmd": "npx"}}}

    @pytest.mark.integration
    def test_load_config_hierarchy_multiple_files_with_disjoint_servers(
        self,
    ) -> None:
        a = _config_file({"mcpServers": {"server-a": {"cmd": "uvx"}}})
        b = _config_file({"mcpServers": {"server-b": {"cmd": "npx"}}})
        loader = ConfigLoader()

        result = loader.load_config_hierarchy([a, b])

        assert result["mcpServers"] == {
            "server-a": {"cmd": "uvx"},
            "server-b": {"cmd": "npx"},
        }

    @pytest.mark.unit
    def test_find_config_files_delegates_to_config_paths(
        self,
    ) -> None:
        mock_paths = MagicMock(spec=ConfigPaths)
        mock_paths.get_standard_config_paths.return_value = [Path("/a"), Path("/b")]
        loader = ConfigLoader(config_paths=mock_paths)

        with (
            patch.object(Path, "exists", return_value=True),
        ):
            found = loader.find_config_files("linux")

        assert found == [Path("/a"), Path("/b")]
        mock_paths.get_standard_config_paths.assert_called_once_with("linux")

    @pytest.mark.unit
    def test_load_config_hierarchy_warning_format(self, capsys) -> None:
        cfg = _config_file("{{{invalid")
        loader = ConfigLoader()

        loader.load_config_hierarchy([cfg])

        captured = capsys.readouterr()
        assert "Warning" in captured.out


def _fake_config_paths(paths: list[Path]) -> ConfigPaths:
    fake = MagicMock(spec=ConfigPaths)
    fake.get_standard_config_paths.return_value = paths
    return fake


def _config_file(content) -> Path:
    import tempfile

    if isinstance(content, str):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        f.write(content)
        f.close()
        return Path(f.name)
    f = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
    json.dump(content, f)
    f.close()
    return Path(f.name)