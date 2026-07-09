---
name: taskwarrior-setup
description: Initialize and configure the Taskwarrior task management CLI tool. Creates ~/.taskrc, verifies installation, and sets basic preferences for an autonomous AI agent workflow.
---

# Taskwarrior Setup

Before using Taskwarrior, ensure the `task` binary is installed and initialized.

## Verify Installation

```bash
which task && task --version
```

If not installed:
- **macOS**: `brew install task`
- **Ubuntu/Debian**: `sudo apt-get install taskwarrior`
- **Fedora**: `sudo dnf install task`
- **Arch**: `sudo pacman -S task`
- **Build from source**: `git clone https://github.com/GothenburgBitFactory/taskwarrior.git`

## Initialize

First run prompts for configuration — answer non-interactively:

```bash
task rc.confirmation=no <<< ""
```

This creates `~/.taskrc` and `~/.task/` directory tree.

## Default Configuration for Autonomous Use

Set these in `~/.taskrc` for non-interactive agent operation:

```
# Disable all confirmation prompts
confirmation=no
# Disable bulk modification threshold
bulk=0
# Disable recurrence confirmation
recurrence.confirmation=no
# Default to next report
default.command=next
# Week start
weekstart=monday
```

Or apply on-the-fly with `rc.` prefix:

```bash
task rc.confirmation=off rc.bulk=0 list
```

## Data Directory

All data stored in `~/.task/`:
- `~/.task/taskchampion.sqlite3` — task database (since v3.0, uses SQLite via TaskChampion)
- `~/.taskrc` — configuration file
- `~/.task/hooks/` — hook scripts

## Verify Working Setup

```bash
task add rc.confirmation=no test task
task list
task 1 done
task undo
```
