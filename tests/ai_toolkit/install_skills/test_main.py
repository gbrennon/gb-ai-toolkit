from pathlib import Path
from unittest.mock import patch

import pytest

from ai_toolkit.install_skills.main import main


class TestMain:
    @pytest.mark.unit
    def test_main_when_skills_yaml_missing_then_returns_one(self, tmp_path: Path) -> None:
        with patch("ai_toolkit.install_skills.main.Path") as mock_path:
            mock_skills_yaml = tmp_path / "skills.yaml"
            mock_path.return_value = mock_skills_yaml
            result = main()
            assert result == 1

    @pytest.mark.unit
    def test_main_when_npx_not_available_then_returns_one(
        self,
        tmp_path: Path,
    ) -> None:
        skills_yaml = tmp_path / "skills.yaml"
        skills_yaml.write_text("skills: []\n")
        with (
            patch(
                "ai_toolkit.install_skills.main.Path",
                return_value=skills_yaml,
            ),
            patch(
                "ai_toolkit.install_skills.main.shell_command_exists",
                return_value=False,
            ),
        ):
            result = main()
            assert result == 1

    @pytest.mark.unit
    def test_main_when_update_fails_then_returns_one(self, tmp_path: Path) -> None:
        skills_yaml = tmp_path / "skills.yaml"
        skills_yaml.write_text("skills: []\n")
        with (
            patch(
                "ai_toolkit.install_skills.main.Path",
                return_value=skills_yaml,
            ),
            patch(
                "ai_toolkit.install_skills.main.shell_command_exists",
                return_value=True,
            ),
            patch(
                "ai_toolkit.install_skills.main.update_skills",
                return_value=False,
            ),
        ):
            result = main()
            assert result == 1

    @pytest.mark.unit
    def test_main_when_all_succeed_then_returns_zero(self, tmp_path: Path) -> None:
        skills_yaml = tmp_path / "skills.yaml"
        skills_yaml.write_text("skills: []\n")
        with (
            patch(
                "ai_toolkit.install_skills.main.Path",
                return_value=skills_yaml,
            ),
            patch(
                "ai_toolkit.install_skills.main.shell_command_exists",
                return_value=True,
            ),
            patch(
                "ai_toolkit.install_skills.main.update_skills",
                return_value=True,
            ),
            patch(
                "ai_toolkit.install_skills.main.NpxSkillInstaller",
            ) as mock_npx,
            patch(
                "ai_toolkit.install_skills.main.LocalSkillInstaller",
            ),
            patch("ai_toolkit.install_skills.main.Path.is_dir"),
            patch("ai_toolkit.install_skills.main.Path.home"),
        ):
            mock_npx_instance = mock_npx.return_value
            mock_npx_instance.install.return_value = True
            result = main()
            assert result == 0
