import pytest

from ai_toolkit.install_skills.models.skill_def import SkillDef


class TestSkillDef:
    @pytest.mark.unit
    def test_construct_when_given_name_and_source_then_sets_attributes(self) -> None:
        skill = SkillDef(name="test-skill", source="/some/path")
        assert skill.name == "test-skill"
        assert skill.source == "/some/path"

    @pytest.mark.unit
    def test_immutable_when_constructed_then_cannot_modify(self) -> None:
        skill = SkillDef(name="fixed", source="/path")
        with pytest.raises(AttributeError):
            skill.name = "changed"  # pyright: ignore[reportAttributeAccessIssue]
