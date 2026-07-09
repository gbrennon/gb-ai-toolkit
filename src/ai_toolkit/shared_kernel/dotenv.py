from pathlib import Path


def load_dotenv(env_path: Path) -> dict[str, str]:
    """Parse KEY=VALUE pairs from a .env file."""
    if not env_path.is_file():
        return {}

    result: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, _, value = stripped.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            result[key] = value
    return result
