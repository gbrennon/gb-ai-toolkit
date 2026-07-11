import argparse
import sys
from pathlib import Path

from ai_toolkit.install_agent_rules.installers.install_agent_rules import (
    AGENT_RULES_TARGET,
    install_agent_rules,
)
from ai_toolkit.install_agent_rules.parsing.load_rules_dir import read_rules_dir

_DEV_RULES_DIR = Path("agent_rules")
_GLOBAL_RULES_DIR = Path.home() / ".config" / "ai-toolkit" / "rules.d"


def _persist_to_global(source: Path, global_dir: Path | None = None) -> int:
    target_dir = global_dir or _GLOBAL_RULES_DIR
    files = read_rules_dir(source)
    if not files:
        print(f"No rules found in {source}")
        return 1
    target_dir.mkdir(parents=True, exist_ok=True)
    for filename, content in files.items():
        dest = target_dir / filename
        dest.write_text(content, encoding="utf-8")
        print(f"  {filename} -> {dest}")
    print(f"\nPersisted {len(files)} rules to {target_dir}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compose and install agent rules into AGENT.md",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=_DEV_RULES_DIR,
        help=f"Source rules.d directory (default: {_DEV_RULES_DIR})",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=AGENT_RULES_TARGET,
        help=f"Target AGENT.md path (default: {AGENT_RULES_TARGET})",
    )
    parser.add_argument(
        "--persist",
        action="store_true",
        help=f"Copy rules to global {_GLOBAL_RULES_DIR} before composing",
    )
    args = parser.parse_args(argv)

    source = args.source

    if args.persist:
        if ret := _persist_to_global(source):
            return ret
        source = _GLOBAL_RULES_DIR

    return install_agent_rules(source_dir=source, target_path=args.target)


if __name__ == "__main__":
    sys.exit(main())
