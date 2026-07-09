from pathlib import Path

from ai_toolkit.install_agent_rules.models.agent_rule import AgentRule


_MARKER = "# Agent Rules — Composed by ai-toolkit"


def compose_rules_content(rules: list[AgentRule], source_label: str) -> str:
    parts: list[str] = [
        _MARKER,
        f"# Source: {source_label}",
        "",
    ]
    for rule in rules:
        parts.append(rule.content.rstrip("\n"))
        parts.append("")
    return "\n".join(parts) + "\n"


def compose_rules_to_file(
    rules: list[AgentRule],
    source_label: str,
    target: Path,
) -> None:
    content = compose_rules_content(rules, source_label)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")