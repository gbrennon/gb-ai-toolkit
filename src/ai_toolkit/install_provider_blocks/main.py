"""Install Provider Blocks — block OpenAI & Anthropic providers on OMP and Cline.

Blocks OpenAI and Anthropic access on both agents by:
  - Adding to disabledProviders in ~/.omp/agent/models.yml       (OMP)
  - Removing provider entries from ~/.cline/data/settings/providers.json (Cline)

No API keys or .env configuration needed — just run and they're blocked.
"""

import json
import sys
from pathlib import Path

import yaml

OMP_MODELS_PATH = Path.home() / ".omp" / "agent" / "models.yml"
CLINE_PROVIDERS_PATH = Path.home() / ".cline" / "data" / "settings" / "providers.json"

_BLOCKED_PROVIDERS = ("openai", "anthropic")


def _read_yaml(path: Path) -> dict:
    """Read and parse a YAML file. Returns empty dict if missing or invalid."""
    if not path.is_file():
        return {}
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        print(f"Warning: {path} is invalid YAML, starting fresh")
        return {}


def _write_yaml(path: Path, data: dict) -> bool:
    """Write data as YAML to path. Creates directories as needed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            yaml.dump(data, default_flow_style=False, allow_unicode=True),
            encoding="utf-8",
        )
        return True
    except OSError as e:
        print(f"Error writing {path}: {e}", file=sys.stderr)
        return False


def _read_json(path: Path) -> dict:
    """Read and parse a JSON file. Returns empty dict if missing or invalid."""
    if not path.is_file():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"Warning: {path} is invalid JSON, starting fresh")
        return {}


def _write_json(path: Path, data: dict) -> bool:
    """Write data as JSON to path. Creates directories as needed."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return True
    except OSError as e:
        print(f"Error writing {path}: {e}", file=sys.stderr)
        return False


def _block_omp_providers(models_path: Path) -> bool:
    """Block OpenAI and Anthropic in OMP by adding them to disabledProviders."""
    try:
        data = _read_yaml(models_path)
        disabled: list[str] = data.get("disabledProviders", [])

        newly_blocked: list[str] = []
        for provider in _BLOCKED_PROVIDERS:
            if provider not in disabled:
                disabled.append(provider)
                newly_blocked.append(provider)

        if newly_blocked:
            data["disabledProviders"] = disabled
            print(f"  OMP: blocked {', '.join(newly_blocked)}")
        else:
            print("  OMP: openai + anthropic already blocked")

        return _write_yaml(models_path, data)
    except Exception as e:
        print(f"Error updating OMP models.yml: {e}", file=sys.stderr)
        return False


def _block_cline_providers(providers_path: Path) -> bool:
    """Block OpenAI and Anthropic in Cline by removing them from providers."""
    try:
        data = _read_json(providers_path)
        if not data:
            print("  Cline: no providers.json found, nothing to block")
            return True

        providers: dict = data.get("providers", {})
        removed: list[str] = []
        for provider in _BLOCKED_PROVIDERS:
            if provider in providers:
                del providers[provider]
                removed.append(provider)

        if removed:
            data["providers"] = providers
            print(f"  Cline: blocked {', '.join(removed)}")
            return _write_json(providers_path, data)
        else:
            print("  Cline: openai + anthropic already blocked (or never configured)")
            return True
    except Exception as e:
        print(f"Error updating Cline providers.json: {e}", file=sys.stderr)
        return False


def install(
    omp_models_path: Path | None = None,
    cline_providers_path: Path | None = None,
) -> int:
    """Block OpenAI and Anthropic providers on OMP and Cline."""
    omp_models = omp_models_path or OMP_MODELS_PATH
    cline_providers = cline_providers_path or CLINE_PROVIDERS_PATH

    print("\nBlocking OpenAI and Anthropic providers...")
    errors: list[str] = []

    if not _block_omp_providers(omp_models):
        errors.append("Failed to block OMP providers")

    if not _block_cline_providers(cline_providers):
        errors.append("Failed to block Cline providers")

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        return 1

    print("\nDone. OpenAI and Anthropic are now blocked on OMP and Cline.")
    return 0


def main() -> int:
    return install()


if __name__ == "__main__":
    sys.exit(main())
