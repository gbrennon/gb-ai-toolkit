import json
import os
from pathlib import Path

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from ai_toolkit.shared_kernel.dotenv import load_dotenv

_PLACEHOLDER_KEYWORDS = frozenset({
    "placeholder",
    "YOUR_",
    "REPLACE_ME",
    "TOKEN_HERE",
    "PASTE_",
})


def _is_placeholder(value: str) -> bool:
    lower = value.lower()
    return any(kw.lower() in lower for kw in _PLACEHOLDER_KEYWORDS)


class HttpMcpInstaller:
    def __init__(self, dotenv_path: Path | None = None) -> None:
        self._dotenv: dict[str, str] = {}
        if dotenv_path and dotenv_path.is_file():
            self._dotenv = load_dotenv(dotenv_path)

    def install(self, server: McpServerDef) -> bool:
        url = server.url or "(no url)"

        if not server.env:
            print(
                f"MCP server '{server.name}' is streamableHttp ({url}) — "
                f"no local install needed"
            )
            return True

        for key, raw_value in server.env:
            real_value = os.environ.get(key) or self._dotenv.get(key)
            if real_value and not _is_placeholder(real_value):
                print(
                    f"MCP server '{server.name}' is streamableHttp ({url}) — "
                    f"no local install needed (secret '{key}' found)"
                )
                return True

        print(
            f"MCP server '{server.name}' is streamableHttp ({url}) — "
            f"no local install needed (secrets unresolved in env)"
        )
        return True
