import re
from pathlib import Path


def parse_skill_name_from_markdown(content: str, filename: str) -> str:
    match = re.search(r"^name:\s*(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return Path(filename).stem
