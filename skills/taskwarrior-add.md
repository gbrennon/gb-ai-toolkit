---
name: taskwarrior-add
description: Create new tasks in Taskwarrior with descriptions, projects, priorities, due dates, tags, dependencies, and recurrence. The primary way to capture work items.
---

# Taskwarrior: Add Tasks

The `task add` command creates new tasks. It's the primary input mechanism.

## Basic Syntax

```bash
task add <description>
```

The description is all remaining arguments. Use quotes for multi-word or multi-line descriptions:

```bash
task add Fix the leaky plumbing
task add "Don't forget to shut off the main water valve first"
task add "Five syllables here\nSeven more syllables there\nAre you happy now?"
```

## Attributes

Set attributes inline — order doesn't matter, they can appear anywhere:

```bash
task add Find the adjustable wrench project:Home priority:H
task add project:Home priority:H Find the adjustable wrench
task add "Buy groceries" due:tomorrow
task add "Write report" due:2025-12-31
task add "Plan vacation" due:eom
```

### Available Attributes

| Attribute | Example | Description |
|-----------|---------|-------------|
| `project:` | `project:Home` | Project name (no spaces, use quotes) |
| `priority:` | `priority:H` | H=High, M=Medium, L=Low |
| `due:` | `due:tomorrow` | Due date (natural language) |
| `tags:` | `+important +work` | Tags (prefix with `+`) |
| `recur:` | `recur:weekly` | Recurrence frequency |
| `until:` | `until:2025-12-31` | Expiration date |
| `depends:` | `depends:3` | Blocked by another task ID |
| `scheduled:` | `scheduled:tomorrow` | Date task becomes visible |
| `wait:` | `wait:friday` | Date task becomes pending |
| `estimate:` | `estimate:2h` | Time estimate |

### Tag Syntax

- `+tag` — add tag
- `-tag` — remove tag (for modify/done)

### Priority

```bash
task add "Critical bug fix" priority:H
task add "Normal task" priority:M
task add "Nice to have" priority:L
```

### Due Dates

Use natural language:

```bash
task add "Submit report" due:today
task add "Meeting" due:tomorrow
task add "Deadline" due:friday
task add "Project end" due:eom
task add "Annual review" due:eoy
task add "Specific date" due:2025-12-31
```

### Recurring Tasks

```bash
task add "Weekly standup notes" recur:weekly due:monday
task add "Monthly report" recur:monthly due:1st
task add "Daily backup check" recur:daily
task add "Yearly review" recur:yearly
```

Recurring tasks auto-create the next instance when the current one is completed.

### Dependencies

```bash
task add "Setup database"
task add "Write API endpoints" depends:1
task add "Write tests" depends:1 depends:2
```

## En Passant (one-line modifications during add)

When adding, you can't annotate, but you can set any attribute:

```bash
task add "Task description" project:MyProject priority:H +important due:tomorrow
```

## Limitations

- Cannot add annotations while creating a task (use `task <id> annotate` after)
- Cannot set ID or UUID (auto-generated)
