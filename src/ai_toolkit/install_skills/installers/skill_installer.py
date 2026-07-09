from typing import Protocol

from ai_toolkit.install_skills.models.skill_def import SkillDef


class SkillInstaller(Protocol):
    def install(self, skill: SkillDef) -> bool: ...
