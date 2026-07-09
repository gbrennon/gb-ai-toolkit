from unittest.mock import patch

import pytest

from ai_toolkit.shared_kernel.shell import shell_command_exists, run_command


class TestShellCommandExists:
    @pytest.mark.unit
    def test_shell_when_on_path_then_returns_true(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which") as mock_which:
            mock_which.return_value = "/usr/bin/python3"
            assert shell_command_exists("python3") is True
            mock_which.assert_called_once_with("python3")

    @pytest.mark.unit
    def test_shell_when_not_on_path_then_returns_false(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.which") as mock_which:
            mock_which.return_value = None
            assert shell_command_exists("nope") is False


class TestRunCommand:
    @pytest.mark.unit
    def test_run_when_subprocess_succeeds_then_returns_true(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            result = run_command(["echo", "hi"])
            assert result is True

    @pytest.mark.unit
    def test_run_when_subprocess_fails_then_returns_false(self) -> None:
        with patch("ai_toolkit.shared_kernel.shell.subprocess.run") as mock_run:
            mock_run.return_value.returncode = 1
            result = run_command(["false"])
            assert result is False
