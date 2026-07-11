from pathlib import Path


import pytest

import importlib

from ai_toolkit.install_agent_rules.main import _persist_to_global, main

main_module = importlib.import_module("ai_toolkit.install_agent_rules.main")


class TestPersistToGlobal:
    @pytest.mark.integration
    def test_with_rules_then_copies_to_global(self, tmp_path: Path) -> None:
        source = tmp_path / "source.d"
        source.mkdir()
        (source / "00-base.md").write_text("# Base")
        (source / "10-tools.md").write_text("# Tools")
        global_dir = tmp_path / "global-rules"
        rc = _persist_to_global(source, global_dir=global_dir)
        assert rc == 0
        assert (global_dir / "00-base.md").is_file()
        assert (global_dir / "10-tools.md").is_file()

    @pytest.mark.integration
    def test_with_empty_dir_then_returns_one(self, tmp_path: Path) -> None:
        source = tmp_path / "empty.d"
        source.mkdir()
        rc = _persist_to_global(source)
        assert rc == 1

    @pytest.mark.integration
    def test_with_nonexistent_dir_then_returns_one(self, tmp_path: Path) -> None:
        rc = _persist_to_global(tmp_path / "nonexistent")
        assert rc == 1


class TestMainCli:
    @pytest.mark.integration
    def test_with_source_and_target_then_composes(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        target = tmp_path / "AGENT.md"
        rc = main(["--source", str(rules_dir), "--target", str(target)])
        assert rc == 0
        assert target.is_file()

    @pytest.mark.integration
    def test_with_persist_then_copies_then_composes(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        source = tmp_path / "dev_rules"
        source.mkdir()
        (source / "00-base.md").write_text("# Base")
        global_dir = tmp_path / "global-rules"
        monkeypatch.setattr(main_module, "_GLOBAL_RULES_DIR", global_dir)
        target = tmp_path / "AGENT.md"
        rc = main(
            [
                "--source",
                str(source),
                "--target",
                str(target),
                "--persist",
            ]
        )
        assert rc == 0
        assert target.is_file()
        assert (global_dir / "00-base.md").is_file()

    @pytest.mark.integration
    def test_with_persist_and_no_rules_then_returns_one(self, tmp_path: Path) -> None:
        source = tmp_path / "empty.d"
        source.mkdir()
        target = tmp_path / "AGENT.md"
        rc = main(
            [
                "--source",
                str(source),
                "--target",
                str(target),
                "--persist",
            ]
        )
        assert rc == 1

    @pytest.mark.integration
    def test_with_no_rules_then_returns_one(self, tmp_path: Path) -> None:
        source = tmp_path / "empty.d"
        source.mkdir()
        rc = main(["--source", str(source)])
        assert rc == 1

    @pytest.mark.integration
    def test_with_persist_composes_from_global_after_copy(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        source = tmp_path / "dev_rules"
        source.mkdir()
        (source / "00-base.md").write_text("# Base")
        global_dir = tmp_path / "global-rules"
        monkeypatch.setattr(main_module, "_GLOBAL_RULES_DIR", global_dir)
        target = tmp_path / "AGENT.md"
        rc = main(
            [
                "--source",
                str(source),
                "--target",
                str(target),
                "--persist",
            ]
        )
        assert rc == 0
        assert target.is_file()
