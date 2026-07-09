# Python-Specific Cline Rules

Exclude Python-specific build artifacts, cache directories, and virtual environments.

## Python Cache & Bytecode
- `__pycache__/`
- `*.pyc`
- `*.pyo`
- `*.pyd`
- `.Python`

## Python Distribution & Build
- `*.egg-info/`
- `*.egg/`
- `.eggs/`
- `dist/`
- `build/`
- `sdist/`
- `wheel/`

## Python Test & Coverage
- `.pytest_cache/`
- `.coverage`
- `htmlcov/`
- `.tox/`
- `cover/`

## Python Linting & Type Checking
- `.mypy_cache/`
- `.ruff_cache/`
- `.pylint_cache/`
- `.pytype/`

## Python Virtual Environments
- `venv/`
- `.venv/`
- `env/`
- `.env/`
- `ENV/`
- `.ENV/`
- `virtualenv/`

## Python Package Managers
- `*.lock` (Pipenv, Poetry)
- `Pipfile.lock`
- `poetry.lock`
- `pip-log.txt`
- `pip-delete-this-directory.txt`

## Python IDE & Development
- `.ipynb_checkpoints/`
- `.jupyter/`
- `*.ipynb`
- `.spyproject/`
- `.ropeproject/`
- `*.pot`
- `instance/`
- `.webassets-cache`
