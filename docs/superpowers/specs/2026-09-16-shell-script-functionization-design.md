# Shell Script Functionization Design

## Goal

Refactor every tracked script in `scripts/` so that each is independently executable as a unit, with all runtime statements inside functions and no emoji or other non-ASCII symbols.

## Scope

The five scripts are:

- `scripts/check-code-quality.sh`
- `scripts/check-modified-code-quality.sh`
- `scripts/install-aliases.sh`
- `scripts/install-systemd.sh`
- `scripts/install_cline_rules.sh`

The shebang, comments, function definitions, and the final `main "$@"` invocation may remain at file scope. Runtime setup—including `set -euo pipefail`, constants, path discovery, argument parsing, and command execution—must occur from `main` or functions called by it.

## Design

Use a consistent structure:

```bash
#!/usr/bin/env bash

helper() {
  ...
}

main() {
  set -euo pipefail
  local ...
  ...
}

main "$@"
```

Each script retains its existing command-line interface, output meaning, and exit-status behavior. Distinct responsibilities remain in focused helpers. Configuration and derived paths are passed explicitly or scoped locally rather than initialized at file scope.

Replace all Unicode status marks, arrows, box-drawing characters, and emoji in script source and generated output with ASCII equivalents.

## Verification

- Run `bash -n` for all five scripts.
- Add or update tests to enforce ASCII-only script contents and the function-entry-point structure.
- Exercise implementation-equivalent paths under `tests/` instead of `src/` where a target path is needed (for example, `tests/app.py`).
- Smoke-test each script independently:
  - `check-code-quality.sh --help`
  - `check-modified-code-quality.sh` with no modified path
  - `install-aliases.sh` using a temporary `HOME`
  - `install-systemd.sh` using temporary directories and a mocked `systemctl`
  - `install_cline_rules.sh` using temporary source and destination directories
- Run the repository test suite.

## Compatibility and safety

Do not change installer destinations or quality-check semantics. Smoke tests must isolate filesystem and service-manager side effects with temporary directories or command stubs. A failing quality analysis must continue to propagate its nonzero status, while a missing modified-file path must remain a no-op.
