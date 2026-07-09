import os
from pathlib import Path

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.dotenv import load_dotenv


def check_mcp_secrets(
    servers: list[McpServerDef],
    dotenv_path: Path | None = None,
) -> list[str]:
    dotenv_vars: dict[str, str] = {}
    if dotenv_path is not None:
        dotenv_vars = load_dotenv(dotenv_path)

    missing: list[str] = []

    for server in servers:
        if server.disabled:
            continue
        for key, _value in server.env:
            runtime_value = os.environ.get(key)
            file_value = dotenv_vars.get(key)
            real_value = runtime_value if runtime_value else file_value
            if not real_value:
                missing.append(key)

    return missing
