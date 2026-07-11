from pathlib import Path

import pytest

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.parsing.list_local_skills import list_local_skills


class TestListLocalSkills:
    @pytest.mark.integration
    def test_list_when_dir_does_not_exist_then_returns_empty(
        self, tmp_path: Path
    ) -> None:
        nonexistent = tmp_path / "no-such-dir"
        skills = list_local_skills(nonexistent)
        assert skills == []

    @pytest.mark.integration
    def test_list_when_dir_empty_then_returns_empty(self, skills_dir: Path) -> None:
        skills = list_local_skills(skills_dir)
        assert skills == []

    @pytest.mark.integration
    def test_list_when_dir_has_markdown_files_then_returns_skill_defs(
        self,
        skills_dir: Path,
    ) -> None:
        (skills_dir / "alpha.md").write_text("---\nname: alpha\n---\nContent")
        (skills_dir / "beta.md").write_text("---\nname: beta\n---\nContent")
        skills = list_local_skills(skills_dir)
        assert len(skills) == 2
        assert skills[0] == SkillDef(name="alpha", source=str(skills_dir / "alpha.md"))
        assert skills[1] == SkillDef(name="beta", source=str(skills_dir / "beta.md"))

    @pytest.mark.integration
    def test_list_when_dir_has_non_markdown_files_then_ignores_them(
        self,
        skills_dir: Path,
    ) -> None:
        (skills_dir / "readme.txt").write_text("not a skill")
        (skills_dir / "skill.md").write_text("---\nname: skill\n---\nContent")
        skills = list_local_skills(skills_dir)
        assert len(skills) == 1
        assert skills[0].name == "skill"

    @pytest.mark.integration
    def test_list_when_files_exist_then_returns_sorted(self, skills_dir: Path) -> None:
        (skills_dir / "z.md").write_text("---\nname: zebra\n---\n")
        (skills_dir / "a.md").write_text("---\nname: alpha\n---\n")
        skills = list_local_skills(skills_dir)
        assert skills[0].name == "alpha"
        assert skills[1].name == "zebra"
