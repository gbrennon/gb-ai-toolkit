from pathlib import Path

import pytest

from ai_toolkit.install_mcp_servers.models.mcp_server_def import McpServerDef
from tests.ai_toolkit.install_mcp_servers.fixtures.fakes import FakeMcpInstaller


@pytest.fixture
def fake_installer() -> FakeMcpInstaller:
    return FakeMcpInstaller()


@pytest.fixture
def sample_mcp_json(tmp_path: Path) -> Path:
    content = """{
  "mcpServers": {
    "github": {
      "type": "streamableHttp",
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer YOUR_GITHUB_TOKEN_HERE"
      },
      "disabled": false,
      "autoApprove": []
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "disabled": false,
      "autoApprove": []
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "disabled": false,
      "autoApprove": []
    },
    "forgejo": {
      "command": "forgejo-mcp",
      "args": ["--transport", "stdio", "--url", "https://codeberg.org"],
      "env": {
        "FORGEJO_ACCESS_TOKEN": "YOUR_CODEBERG_TOKEN_HERE"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}"""
    p = tmp_path / "mcp.json"
    p.write_text(content)
    return p


@pytest.fixture
def mcp_dir(tmp_path: Path) -> Path:
    d = tmp_path / "mcp"
    d.mkdir()
    return d


@pytest.fixture
def npx_server() -> McpServerDef:
    """A basic npx server definition for installer tests."""
    return McpServerDef(
        name="test", command="npx", args=("pkg",), env=(),
        server_type=None, url=None, disabled=False,
    )


@pytest.fixture
def uvx_server() -> McpServerDef:
    return McpServerDef(
        name="fetch", command="uvx", args=("mcp-server-fetch",),
        env=(), server_type=None, url=None, disabled=False,
    )


@pytest.fixture
def http_server() -> McpServerDef:
    return McpServerDef(
        name="github", command=None, args=(), env=(),
        server_type="streamableHttp", url="https://api.githubcopilot.com/mcp/",
        disabled=False,
    )
