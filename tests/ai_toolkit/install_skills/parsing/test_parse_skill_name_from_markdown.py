import pytest

from ai_toolkit.install_skills.parsing.parse_skill_name_from_markdown import (
    parse_skill_name_from_markdown,
)


class TestParseSkillNameFromMarkdown:
    @pytest.mark.unit
    def test_parse_when_frontmatter_has_name_then_returns_name(self) -> None:
        content = "---\nname: my-skill\ndescription: foo\n---\n# Content"
        result = parse_skill_name_from_markdown(content, "some-file.md")
        assert result == "my-skill"

    @pytest.mark.unit
    def test_parse_when_no_frontmatter_then_uses_filename(self) -> None:
        content = "# Just content\n\nNo frontmatter here."
        result = parse_skill_name_from_markdown(content, "my-local-skill.md")
        assert result == "my-local-skill"

    @pytest.mark.unit
    def test_parse_when_frontmatter_missing_name_field_then_falls_back_to_filename(
        self,
    ) -> None:
        content = "---\ndescription: no name field\n---\n# Content"
        result = parse_skill_name_from_markdown(content, "fallback-name.md")
        assert result == "fallback-name"

    @pytest.mark.unit
    def test_parse_when_frontmatter_name_has_extra_whitespace_then_strips(self) -> None:
        content = "---\nname:   spaced-out   \ndescription: foo\n---\n"
        result = parse_skill_name_from_markdown(content, "file.md")
        assert result == "spaced-out"
