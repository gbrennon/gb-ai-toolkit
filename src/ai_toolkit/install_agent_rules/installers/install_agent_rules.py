from pathlib import Path

from ai_toolkit.install_agent_rules.parsing.compose_rules import (
    compose_rules_to_file,
)
from ai_toolkit.install_agent_rules.parsing.load_rules_dir import (
    load_rules_entries,
    read_rules_dir,
)

_GLOBAL_RULES_DIR = Path.home() / ".config" / "ai-toolkit" / "rules.d"

AGENT_RULES_TARGET = Path.home() / ".agents" / "AGENT.md"


def install_agent_rules(
    source_dir: Path | None = None,
    target_path: Path | None = None,
) -> int:
    rules_dir = source_dir or _GLOBAL_RULES_DIR
    target = target_path or AGENT_RULES_TARGET

    files = read_rules_dir(rules_dir)
    if not files:
        print(f"No rules found in {rules_dir}")
        return 1

    rules = load_rules_entries(files)
    compose_rules_to_file(rules, str(rules_dir), target)
    print(f"Composed {len(rules)} rules into {target}")
    return 0