"""Install OMP Commands — install Cline auth check command + script into ~/.omp/agent/."""

from pathlib import Path

from ai_toolkit.install_omp_commands.main import main

__all__ = ["main", "OMP_COMMANDS_DIR", "OMP_SCRIPTS_DIR"]

OMP_COMMANDS_DIR: Path = Path.home() / ".omp" / "agent" / "commands"
OMP_SCRIPTS_DIR: Path = Path.home() / ".omp" / "agent" / "scripts"
