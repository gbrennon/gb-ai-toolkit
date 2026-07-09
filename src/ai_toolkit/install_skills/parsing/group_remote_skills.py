from collections import defaultdict


def group_remote_skills(skills: list[str]) -> dict[str, list[str]]:
    repo_to_skills: dict[str, list[str]] = defaultdict(list)

    for skill in skills:
        if skill.startswith("https://github.com/"):
            parts = skill.split("/")
            repo = "/".join(parts[:5])
            skill_path_parts = parts[5:]
            non_branch: list[str] = []
            i = 0
            while i < len(skill_path_parts):
                if skill_path_parts[i] == "tree" and i + 1 < len(skill_path_parts):
                    i += 2
                else:
                    non_branch.append(skill_path_parts[i])
                    i += 1
            skill_name = "/".join(non_branch)
        else:
            parts = skill.split("/")
            if len(parts) >= 3:
                repo = f"https://github.com/{parts[0]}/{parts[1]}"
                skill_name = "/".join(parts[2:])
            else:
                repo = f"https://github.com/{parts[0]}/{parts[1]}"
                skill_name = ""

        repo_to_skills[repo].append(skill_name)

    return repo_to_skills
