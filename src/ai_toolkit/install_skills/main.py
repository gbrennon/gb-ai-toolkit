import sys
from pathlib import Path

from ai_toolkit.shared_kernel.shell import shell_command_exists
from ai_toolkit.install_skills.installers.skill_installer import SkillInstaller
from ai_toolkit.install_skills.installers.npx_skill_installer import NpxSkillInstaller
from ai_toolkit.install_skills.installers.local_skill_installer import (
    LocalSkillInstaller,
)
from ai_toolkit.install_skills.installers.update_skills import update_skills
from ai_toolkit.install_skills.installers.install_skills import (
    install_remote_skills,
    install_local_skills,
)
from ai_toolkit.install_skills.parsing.load_skills_yaml import load_skills_yaml


def main() -> int:
    skills_yaml = Path("skills.yaml")
    local_source = Path("skills")
    local_target = Path.home() / ".agents" / "skills"

    if not skills_yaml.exists():
        print("skills.yaml not found")
        return 1

    if not shell_command_exists("npx"):
        print("npx not available")
        return 1

    if not update_skills():
        print("Failed to update skills")
        return 1

    raw_skills = load_skills_yaml(skills_yaml)
    remote_installer: SkillInstaller = NpxSkillInstaller()

    failed: list[str] = list(install_remote_skills(remote_installer, raw_skills))

    if local_source.is_dir():
        local_installer: SkillInstaller = LocalSkillInstaller(target_dir=local_target)
        failed.extend(install_local_skills(local_installer, local_source))

    if failed:
        print("\nFailed installations:")
        for skill in failed:
            print(f" - {skill}")
        return 1

    print("\nAll skills installed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
