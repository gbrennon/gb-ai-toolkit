# General Purpose Noise Exclusions

Exclude build artifacts, cache directories, dependency caches, and generated files that clutter context and waste tokens. Covers general, Python, and OS-level patterns.

## Patterns to Always Ignore

### General Build and CI/CD
- `.git/`
- `.github/workflows/`
- `.gitlab-ci/`
- `.circleci/`
- `build/`
- `dist/`
- `out/`

### IDE and Editor
- `.vscode/`
- `.idea/`
- `*.swp`
- `*.swo`
- `*~`
- `.DS_Store`
- `Thumbs.db`
- `.project`
- `.classpath`

### Logs and Temporary
- `*.log`
- `logs/`
- `tmp/`
- `temp/`
- `.tmp/`
- `*.pid`

### OS-Level
- `.DS_Store`
- `.Thumbs.db`
- `.AppleDouble/`
- `.LSOverride`

### Container and VM
- `Dockerfile.build`
- `.dockerignore`
- `.vagrant/`

### Python Cache and Bytecode
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.pyd`
- `.Python`

### Python Distribution and Build
- `*.egg-info/`
- `*.egg/`
- `.eggs/`
- `sdist/`
- `wheel/`

### Python Test and Coverage
- `.pytest_cache/`
- `.coverage`
- `htmlcov/`
- `.tox/`
- `cover/`

### Python Linting and Type Checking
- `.mypy_cache/`
- `.ruff_cache/`
- `.pylint_cache/`
- `.pytype/`

### Python Virtual Environments
- `venv/`
- `.venv/`
- `env/`
- `.env/`
- `ENV/`
- `.ENV/`
- `virtualenv/`

### Python Package Managers
- `*.lock` (Pipenv, Poetry)
- `Pipfile.lock`
- `poetry.lock`
- `pip-log.txt`
- `pip-delete-this-directory.txt`

### Python IDE and Development
- `.ipynb_checkpoints/`
- `.jupyter/`
- `*.ipynb`
- `.spyproject/`
- `.ropeproject/`
- `*.pot`
- `instance/`
- `.webassets-cache`
