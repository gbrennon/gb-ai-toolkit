from pathlib import Path

import pytest

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.installers.install_skills import (
    install_remote_skills,
    install_local_skills,
)
from tests.ai_toolkit.install_skills.fakes import (
    FakeCopierInstaller,
    FakeNpxInstaller,
)


class TestInstallRemoteSkills:
    @pytest.mark.unit
    def test_install_when_all_succeed_then_returns_empty(
        self,
        fake_npx: FakeNpxInstaller,
    ) -> None:
        skills = ["owner/repo/skill-a", "owner/repo/skill-b"]
        failed = install_remote_skills(fake_npx, skills)
        assert failed == []
        assert fake_npx.installed == [
            SkillDef(name="skill-a", source="https://github.com/owner/repo"),
            SkillDef(name="skill-b", source="https://github.com/owner/repo"),
        ]

    @pytest.mark.unit
    def test_install_when_some_fail_then_returns_failed_list(
        self,
        fake_npx: FakeNpxInstaller,
    ) -> None:
        fake_npx.fail_on = ["skill-b"]
        skills = ["owner/repo/skill-a", "owner/repo/skill-b"]
        failed = install_remote_skills(fake_npx, skills)
        assert failed == ["https://github.com/owner/repo/skill-b"]

    @pytest.mark.unit
    def test_install_when_empty_then_returns_empty(
        self,
        fake_npx: FakeNpxInstaller,
    ) -> None:
        failed = install_remote_skills(fake_npx, [])
        assert failed == []


class TestInstallLocalSkills:
    @pytest.mark.unit
    def test_install_when_all_succeed_then_returns_empty(
        self,
        skills_dir: Path,
        fake_copier: FakeCopierInstaller,
    ) -> None:
        (skills_dir / "a.md").write_text("---\nname: a\n---\n")
        (skills_dir / "b.md").write_text("---\nname: b\n---\n")
        failed = install_local_skills(fake_copier, skills_dir)
        assert failed == []

    @pytest.mark.unit
    def test_install_when_some_fail_then_returns_failed_list(
        self,
        skills_dir: Path,
        fake_copier: FakeCopierInstaller,
    ) -> None:
        fake_copier.fail_on = ["a"]
        (skills_dir / "a.md").write_text("---\nname: a\n---\n")
        (skills_dir / "b.md").write_text("---\nname: b\n---\n")
        failed = install_local_skills(fake_copier, skills_dir)
        assert failed == ["a"]

    @pytest.mark.unit
    def test_install_when_no_skills_then_returns_empty(
        self,
        skills_dir: Path,
        fake_copier: FakeCopierInstaller,
    ) -> None:
        failed = install_local_skills(fake_copier, skills_dir)
        assert failed == []
