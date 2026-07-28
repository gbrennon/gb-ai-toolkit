from collections import defaultdict


def group_remote_skills(skills: list[str]) -> dict[str, list[str]]:
    """Group skill references by their GitHub repository.

    Accepts full GitHub URLs (e.g. ``https://github.com/owner/repo/tree/main/skill``)
    and short-form references (e.g. ``owner/repo/skill``). Strips ``tree/<branch>``
    segments from URLs so the returned skill name points to the default branch.

    Returns a mapping of repository URL to the list of skill paths within it.
    """
    repo_to_skills: dict[str, list[str]] = defaultdict(list)

    for skill in skills:
        if skill.startswith("https://github.com/"):
            url_segments = skill.split("/")
            repository_url = "/".join(url_segments[:5])
            path_segments = url_segments[5:]
            skill_path_segments: list[str] = []
            segment_index = 0
            while segment_index < len(path_segments):
                if path_segments[segment_index] == "tree" and segment_index + 1 < len(
                    path_segments
                ):
                    segment_index += 2
                else:
                    skill_path_segments.append(path_segments[segment_index])
                    segment_index += 1
            skill_name = "/".join(skill_path_segments)
        else:
            url_segments = skill.split("/")
            if len(url_segments) >= 3:
                repository_url = (
                    f"https://github.com/{url_segments[0]}/{url_segments[1]}"
                )
                skill_name = "/".join(url_segments[2:])
            else:
                repository_url = (
                    f"https://github.com/{url_segments[0]}/{url_segments[1]}"
                )
                skill_name = ""

        repo_to_skills[repository_url].append(skill_name)

    return repo_to_skills
