# Shell Script Functionization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor all five `scripts/*.sh` files so each is independently executable, all runtime statements are reached through `main`, and all output/source is ASCII-only.

**Architecture:** Preserve each script's existing CLI and side effects. Use focused helper functions for reusable responsibilities and a `main "$@"` entry point for runtime initialization and orchestration. Add focused Python subprocess tests for structural requirements and isolated smoke behavior.

**Tech Stack:** Bash, Python 3, pytest, existing `uv`/Makefile workflow.

## Global Constraints

- Runtime setup—including `set -euo pipefail`, constants, path discovery, argument parsing, and command execution—must occur from `main` or functions called by it.
- The shebang, comments, function definitions, and final `main "$@"` invocation may remain at file scope.
- Preserve command-line interfaces, output meaning, and exit-status behavior.
- Replace all Unicode status marks, arrows, box-drawing characters, and emoji with ASCII equivalents.
- Use `tests/...` paths for implementation-equivalent test targets instead of `src/...` paths.
- Isolate installer smoke tests with temporary directories and command stubs.

---

### Task 1: Add shell-script contract tests

**Files:**
- Create: `tests/scripts/test_shell_scripts.py`
- Test existing behavior: `tests/scripts/test_check_modified_code_quality.py`

**Interfaces:**
- Consumes: the five executable scripts in `scripts/`.
- Produces: pytest checks that the refactor tasks must satisfy.

- [ ] **Step 1: Write failing structural tests**

Create tests that enumerate the five scripts and assert:

```python
SCRIPT_NAMES = (
    "check-code-quality.sh",
    "check-modified-code-quality.sh",
    "install-aliases.sh",
    "install-systemd.sh",
    "install_cline_rules.sh",
)


def test_scripts_are_ascii_only() -> None:
    for script in scripts():
        script.read_text(encoding="ascii")


def test_scripts_have_main_entry_point() -> None:
    for script in scripts():
        text = script.read_text(encoding="ascii")
        assert "main()" in text
        assert text.rstrip().endswith("main \"$@\"")
```

Add a source-structure assertion that executable statements before `main()` are limited to the shebang, comments, blank lines, function definitions, and shell syntax needed for definitions. The test should specifically reject top-level assignments such as `SCRIPT_DIR=`, `REPO_ROOT=`, `FILES=(`, and `set -euo pipefail`.

- [ ] **Step 2: Run the new tests and verify the expected failures**

Run:

```bash
uv run pytest tests/scripts/test_shell_scripts.py -q
```

Expected: FAIL because the existing scripts lack `main()` or contain non-ASCII content.

- [ ] **Step 3: Commit the red tests**

```bash
git add tests/scripts/test_shell_scripts.py
git commit -m "test: define shell script structure" 
```

---

### Task 2: Functionize the quality checker

**Files:**
- Modify: `scripts/check-code-quality.sh`
- Test: `tests/scripts/test_shell_scripts.py`

**Interfaces:**
- Consumes: existing options and target-directory behavior.
- Produces: executable `check-code-quality.sh` with `main "$@"` and ASCII output.

- [ ] **Step 1: Move all runtime state into `main` or helper parameters**

Keep `usage`, `find_source_rules`, `resolve_semgrep_config`, `check_lizard`, and `check_semgrep` as helpers, changing them to accept needed directories/values as arguments. Move strict mode, path derivation, defaults, argument parsing, init handling, analyses, and final exit handling into `main`.

- [ ] **Step 2: Replace every non-ASCII source/output character**

Use ASCII messages such as `Lizard detected complexity violations`, `Lizard complexity analysis passed`, and `All code quality checks passed`; replace any remaining arrows or symbols in comments/messages.

- [ ] **Step 3: Run syntax and structural tests**

```bash
bash -n scripts/check-code-quality.sh
uv run pytest tests/scripts/test_shell_scripts.py -q
```

Expected: syntax succeeds and the quality-check script passes its structural assertions.

- [ ] **Step 4: Smoke-test the executable unit**

```bash
bash scripts/check-code-quality.sh --help
```

Expected: usage text and exit status `0`.

- [ ] **Step 5: Commit**

```bash
git add scripts/check-code-quality.sh tests/scripts/test_shell_scripts.py
git commit -m "refactor: functionize quality checker"
```

---

### Task 3: Functionize the modified-file quality wrapper

**Files:**
- Modify: `scripts/check-modified-code-quality.sh`
- Modify: `tests/scripts/test_check_modified_code_quality.py`

**Interfaces:**
- Consumes: JSON hook input on stdin and `check-code-quality PATH`.
- Produces: unchanged no-path no-op, output forwarding on failure, and checker status propagation.

- [ ] **Step 1: Preserve and extend tests using a `tests/...` target**

