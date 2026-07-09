from pathlib import Path

import pytest

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.installers.local_skill_installer import (
    LocalSkillInstaller,
)


class TestLocalSkillInstaller:
    @pytest.mark.integration
    def test_install_when_source_exists_then_copies_to_target(
        self,
        skills_dir: Path,
        target_dir: Path,
    ) -> None:
        skill_file = skills_dir / "test-skill.md"
        skill_file.write_text("# Test content")
        installer = LocalSkillInstaller(target_dir=target_dir)
        skill = SkillDef(name="test-skill", source=str(skill_file))
        result = installer.install(skill)
        assert result is True
        installed_file = target_dir / "test-skill" / "SKILL.md"
        assert installed_file.read_text() == "# Test content"

    @pytest.mark.integration
    def test_install_when_source_missing_then_returns_false(
        self,
        target_dir: Path,
    ) -> None:
        installer = LocalSkillInstaller(target_dir=target_dir)
        skill = SkillDef(name="ghost", source="/no/such/file.md")
        result = installer.install(skill)
        assert result is False

    @pytest.mark.integration
    def test_install_when_target_dir_does_not_exist_then_creates_it(
        self,
        skills_dir: Path,
        tmp_path: Path,
    ) -> None:
        new_target = tmp_path / "new-dir" / "skills"
        skill_file = skills_dir / "new-skill.md"
        skill_file.write_text("# New skill")
        installer = LocalSkillInstaller(target_dir=new_target)
        skill = SkillDef(name="new-skill", source=str(skill_file))
        result = installer.install(skill)
        assert result is True
        assert (new_target / "new-skill" / "SKILL.md").exists()

    @pytest.mark.integration
    def test_install_when_skill_already_exists_then_overwrites(
        self,
        skills_dir: Path,
        target_dir: Path,
    ) -> None:
        existing = target_dir / "existing-skill" / "SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("# Old content")
        skill_file = skills_dir / "existing-skill.md"
        skill_file.write_text("# New content")
        installer = LocalSkillInstaller(target_dir=target_dir)
        skill = SkillDef(name="existing-skill", source=str(skill_file))
        result = installer.install(skill)
        assert result is True
        assert existing.read_text() == "# New content"


class TestIntegrationLocalSkillInstaller:
    @pytest.mark.integration
    def test_install_multiple_skills_all_succeed(
        self,
        skills_dir: Path,
        target_dir: Path,
    ) -> None:
        (skills_dir / "a.md").write_text("---\nname: skill-a\n---\n# Skill A")
        (skills_dir / "b.md").write_text("---\nname: skill-b\n---\n# Skill B")
        installer = LocalSkillInstaller(target_dir=target_dir)
        failed = _install_local_skills(installer, skills_dir)
        assert failed == []
        assert (
            target_dir / "skill-a" / "SKILL.md"
        ).read_text() == "---\nname: skill-a\n---\n# Skill A"
        assert (
            target_dir / "skill-b" / "SKILL.md"
        ).read_text() == "---\nname: skill-b\n---\n# Skill B"

    @pytest.mark.integration
    def test_install_when_source_missing_md_file_then_returns_failed(
        self,
        skills_dir: Path,
        target_dir: Path,
    ) -> None:
        (skills_dir / "broken.md").write_text("---\nname: broken\n---\nContent")
        broken_path = skills_dir / "broken.md"
        installer = LocalSkillInstaller(target_dir=target_dir)
        skill = SkillDef(name="broken", source=str(broken_path))
        broken_path.unlink()
        result = installer.install(skill)
        assert result is False

    @pytest.mark.integration
    def test_source_not_a_directory_returns_empty(self, tmp_path: Path) -> None:
        from ai_toolkit.install_skills.parsing.list_local_skills import (
            list_local_skills,
        )

        not_a_dir = tmp_path / "not-a-dir"
        skills = list_local_skills(not_a_dir)
        assert skills == []


def _install_local_skills(
    installer: LocalSkillInstaller,
    source_dir: Path,
) -> list[str]:
    from ai_toolkit.install_skills.parsing.list_local_skills import (
        list_local_skills,
    )

    skills = list_local_skills(source_dir)
    failed: list[str] = []
    for skill in skills:
        if not installer.install(skill):
            failed.append(skill.name)
    return failed
