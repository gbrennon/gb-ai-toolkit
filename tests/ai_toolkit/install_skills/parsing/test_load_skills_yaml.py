from pathlib import Path

import pytest

from ai_toolkit.install_skills.parsing.load_skills_yaml import load_skills_yaml


class TestLoadSkillsYaml:
    @pytest.mark.integration
    def test_load_when_yaml_has_skills_list_then_returns_list(
        self,
        sample_yaml: Path,
    ) -> None:
        result = load_skills_yaml(sample_yaml)
        assert result == [
            "forging-blocks-org/forging-blocks/tree/main/skills/forging-blocks-maintenance",
            "owner/repo/some-skill",
        ]

    @pytest.mark.integration
    def test_load_when_yaml_empty_then_raises_value_error(self, tmp_path: Path) -> None:
        p = tmp_path / "empty.yaml"
        p.write_text("---\nskills: []\n")
        result = load_skills_yaml(p)
        assert result == []

    @pytest.mark.integration
    def test_load_when_yaml_skills_not_a_list_then_raises_value_error(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / "bad.yaml"
        p.write_text("skills: not-a-list\n")
        with pytest.raises(ValueError, match="skills must be a list"):
            load_skills_yaml(p)

    @pytest.mark.integration
    def test_load_when_yaml_missing_skills_key_then_raises_type_error(
        self,
        tmp_path: Path,
    ) -> None:
        p = tmp_path / "missing.yaml"
        p.write_text("other: data\n")
        with pytest.raises(ValueError, match="skills must be a list"):
            load_skills_yaml(p)
