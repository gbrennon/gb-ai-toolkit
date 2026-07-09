import subprocess
from unittest.mock import patch

import pytest

from ai_toolkit.install_skills.installers.update_skills import update_skills


class TestUpdateSkills:
    @pytest.mark.unit
    def test_update_when_subprocess_succeeds_then_returns_true(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = update_skills()
            assert result is True
            mock_run.assert_called_once_with(
                ["npx", "skills", "update"],
                check=False,
                stdin=subprocess.DEVNULL,
            )

    @pytest.mark.unit
    def test_update_when_subprocess_fails_then_returns_false(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            result = update_skills()
            assert result is False
