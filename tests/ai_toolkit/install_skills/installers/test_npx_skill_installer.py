import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.installers.npx_skill_installer import NpxSkillInstaller


class TestNpxSkillInstaller:
    @pytest.mark.unit
    def test_npx_install_when_subprocess_succeeds_then_returns_true(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            installer = NpxSkillInstaller()
            skill = SkillDef(
                name="test-skill",
                source="https://github.com/owner/repo",
            )
            result = installer.install(skill)
            assert result is True
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "skills",
                    "add",
                    "https://github.com/owner/repo",
                    "--skill",
                    "test-skill",
                    "-g",
                    "-y",
                ],
                check=False,
                stdin=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_npx_install_when_subprocess_fails_then_returns_false(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            installer = NpxSkillInstaller(npx_command="npx")
            skill = SkillDef(
                name="fail-skill",
                source="https://github.com/owner/repo",
            )
            result = installer.install(skill)
            assert result is False

    @pytest.mark.unit
    def test_npx_install_when_custom_npx_path_uses_it(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            installer = NpxSkillInstaller(npx_command="/custom/npx")
            skill = SkillDef(
                name="skill",
                source="https://github.com/owner/repo",
            )
            installer.install(skill)
            cmd = mock_run.call_args[0][0]
            assert cmd[0] == "/custom/npx"

    @pytest.mark.unit
    def test_npx_install_when_skill_in_subdirectory_then_extracts_basename(
        self,
    ) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            installer = NpxSkillInstaller()
            skill = SkillDef(
                name="engineering/improve-codebase-architecture",
                source="https://github.com/owner/repo",
            )
            result = installer.install(skill)
            assert result is True
            mock_run.assert_called_once_with(
                [
                    "npx",
                    "skills",
                    "add",
                    "https://github.com/owner/repo",
                    "--skill",
                    "improve-codebase-architecture",
                    "-g",
                    "-y",
                ],
                check=False,
                stdin=subprocess.DEVNULL,
            )
