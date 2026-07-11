from pathlib import Path

import pytest

from ai_toolkit.install_omp_commands.main import install


class TestInstallOmpCommands:
    @pytest.mark.integration
    def test_install_writes_both_files(self, tmp_path: Path) -> None:
        cmd_dir = tmp_path / "commands"
        scr_dir = tmp_path / "scripts"
        rc = install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        assert rc == 0
        assert (cmd_dir / "cline-auth.md").is_file()
        assert (scr_dir / "cline-auth-check.sh").is_file()

    @pytest.mark.integration
    def test_script_is_executable(self, tmp_path: Path) -> None:
        cmd_dir = tmp_path / "commands"
        scr_dir = tmp_path / "scripts"
        install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        scr = scr_dir / "cline-auth-check.sh"
        assert scr.is_file()
        assert scr.stat().st_mode & 0o111  # executable bit set

    @pytest.mark.integration
    def test_command_contains_bash_call(self, tmp_path: Path) -> None:
        cmd_dir = tmp_path / "commands"
        scr_dir = tmp_path / "scripts"
        install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        content = (cmd_dir / "cline-auth.md").read_text(encoding="utf-8")
        assert "cline-auth-check.sh" in content
        assert "$ARGUMENTS" in content

    @pytest.mark.integration
    def test_script_contains_expected_check(self, tmp_path: Path) -> None:
        cmd_dir = tmp_path / "commands"
        scr_dir = tmp_path / "scripts"
        install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        content = (scr_dir / "cline-auth-check.sh").read_text(encoding="utf-8")
        assert "providers.json" in content
        assert "workos:" in content
        assert "cline auth cline" in content

    @pytest.mark.integration
    def test_install_idempotent(self, tmp_path: Path) -> None:
        cmd_dir = tmp_path / "commands"
        scr_dir = tmp_path / "scripts"
        install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        rc = install(commands_dir=cmd_dir, scripts_dir=scr_dir)
        assert rc == 0
