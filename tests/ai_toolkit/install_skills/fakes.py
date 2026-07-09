from pathlib import Path

from ai_toolkit.install_skills.models.skill_def import SkillDef


class FakeNpxInstaller:
    def __init__(self) -> None:
        self.installed: list[SkillDef] = []
        self.fail_on: list[str] = []

    def install(self, skill: SkillDef) -> bool:
        self.installed.append(skill)
        return skill.name not in self.fail_on


class FakeCopierInstaller:
    def __init__(self) -> None:
        self.installed: list[SkillDef] = []
        self.copied_to: list[Path] = []
        self.fail_on: list[str] = []

    def install(self, skill: SkillDef) -> bool:
        self.installed.append(skill)
        if skill.name in self.fail_on:
            return False
        self.copied_to.append(Path(skill.source + "_copy"))
        return True
