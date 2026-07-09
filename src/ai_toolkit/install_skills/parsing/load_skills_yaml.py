from pathlib import Path

import yaml


def load_skills_yaml(file_path: Path) -> list[str]:
    with file_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    skills = data.get("skills")

    if not isinstance(skills, list):
        raise ValueError("skills must be a list")

    return [str(s) for s in skills]
