#!/usr/bin/env bash

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get the script's directory and use it to find the repo root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

# Configuration (relative paths from repo root)
AGENT_RULES_DIR="${REPO_ROOT}/agent_rules"
CLINE_RULES_DIR="${HOME}/.cline/rules"
FILES=(
  "00-global-noise-exclusions.md"
  "01-python-language-specific.md"
  "02-general-project-policies.md"
)

# Functions
log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

check_agent_rules_exists() {
  if [[ ! -d "$AGENT_RULES_DIR" ]]; then
    log_error "Agent rules directory not found: $AGENT_RULES_DIR"
    exit 1
  fi
  log_info "Found agent_rules directory: $AGENT_RULES_DIR"
}

create_cline_dir() {
  if [[ ! -d "$CLINE_RULES_DIR" ]]; then
    log_info "Creating Cline rules directory: $CLINE_RULES_DIR"
    mkdir -p "$CLINE_RULES_DIR"
  else
    log_info "Cline rules directory exists: $CLINE_RULES_DIR"
  fi
}

move_files() {
  local failed=0

  for file in "${FILES[@]}"; do
    local src="${AGENT_RULES_DIR}/${file}"
    local dest="${CLINE_RULES_DIR}/${file}"

    if [[ ! -f "$src" ]]; then
      log_warn "File not found: $src"
      ((failed++))
      continue
    fi

    if [[ -f "$dest" ]]; then
      log_warn "Destination already exists, backing up: $dest"
      mv "$dest" "${dest}.bak.$(date +%s)"
    fi

    mv "$src" "$dest"
    log_info "Moved: $src → $dest"
  done

  return $failed
}

verify_installation() {
  log_info "Verifying installation..."
  local all_exist=true

  for file in "${FILES[@]}"; do
    local dest="${CLINE_RULES_DIR}/${file}"
    if [[ -f "$dest" ]]; then
      echo "  ✓ $file"
    else
      echo "  ✗ $file (MISSING)"
      all_exist=false
    fi
  done

  if [[ "$all_exist" == true ]]; then
    log_info "All files installed successfully!"
    return 0
  else
    log_error "Some files are missing"
    return 1
  fi
}

show_summary() {
  echo ""
  echo "──────────────────────────────────────"
  echo "Cline Rules Installation Summary"
  echo "──────────────────────────────────────"
  echo "Source: $AGENT_RULES_DIR"
  echo "Destination: $CLINE_RULES_DIR"
  echo "Files: ${#FILES[@]}"
  echo ""
  echo "Cline will load rules in order:"
  for i in "${!FILES[@]}"; do
    echo "  $((i+1)). ${FILES[$i]}"
  done
  echo ""
  echo "For more info, run:"
  echo "  cat $CLINE_RULES_DIR/00-global-noise-exclusions.md"
  echo "──────────────────────────────────────"
}

main() {
  echo ""
  log_info "Starting Cline rules installation..."
  echo ""

  check_agent_rules_exists
  create_cline_dir
  move_files
  verify_installation

  show_summary
}

main "$@"
