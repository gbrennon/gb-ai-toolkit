import pytest

from ai_toolkit.install_skills.parsing.group_remote_skills import group_remote_skills


class TestGroupRemoteSkills:
    @pytest.mark.unit
    def test_group_when_skills_have_full_https_urls_then_groups_by_repo(self) -> None:
        skills = [
            "https://github.com/a/b/tree/main/skills/x",
            "https://github.com/a/b/tree/main/skills/y",
            "https://github.com/c/d/tree/main/skills/z",
        ]
        result = group_remote_skills(skills)
        assert result == {
            "https://github.com/a/b": ["skills/x", "skills/y"],
            "https://github.com/c/d": ["skills/z"],
        }

    @pytest.mark.unit
    def test_group_when_skills_use_owner_repo_format_then_derives_github_url(self) -> None:
        skills = [
            "owner-a/repo-a/path/to/skill",
            "owner-a/repo-a/other/skill",
            "owner-b/repo-b/skill",
        ]
        result = group_remote_skills(skills)
        assert result == {
            "https://github.com/owner-a/repo-a": ["path/to/skill", "other/skill"],
            "https://github.com/owner-b/repo-b": ["skill"],
        }

    @pytest.mark.unit
    def test_group_when_skill_has_no_subpath_then_empty_string_skill_name(self) -> None:
        skills = ["owner/repo"]
        result = group_remote_skills(skills)
        assert result == {"https://github.com/owner/repo": [""]}

    @pytest.mark.unit
    def test_group_when_empty_list_then_returns_empty_dict(self) -> None:
        result = group_remote_skills([])
        assert result == {}
