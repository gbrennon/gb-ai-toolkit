import pytest

from ai_toolkit.install_skills.installers.skill_installer import SkillInstaller


class TestSkillInstaller:
    @pytest.mark.unit
    def test_protocol_when_class_implements_install_then_is_subtype(self) -> None:
        class ConcreteInstaller:
            def install(self, skill: object) -> bool:
                return True

        installer: SkillInstaller = ConcreteInstaller()
        assert installer.install(object()) is True
