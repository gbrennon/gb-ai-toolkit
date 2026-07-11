import shutil
from pathlib import Path

from ai_toolkit.install_skills.models.skill_def import SkillDef


class LocalSkillInstaller:
    def __init__(self, target_dir: Path) -> None:
        self._target_dir = target_dir

    def install(self, skill: SkillDef) -> bool:
        source_path = Path(skill.source)

        if not source_path.exists():
            print(f"Local skill source not found: {source_path}")
            return False

        target_skill_dir = self._target_dir / skill.name
        target_skill_dir.mkdir(parents=True, exist_ok=True)

        target_file = target_skill_dir / "SKILL.md"
        shutil.copy2(source_path, target_file)

        print(f"Installed local skill: {skill.name}")
        return True
