# MCP Servers

## Overview

The project manages MCP (Model Context Protocol) servers through a single
`mcp/mcp.json` configuration file. Running `make install-mcp` (or `make deploy-mcp`)
will:

1. **Verify** each server's runtime command is available on `$PATH`
2. **Install** packages via npx, uvx, opencode, pi-install, or vibe-install
3. **Deploy** the rendered config to every supported agent's settings file

## Configuration file: `mcp/mcp.json`

The file has one top-level key, `mcpServers`, containing named server entries:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "package-name"],
      "env": { "SECRET": "{{ SECRET or 'YOUR_SECRET_HERE' }}" },
      "disabled": false
    }
  }
}
```

### Server entry fields

| Field | Required | Description |
|-------|----------|-------------|
| `command` | yes* | Runtime: `"npx"`, `"uvx"`, or a custom binary name |
| `args` | no | Positional arguments passed to the command |
| `type` | no | Set to `"streamableHttp"` for HTTP-based servers |
| `url` | no | Base URL for streamableHttp servers |
| `headers` | no | HTTP headers (supports Jinja2 templating) |
| `env` | no | Environment variables (supports Jinja2 templating) |
| `disabled` | no | Skip this server when `true` (default: `false`) |
| `platform` | no | Scopes the server to a single agent platform |
| `autoApprove` | no | List of tool names to auto-approve (agent-specific) |

\* Not required when `type` is `"streamableHttp"`.

### Jinja2 templating

Values in `env` and `headers` support Jinja2 expressions. The template context
includes all OS environment variables **and** variables from `.env`:

```json
"env": {
  "GITHUB_TOKEN": "{{ GITHUB_TOKEN or 'YOUR_GITHUB_TOKEN_HERE' }}"
}
```

If the variable is set in the environment or `.env`, the real value is used.
Otherwise the fallback string after `or` is kept as-is.

## Supported agent platforms

| Platform | Enum value | Config path | Install command |
|----------|-----------|-------------|-----------------|
| Cline | *(none — default)* | `~/.cline/data/settings/cline_mcp_settings.json` | npx / uvx / custom |
| OpenCode | `"opencode"` | `~/.config/opencode/mcp.json` | `opencode install <pkg>` |
| Pi | `"pi"` | `~/.config/pi/mcp.json` | `pi-install --arm <pkg>` |
| Vibe | `"vibe"` | `~/.config/vibe/mcp.json` | `vibe-install --resolve <pkg>` |

### How deployment works

- Servers **without** a `platform` field are **shared** — deployed to every agent's config file.
- Servers **with** a `platform` field are **scoped** — only deployed to that agent.
- A server with `"platform": "opencode"` will never appear in Pi or Vibe configs.

## Platform-scoped server example

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"],
      "disabled": false
    },
    "opencode-only-tool": {
      "command": "npx",
      "args": ["-y", "@some/opencode-package"],
      "platform": "opencode"
    }
  }
}
```

Here `fetch` deploys to **all** agents, while `opencode-only-tool` only deploys
to `~/.config/opencode/mcp.json`.

## Secrets check

Before deploying, `make install-mcp` scans all server `env` entries for
unresolved placeholders (values containing `YOUR_`, `TOKEN_HERE`, `REPLACE_ME`,
`PASTE_`, or `placeholder`). Any found are printed as a warning — add them to
`.env` or your environment to resolve.

## Running manually

```bash
# Default: mcp/mcp.json → ~/.cline/data/settings/cline_mcp_settings.json
uv run install-mcp-servers

# Custom paths
uv run python -c "
from ai_toolkit.install_mcp_servers.main import main
main(mcp_json_path='path/to/mcp.json', dotenv_path='.env.prod')
"
```
