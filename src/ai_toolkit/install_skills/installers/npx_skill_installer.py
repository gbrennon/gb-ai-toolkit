from pathlib import Path

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.shared_kernel.shell import run_command


class NpxSkillInstaller:
    def __init__(self, npx_command: str | None = None) -> None:
        self._npx_command = npx_command or "npx"

    def install(self, skill: SkillDef) -> bool:
        skill_name = Path(skill.name).name
        print(f"Installing {skill_name} from {skill.source}")
        return run_command(
            [
                self._npx_command,
                "skills",
                "add",
                skill.source,
                "--skill",
                skill_name,
                "-g",
                "-y",
            ]
        )
