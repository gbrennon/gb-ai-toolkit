from pathlib import Path

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.parsing.parse_skill_name_from_markdown import (
    parse_skill_name_from_markdown,
)


def list_local_skills(source_dir: Path) -> list[SkillDef]:
    if not source_dir.is_dir():
        return []

    skills: list[SkillDef] = []

    for md_file in sorted(source_dir.glob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        name = parse_skill_name_from_markdown(content, md_file.name)
        skills.append(SkillDef(name=name, source=str(md_file)))

    return skills
