from ai_toolkit.install_agent_rules.models.agent_rule import AgentRule
from ai_toolkit.install_agent_rules.parsing.compose_rules import (
    compose_rules_content,
)


class TestComposeRulesContent:
    def test_with_multiple_rules_then_includes_all_in_order(self) -> None:
        rules = [
            AgentRule(content="# Base\n\nContent A", order=0, name="base"),
            AgentRule(content="# Tools\n\nContent B", order=10, name="tools"),
        ]
        result = compose_rules_content(rules, "test/source")
        assert "# Base" in result
        assert "# Tools" in result
        assert "Content A" in result
        assert "Content B" in result

    def test_with_header_always_present(self) -> None:
        rules = [
            AgentRule(content="# Only", order=0, name="only"),
        ]
        result = compose_rules_content(rules, "some/path")
        assert "# Agent Rules" in result
        assert "# Source: some/path" in result

    def test_with_empty_rules_list_then_returns_header_only(self) -> None:
        result = compose_rules_content([], "empty/path")
        assert "# Agent Rules" in result