from pathlib import Path

import ai_toolkit.install_agent_rules.installers.install_agent_rules as _installers_module
import pytest

from ai_toolkit.install_agent_rules.installers.install_agent_rules import (
    _DEFAULT_TARGETS_TEMPLATE,
    install_agent_rules,
    read_target_paths,
)
from ai_toolkit.install_agent_rules.models.agent_rule import AgentRule
from ai_toolkit.install_agent_rules.parsing.compose_rules import (
    compose_rules_to_file,
)
from ai_toolkit.install_agent_rules.parsing.load_rules_dir import (
    read_rules_dir,
)


class TestComposeRulesToFile:
    @pytest.mark.integration
    def test_writes_rules_to_disk(self, tmp_path: Path) -> None:
        rules = [
            AgentRule(content="# Base", order=0, name="base"),
        ]
        target = tmp_path / "AGENT.md"
        compose_rules_to_file(rules, "test", target)
        assert target.is_file()
        content = target.read_text(encoding="utf-8")
        assert "# Agent Rules" in content
        assert "# Base" in content


class TestReadRulesDir:
    @pytest.mark.integration
    def test_reads_directory(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        (rules_dir / "10-tools.md").write_text("# Tools")
        files = read_rules_dir(rules_dir)
        assert "00-base.md" in files
        assert "10-tools.md" in files
        assert files["00-base.md"] == "# Base"

    @pytest.mark.integration
    def test_when_not_exists_returns_empty(self, tmp_path: Path) -> None:
        assert read_rules_dir(tmp_path / "nonexistent") == {}


class TestReadTargetPaths:
    @pytest.mark.integration
    def test_missing_manifest_returns_empty(self, tmp_path: Path) -> None:
        assert read_target_paths(tmp_path / "missing.txt") == []

    @pytest.mark.integration
    def test_ignores_comments_and_blank_lines(self, tmp_path: Path) -> None:
        manifest = tmp_path / "targets.txt"
        manifest.write_text("# comment\n\n~/one/AGENTS.md\n\ntwo/AGENTS.md\n")
        paths = read_target_paths(manifest)
        assert len(paths) == 2
        assert str(paths[0]) == str(Path.home() / "one" / "AGENTS.md")
        assert str(paths[1]) == "two/AGENTS.md"


class TestInstallAgentRules:
    @pytest.mark.integration
    def test_install_when_rules_exist_then_returns_zero(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        target = tmp_path / "AGENTS.md"
        targets_file = tmp_path / "targets.txt"
        targets_file.write_text(str(target) + "\n")
        rc = install_agent_rules(source_dir=rules_dir, targets_file=targets_file)
        assert rc == 0
        assert target.is_file()

    @pytest.mark.integration
    def test_install_when_no_rules_then_returns_one(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "empty.d"
        rules_dir.mkdir()
        rc = install_agent_rules(source_dir=rules_dir)
        assert rc == 1

    @pytest.mark.integration
    def test_install_writes_to_all_manifest_targets(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        first = tmp_path / "one" / "AGENTS.md"
        second = tmp_path / "two" / "AGENTS.md"
        targets_file = tmp_path / "targets.txt"
        targets_file.write_text(f"# destinations\n{first}\n\n{second}\n")
        rc = install_agent_rules(source_dir=rules_dir, targets_file=targets_file)
        assert rc == 0
        assert first.is_file()
        assert second.is_file()
        assert first.read_text(encoding="utf-8") == second.read_text(encoding="utf-8")

    @pytest.mark.integration
    def test_default_targets_template_parses(self, tmp_path: Path) -> None:
        manifest = tmp_path / "template.txt"
        manifest.write_text(_DEFAULT_TARGETS_TEMPLATE, encoding="utf-8")
        paths = read_target_paths(manifest)
        assert len(paths) == 4
        assert str(paths[0]) == str(Path.home() / ".agents" / "AGENTS.md")

    @pytest.mark.integration
    def test_install_seeds_default_manifest_when_missing(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        manifest = tmp_path / "config" / "agent_targets.txt"
        monkeypatch.setattr(_installers_module, "AGENT_TARGETS_FILE", manifest)
        monkeypatch.setattr(
            _installers_module,
            "_DEFAULT_TARGETS_TEMPLATE",
            f"# destinations\n{tmp_path / 'AGENTS.md'}\n",
        )
        rc = install_agent_rules(source_dir=rules_dir)
        assert rc == 0
        assert manifest.is_file()
        assert (tmp_path / "AGENTS.md").is_file()

    @pytest.mark.integration
    def test_install_when_targets_file_has_no_paths_then_returns_one(
        self, tmp_path: Path
    ) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        targets_file = tmp_path / "targets.txt"
        targets_file.write_text("# only comments\n")
        rc = install_agent_rules(source_dir=rules_dir, targets_file=targets_file)
        assert rc == 1

    @pytest.mark.integration
    def test_install_accepts_adhoc_target_path(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        target = tmp_path / "AGENTS.md"
        rc = install_agent_rules(source_dir=rules_dir, target_path=target)
        assert rc == 0
        assert target.is_file()