Change the representative event path from `src/app.py` to `tests/app.py`, and retain tests for success, failure output/status, and missing path.

- [ ] **Step 2: Run the wrapper tests to establish the pre-refactor baseline**

```bash
uv run pytest tests/scripts/test_check_modified_code_quality.py -q
```

Expected: existing behavior passes before structural refactoring.

- [ ] **Step 3: Move wrapper runtime into helpers and `main`**

Place strict mode, stdin reading, JSON parsing, checker execution, output printing, and final status return inside `main` or called helpers. End with `main "$@"`.

- [ ] **Step 4: Run focused tests and syntax checks**

```bash
bash -n scripts/check-modified-code-quality.sh
uv run pytest tests/scripts/test_check_modified_code_quality.py tests/scripts/test_shell_scripts.py -q
```

Expected: all focused tests pass.

- [ ] **Step 5: Smoke-test the no-op unit path**

```bash
printf '%s\n' '{"tool_input": {}}' | bash scripts/check-modified-code-quality.sh
```

Expected: no output and exit status `0`.

- [ ] **Step 6: Commit**

```bash
git add scripts/check-modified-code-quality.sh tests/scripts/test_check_modified_code_quality.py
git commit -m "refactor: functionize modified quality hook"
```

---

### Task 4: Functionize the installer scripts

**Files:**
- Modify: `scripts/install-aliases.sh`
- Modify: `scripts/install-systemd.sh`
- Modify: `scripts/install_cline_rules.sh`
- Test: `tests/scripts/test_shell_scripts.py`

**Interfaces:**
- Consumes: existing environment variables, filesystem layout, and system commands.
- Produces: independently executable installers with unchanged destinations and statuses.

- [ ] **Step 1: Add isolated smoke tests**

Add subprocess tests that:

- run `install-aliases.sh` with temporary `HOME` and assert the alias file contains the existing aliases;
- run `install-systemd.sh` with temporary `HOME`/`XDG_CONFIG_HOME`, a copied temporary `systemd/` fixture, and a fake `systemctl` that records calls;
- run `install_cline_rules.sh` with temporary HOME and fixture rule files, asserting files move to the Cline destination.

- [ ] **Step 2: Run the new smoke tests before refactoring**

```bash
uv run pytest tests/scripts/test_shell_scripts.py -q
```

Expected: structural tests fail because the scripts have not yet been refactored; installer behavior tests establish the expected isolated behavior.

- [ ] **Step 3: Functionize `install-aliases.sh`**

Move strict mode, alias-file path setup, heredoc generation, and status messages into `main`. Keep the heredoc content ASCII-only and finish with `main "$@"`.

- [ ] **Step 4: Functionize `install-systemd.sh`**

Move strict mode, path setup, directory creation, unit copying, daemon reload, and timer activation into `main` or helpers. Pass paths to helpers so tests can isolate them. Replace Unicode output with ASCII.

- [ ] **Step 5: Functionize `install_cline_rules.sh`**

Move strict mode, color constants, path setup, file list, and execution orchestration into `main`/helpers. Prefer plain ASCII log output rather than ANSI-colored Unicode markers; preserve install, backup, and verification behavior.

- [ ] **Step 6: Run focused installer verification**

```bash
for script in scripts/*.sh; do bash -n "$script"; done
uv run pytest tests/scripts/test_shell_scripts.py -q
```

Expected: all five scripts pass syntax, ASCII, structure, and isolated smoke checks.

- [ ] **Step 7: Commit**

```bash
git add scripts/install-aliases.sh scripts/install-systemd.sh scripts/install_cline_rules.sh tests/scripts/test_shell_scripts.py
git commit -m "refactor: functionize shell installers"
```

---

### Task 5: Full verification and diff review

**Files:**
- Verify: all files under `scripts/`
- Verify: `tests/scripts/test_shell_scripts.py`, `tests/scripts/test_check_modified_code_quality.py`

- [ ] **Step 1: Run all shell syntax checks**

```bash
find scripts -type f -name '*.sh' -print0 | xargs -0 -n1 bash -n
```

Expected: exit status `0`.

- [ ] **Step 2: Run the complete test suite**

```bash
make test
```

Expected: pytest exits `0` with no failures.

- [ ] **Step 3: Check the final diff**

```bash
git diff HEAD~4..HEAD --check
git status --short
git diff HEAD~4..HEAD -- scripts tests/scripts
```

Confirm that only requested scripts/tests changed, no Unicode remains in shell scripts, and all scripts end with `main "$@"`.

- [ ] **Step 4: Run each script's safe unit path once more**

```bash
bash scripts/check-code-quality.sh --help
printf '%s\n' '{"tool_input": {}}' | bash scripts/check-modified-code-quality.sh
```

Run the two installers only with the isolated temporary fixtures from Task 4; do not alter the real home directory or user systemd configuration.
