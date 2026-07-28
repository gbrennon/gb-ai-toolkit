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
import subprocess
import os
from typing import List, Optional

class BugFixTDD:
    def __init__(self):
        self.main_branch_names = ['master', 'main', 'trunk']

    def get_current_branch(self) -> str:
        """Get current git branch name"""
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()

    def get_main_branch_name(self) -> str:
        """Discover the main branch name from git configuration"""
        for branch in self.main_branch_names:
            result = subprocess.run(['git', 'show-ref', '--verify', f'refs/heads/{branch}'],
                                  capture_output=True, check=False)
            if result.returncode == 0:
                return branch
        return 'main'  # default fallback

    def create_feature_branch(self, bug_description: str) -> str:
        """Create new feature branch for bug fix"""
        branch_name = f"fix/{bug_description.lower().replace(' ', '-')}"
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
        return branch_name

    def write_failing_test(self, test_code: str, test_file: str) -> None:
        """Write test that should fail to demonstrate bug"""
        with open(test_file, 'w') as f:
            f.write(test_code)

        # Run test to confirm it fails
        subprocess.run(['pytest', test_file, '-v'], check=False)

    def fix_implementation(self, implementation_changes: List[str]) -> None:
        """Apply fixes to implementation"""
        for change in implementation_changes:
            # Apply each change to the codebase
            pass  # Implementation depends on specific changes

    def refactor_code(self, refactoring_changes: List[str]) -> None:
        """Refactor code while keeping tests passing"""
        for change in refactoring_changes:
            # Apply refactoring changes
            pass

    def add_more_tests(self, additional_tests: List[tuple]) -> None:
        """Add more tests to verify edge cases"""
        for test_code, test_file in additional_tests:
            with open(test_file, 'a') as f:
                f.write('\n' + test_code)

    def create_conventional_commit(self, files_changed: List[str]) -> None:
        """Create conventional commit for each changed file"""
        for file in files_changed:
            subprocess.run(['git', 'add', file], check=True)

            # Determine commit type based on file changes
            commit_type = 'fix'  # default for bug fixes

            commit_message = f"{commit_type}: {file} - bug fix"
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)

    def execute(self, bug_description: str, test_code: str, test_file: str,
                implementation_changes: List[str], refactoring_changes: List[str],
                additional_tests: List[tuple]) -> None:
        """Execute the full TDD bug fix process"""
        # Step 1: Branch management
        current_branch = self.get_current_branch()
        main_branch = self.get_main_branch_name()

        if current_branch == main_branch:
            print(f"Currently on main branch {main_branch}, creating feature branch...")
            feature_branch = self.create_feature_branch(bug_description)
            print(f"Switched to new branch: {feature_branch}")

        # Step 2: TDD Cycle
        print("Step 1: Writing failing test...")
        self.write_failing_test(test_code, test_file)

        print("Step 2: Fixing implementation...")
        self.fix_implementation(implementation_changes)

        print("Step 3: Refactoring code...")
        self.refactor_code(refactoring_changes)

        print("Step 4: Adding more tests...")
        self.add_more_tests(additional_tests)

        # Step 3: Commit
        print("Creating conventional commits...")
        files_changed = [test_file] + [change.split(' ')[1] for change in implementation_changes]
        self.create_conventional_commit(files_changed)

        print("Bug fix TDD process completed successfully!")

# Example usage
tdd_bug_fix = BugFixTDD()
tdd_bug_fix.execute(
    bug_description="divide by zero in calculator",
    test_code="""
def test_divide_by_zero():
    from calculator import divide
    result = divide(10, 0)
    assert result == 0  # This should fail, demonstrating the bug
""",
    test_file="test_calculator.py",
    implementation_changes=[
        "fix calculator.py: handle division by zero",
        "add check for zero denominator in divide function"
    ],
    refactoring_changes=[
        "refactor calculator.py: extract division logic to separate method"
    ],
    additional_tests=[
        ("def test_divide_by_zero_negative(): ...", "test_calculator.py")
    ]
)
```

## Usage Example

```bash
gb bug-fix-tdd --description "divide by zero in calculator" \
    --test-code "def test_divide_by_zero(): ..." \
    --test-file test_calculator.py \
    --impl-changes "fix calculator.py: handle division by zero" \
    --refactor-changes "refactor calculator.py: extract division logic" \
    --additional-tests "def test_divide_by_zero_negative(): ..."
```

## Notes
- This skill assumes git is available in the system PATH
- The test framework should be configured (pytest in the example)
- Implementation details for fix_implementation and refactor_code need to be adapted to specific use cases
- The skill follows semantic commit conventions for better changelog generation
