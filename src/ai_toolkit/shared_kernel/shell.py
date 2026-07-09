import subprocess
from shutil import which


def shell_command_exists(command: str) -> bool:
    return which(command) is not None


def run_command(command: list[str]) -> bool:
    result = subprocess.run(command, check=False, stdin=subprocess.DEVNULL)
    return result.returncode == 0
