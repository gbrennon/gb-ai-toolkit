# Global Cline Rules — Exclude Noise Across All Languages

Exclude build artifacts, cache directories, dependency caches, and generated files that clutter context and waste tokens.

## Patterns to Always Ignore

### General Build & CI/CD
- `.git/`
- `.github/workflows/`
- `.gitlab-ci/`
- `.circleci/`
- `build/`
- `dist/`
- `out/`

### IDE & Editor
- `.vscode/`
- `.idea/`
- `*.swp`
- `*.swo`
- `*~`
- `.DS_Store`
- `Thumbs.db`
- `.project`
- `.classpath`

### Logs & Temporary
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

### Container & VM
- `Dockerfile.build`
- `.dockerignore`
- `.vagrant/`
