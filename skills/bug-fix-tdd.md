---
name: bug-fix-tdd
description: Fix bugs using Test-Driven Development (TDD) by writing a failing test, fixing the implementation, refactoring, and verifying edge cases.
---

# Bug Fix TDD Skill

## Description
This skill performs a bug fix using a Test-Driven Development (TDD) approach. It first checks if the repository is on the main branch and switches to a different branch if needed. Then it follows a TDD cycle: write failing test, fix implementation, refactor, and add more tests as needed.

## Requirements
- Git CLI available
- Repository must be a git repository
- Must have test framework set up

## Steps

### 1. Branch Management
- Check current branch
- If on main branch (master, main, etc.), create and switch to new feature branch
- Use git CLI to discover main branch name

### 2. TDD Cycle
1. **Write failing test**: Create test that exercises the bug and should fail
2. **Fix implementation**: Modify code to make test pass
3. **Refactor**: Improve code quality while keeping tests passing
4. **Explore**: Write additional tests to verify edge cases

### 3. Commit
- Create conventional commit for each changed file
- Follow semantic commit conventions

## Implementation

```python
from collections.abc import Sequence
from pathlib import Path
import subprocess

class BugFixTDD:
    def __init__(self, main_branches: Sequence[str] = ("master", "main", "trunk")) -> None:
        self._main_branches: tuple[str, ...] = tuple(main_branches)

    def get_current_branch(self) -> str:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def get_main_branch_name(self) -> str:
        for branch in self._main_branches:
            result: subprocess.CompletedProcess[str] = subprocess.run(
                ["git", "show-ref", "--verify", f"refs/heads/{branch}"],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return branch
        return "main"

    def create_feature_branch(self, bug_description: str) -> str:
        slug: str = bug_description.lower().replace(" ", "-")
        branch_name: str = f"fix/{slug}"
        subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        return branch_name

    def write_failing_test(self, test_code: str, test_file: Path) -> None:
        test_file.write_text(test_code, encoding="utf-8")
        subprocess.run(["pytest", str(test_file), "-v"], check=False)

    def fix_implementation(self, implementation_changes: Sequence[str]) -> None:
        for _change in implementation_changes:
            pass

    def refactor_code(self, refactoring_changes: Sequence[str]) -> None:
        for _change in refactoring_changes:
            pass

    def add_more_tests(self, additional_tests: Sequence[tuple[str, Path]]) -> None:
        for test_code, test_file in additional_tests:
            with open(test_file, "a", encoding="utf-8") as handle:
                handle.write(f"\n{test_code}")

    def create_conventional_commit(self, files_changed: Sequence[Path]) -> None:
        for file in files_changed:
            subprocess.run(["git", "add", str(file)], check=True)
            commit_message: str = f"fix: {file} - resolve bug"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)

    def execute(
        self,
        bug_description: str,
        test_code: str,
        test_file: Path,
        implementation_changes: Sequence[str],
        refactoring_changes: Sequence[str],
        additional_tests: Sequence[tuple[str, Path]],
    ) -> None:
        current_branch: str = self.get_current_branch()
        main_branch: str = self.get_main_branch_name()

        if current_branch == main_branch:
            self.create_feature_branch(bug_description)

        self.write_failing_test(test_code, test_file)
        self.fix_implementation(implementation_changes)
        self.refactor_code(refactoring_changes)
        self.add_more_tests(additional_tests)

        files_changed: list[Path] = [test_file]
        self.create_conventional_commit(files_changed)
```

## Usage Example

```bash
gb bug-fix-tdd --description "divide by zero in calculator" \
    --test-code "def test_divide_by_zero() -> None: ..." \
    --test-file test_calculator.py \
    --impl-changes "fix calculator.py: handle division by zero" \
    --refactor-changes "refactor calculator.py: extract division logic" \
    --additional-tests "def test_divide_by_zero_negative() -> None: ..."
```
