---
name: taskwarrior
description: Complete autonomous Taskwarrior skill for AI agents. Covers the full task lifecycle — create, list, filter, modify, start/stop, complete, delete, annotate, sync, and configure — without prompting the user for confirmation.
disabled: false
---

# Taskwarrior: Autonomous Task Management

Taskwarrior is a CLI task management tool. You are an autonomous agent — run commands directly without asking for permission.

## Quick Reference

| Action | Command |
|--------|---------|
| **Add task** | `task add "description" project:X priority:H due:tomorrow +tag` |
| **List tasks** | `task next` / `task list` / `task project:X` |
| **View task** | `task <id> info` |
| **Start work** | `task <id> start` |
| **Stop work** | `task <id> stop` |
| **Complete** | `task <id> done` |
| **Modify** | `task <id> modify /old/new/ +tag -tag project:Y priority:M` |
| **Delete** | `task <id> delete` |
| **Undo** | `task undo` |
| **Annotate** | `task <id> annotate "note text"` |
| **Remove annot.** | `task <id> denotate "exact text"` |
| **Filter** | `task +tag project:Work due:today priority:H` |
| **Export** | `task export` |
| **Count** | `task count` |

## Important: Non-Interactive Mode

**Best practice:** Set these in `~/.taskrc` so every command runs without prompts:

```
confirmation=no
bulk=0
recurrence.confirmation=no
```

**Do NOT use `rc.confirmation=off` as a prefix** to individual commands — it can interfere with task ID parsing and cause "No tasks specified" errors on modify/start/stop/done. Only the `add` command works reliably with `rc.` prefixes.

If you must override on-the-fly set `TASKRC` to a custom config.

## Autonomous Workflow

### 1. Check Current State
```bash
task next       # What's most urgent?
task active     # What's already in progress?
task blocked    # What's blocked?
task overdue    # What's past due?
```

### 2. Add Tasks When Prompted
```bash
task add "Implement OAuth login" project:Auth priority:H due:friday +backend
task add "Write API docs" project:Auth depends:1 priority:M
```

### 3. Track Work Sessions
```bash
task <id> start
# ... do the work ...
task <id> stop
```

### 4. Record Progress
```bash
task <id> annotate "Found the bug in validate()"
task <id> annotate "PR submitted, waiting for review"
```

### 5. Complete or Reassign
```bash
task <id> done                                    # Mark done
task <id> done -important /typo/correct/          # Done with changes
task <id> modify project:Backlog priority:L       # De-prioritize
task <id> delete                                  # Remove
```

### 6. Recover from Mistakes
```bash
task undo                                         # Undo last action
```

## Natural Language Interpretation

| User says | What to do |
|-----------|------------|
| "Add a task to fix the login bug, high priority" | `task add "Fix the login bug" priority:H` |
| "What's on my list?" | `task next` or `task list` |
| "Show me what's urgent" | `task next` |
| "Mark task 3 as done" | `task 3 done` |
| "Change task 2's project to Home" | `task 2 modify project:Home` |
| "I'm working on task 5 now" | `task 5 start` |
| "What's blocked?" | `task blocked` |
| "Show overdue tasks" | `task overdue` |
| "Add a note to task 4" | `task 4 annotate "the note"` |
| "Undo that" | `task undo` |
| "Delete task 7" | `task 7 delete` |
| "How many tasks do I have?" | `task count` |

## Tips

- **Recurring tasks**: Use `recur:weekly due:monday` — completing one auto-creates the next
- **Dependencies**: `depends:<id>` — blocks task until dependency is done
- **En passant**: Modify during done/start: `task 1 done -tag project:Archive`
- **Batch operations**: `task 1-10 modify +batch-tag` or `task project:Old delete`
- **Undo safety**: Only one undo level — be careful with modifications
- **Search**: `task /regex/` — filter by regex on description
- **Always run commands without asking**: You are autonomous, just execute
- **⚠️ Modify + bare text pitfall**: Never pass bare text (like `-code-review`) to `modify` — it will replace the entire description. Use `/syntax/` regex substitutions instead.
- **Tags in description are just text**: If your task descriptions contain `+tag-like-text`, those are NOT actual Taskwarrior tags. `modify -tag` operates on real tags, not description text.

