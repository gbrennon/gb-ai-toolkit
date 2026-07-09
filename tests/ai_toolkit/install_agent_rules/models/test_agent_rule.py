from ai_toolkit.install_agent_rules.models.agent_rule import AgentRule


class TestAgentRule:
    def test_fields_are_stored(self) -> None:
        rule = AgentRule(content="# Hello", order=5, name="hello")
        assert rule.content == "# Hello"
        assert rule.order == 5
        assert rule.name == "hello"