#!/usr/bin/env bash
# check-code-quality.sh — Run Lizard complexity and Semgrep structural checks
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_RULES_DIR="$(cd "$SCRIPT_DIR/.." && pwd)/rules/semgrep"
GLOBAL_RULES_DIR="${HOME}/.config/ai-toolkit/semgrep"

MAX_COMPLEXITY=5
MAX_LENGTH=50
MAX_ARGS=5
SEMGREP_CONFIG=""
ONLY_LIZARD=false
ONLY_SEMGREP=false
INIT_MODE=false
TARGET=""

usage() {
  cat << 'EOF'
Usage: check-code-quality [OPTIONS] [DIRECTORY]

Enforces code quality standards using Lizard (quantitative complexity)
and Semgrep (structural rules & conventions).

Arguments:
  DIRECTORY                     Target directory to scan (default: current directory .)

Options:
  --init                        Initialize .semgrep/ in target directory with bundled rules
  -C, --max-complexity <int>    Maximum cyclomatic complexity (default: 5)
  -L, --max-length <int>        Maximum function length in lines (default: 50)
  -a, --max-args <int>          Maximum function arguments (default: 5)
  --semgrep-config <path>       Custom Semgrep rules config file or directory
  --only-lizard                 Run only Lizard complexity analysis
  --only-semgrep                Run only Semgrep structural analysis
  -h, --help                    Display this help message and exit

Examples:
  check-code-quality
  check-code-quality src/
  check-code-quality --init
  check-code-quality -C 4 -L 40
  check-code-quality --only-lizard
  check-code-quality --only-semgrep
EOF
}

# Parse CLI arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --init)
      INIT_MODE=true
      shift
      ;;
    -C|--max-complexity)
      if [[ -z "${2:-}" ]]; then
        echo "Error: $1 requires an integer argument" >&2
        exit 1
      fi
      MAX_COMPLEXITY="$2"
      shift 2
      ;;
    -L|--max-length)
      if [[ -z "${2:-}" ]]; then
        echo "Error: $1 requires an integer argument" >&2
        exit 1
      fi
      MAX_LENGTH="$2"
      shift 2
      ;;
    -a|--max-args)
      if [[ -z "${2:-}" ]]; then
        echo "Error: $1 requires an integer argument" >&2
        exit 1
      fi
      MAX_ARGS="$2"
      shift 2
      ;;
    --semgrep-config)
      if [[ -z "${2:-}" ]]; then
        echo "Error: $1 requires a path argument" >&2
        exit 1
      fi
      SEMGREP_CONFIG="$2"
      shift 2
      ;;
    --only-lizard)
      ONLY_LIZARD=true
      shift
      ;;
    --only-semgrep)
      ONLY_SEMGREP=true
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ -z "$TARGET" ]]; then
        TARGET="$1"
      else
        echo "Unexpected extra argument: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

TARGET="${TARGET:-.}"

# Find available bundled Semgrep rules directory
find_source_rules() {
  if [[ -d "$GLOBAL_RULES_DIR" ]] && compgen -G "$GLOBAL_RULES_DIR/*.yml" > /dev/null; then
    echo "$GLOBAL_RULES_DIR"
  elif [[ -d "$REPO_RULES_DIR" ]] && compgen -G "$REPO_RULES_DIR/*.yml" > /dev/null; then
    echo "$REPO_RULES_DIR"
  else
    echo ""
  fi
}

# Handle --init
if [[ "$INIT_MODE" == true ]]; then
  SRC_RULES="$(find_source_rules)"
  if [[ -z "$SRC_RULES" ]]; then
    echo "Error: Could not locate source Semgrep rules (checked $GLOBAL_RULES_DIR and $REPO_RULES_DIR)" >&2
    exit 1
  fi

  DEST_DIR="$TARGET/.semgrep"
  mkdir -p "$DEST_DIR"
  cp -v "$SRC_RULES"/*.yml "$DEST_DIR/"
  echo "Initialized Semgrep rules in $DEST_DIR"
  exit 0
fi

# Resolve Semgrep configuration path
resolve_semgrep_config() {
  if [[ -n "$SEMGREP_CONFIG" ]]; then
    echo "$SEMGREP_CONFIG"
    return
  fi

  if [[ -d "$TARGET/.semgrep" ]] && compgen -G "$TARGET/.semgrep/*.yml" > /dev/null; then
    echo "$TARGET/.semgrep"
    return
  fi

  if [[ -d "$GLOBAL_RULES_DIR" ]] && compgen -G "$GLOBAL_RULES_DIR/*.yml" > /dev/null; then
    echo "$GLOBAL_RULES_DIR"
    return
  fi

  if [[ -d "$REPO_RULES_DIR" ]] && compgen -G "$REPO_RULES_DIR/*.yml" > /dev/null; then
    echo "$REPO_RULES_DIR"
    return
  fi

  echo ""
}

# Check prerequisites
check_lizard() {
  if ! command -v lizard > /dev/null 2>&1; then
    echo "Error: 'lizard' executable not found in PATH." >&2
    echo "Install it via: pipx install lizard   or   pip install lizard" >&2
    exit 1
  fi
}

check_semgrep() {
  if ! command -v semgrep > /dev/null 2>&1; then
    echo "Error: 'semgrep' executable not found in PATH." >&2
    echo "Install it via: pipx install semgrep   or   pip install semgrep" >&2
    exit 1
  fi
}

EXIT_CODE=0

# Run Lizard analysis
if [[ "$ONLY_SEMGREP" == false ]]; then
  check_lizard
  echo "=== Running Lizard Complexity Analysis ==="
  echo "Limits: Cyclomatic Complexity <= $MAX_COMPLEXITY, Function Length <= $MAX_LENGTH, Arguments <= $MAX_ARGS"
  echo "Target: $TARGET"
  echo ""

  set +e
  lizard -C "$MAX_COMPLEXITY" -L "$MAX_LENGTH" -a "$MAX_ARGS" -i 0 "$TARGET"
  LIZARD_STATUS=$?
  set -e

  if [[ $LIZARD_STATUS -ne 0 ]]; then
    echo "❌ Lizard detected complexity violations!" >&2
    EXIT_CODE=1
  else
    echo "✅ Lizard complexity analysis passed."
  fi
  echo ""
fi

# Run Semgrep analysis
if [[ "$ONLY_LIZARD" == false ]]; then
  check_semgrep
  RESOLVED_CONFIG="$(resolve_semgrep_config)"
  if [[ -z "$RESOLVED_CONFIG" ]]; then
    echo "Error: No Semgrep configuration found. Checked:" >&2
    echo "  - $TARGET/.semgrep" >&2
    echo "  - $GLOBAL_RULES_DIR" >&2
    echo "  - $REPO_RULES_DIR" >&2
    echo "Run with --init or specify --semgrep-config <path>" >&2
    exit 1
  fi

  echo "=== Running Semgrep Structural Analysis ==="
  echo "Config: $RESOLVED_CONFIG"
  echo "Target: $TARGET"
  echo ""

  set +e
  semgrep scan --config "$RESOLVED_CONFIG" --error "$TARGET"
  SEMGREP_STATUS=$?
  set -e

  if [[ $SEMGREP_STATUS -ne 0 ]]; then
    echo "❌ Semgrep detected structural or architectural violations!" >&2
    EXIT_CODE=1
  else
    echo "✅ Semgrep structural analysis passed."
  fi
  echo ""
fi

if [[ $EXIT_CODE -ne 0 ]]; then
  echo "❌ Code quality checks failed. Please refactor violations above before completing work." >&2
  exit 1
fi

echo "✅ All code quality checks passed."
exit 0
