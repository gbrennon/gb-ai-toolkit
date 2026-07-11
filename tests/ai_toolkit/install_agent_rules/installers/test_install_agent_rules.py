from pathlib import Path

import pytest

from ai_toolkit.install_agent_rules.installers.install_agent_rules import (
    install_agent_rules,
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


class TestInstallAgentRules:
    @pytest.mark.integration
    def test_install_when_rules_exist_then_returns_zero(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "rules.d"
        rules_dir.mkdir()
        (rules_dir / "00-base.md").write_text("# Base")
        target = tmp_path / "AGENT.md"
        rc = install_agent_rules(source_dir=rules_dir, target_path=target)
        assert rc == 0
        assert target.is_file()

    @pytest.mark.integration
    def test_install_when_no_rules_then_returns_one(self, tmp_path: Path) -> None:
        rules_dir = tmp_path / "empty.d"
        rules_dir.mkdir()
        target = tmp_path / "AGENT.md"
        rc = install_agent_rules(source_dir=rules_dir, target_path=target)
        assert rc == 1
