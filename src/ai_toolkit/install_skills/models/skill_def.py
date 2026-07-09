from dataclasses import dataclass


@dataclass(frozen=True)
class SkillDef:
    name: str
    source: str
