from pathlib import Path

from ai_toolkit.install_agent_rules.models.agent_rule import AgentRule


def load_rules_entries(
    files: dict[str, str],
) -> list[AgentRule]:
    rules: list[AgentRule] = []
    for filename in sorted(files):
        if not filename.endswith(".md"):
            continue
        stem = filename[:-3]
        order_str = stem[:2]
        if not order_str.isdigit():
            continue
        name = stem[3:]
        rules.append(
            AgentRule(content=files[filename], order=int(order_str), name=name)
        )
    return rules


def read_rules_dir(rules_dir: Path) -> dict[str, str]:
    if not rules_dir.is_dir():
        return {}
    files: dict[str, str] = {}
    for path in sorted(rules_dir.glob("[0-9][0-9]-*.md")):
        files[path.name] = path.read_text(encoding="utf-8")
    return files
