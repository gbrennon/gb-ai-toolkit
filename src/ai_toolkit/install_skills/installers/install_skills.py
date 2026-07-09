from pathlib import Path

from ai_toolkit.install_skills.models.skill_def import SkillDef
from ai_toolkit.install_skills.installers.skill_installer import SkillInstaller
from ai_toolkit.install_skills.parsing.group_remote_skills import group_remote_skills
from ai_toolkit.install_skills.parsing.list_local_skills import list_local_skills


def install_remote_skills(
    installer: SkillInstaller,
    skills: list[str],
) -> list[str]:
    repo_groups = group_remote_skills(skills)
    failed: list[str] = []

    for repo, skill_names in repo_groups.items():
        for skill_name in skill_names:
            skill = SkillDef(name=skill_name, source=repo)
            if not installer.install(skill):
                failed.append(f"{repo}/{skill_name}")

    return failed


def install_local_skills(
    installer: SkillInstaller,
    source_dir: Path,
) -> list[str]:
    skills = list_local_skills(source_dir)
    failed: list[str] = []

    for skill in skills:
        if not installer.install(skill):
            failed.append(skill.name)

    return failed
