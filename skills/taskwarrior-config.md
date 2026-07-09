---
name: taskwarrior-config
description: Configure Taskwarrior settings via .taskrc or on-the-fly rc. options. Manage UDAs, contexts, aliases, and report customization.
---

# Taskwarrior: Configuration

## Config File

Primary config at `~/.taskrc`. Also checked: `$TASKRC` environment variable.

## View Configuration

```bash
task show                      # All config
task show report.list          # List report config
task show color                # Color config
task show <pattern>            # Search config
```

## Set Configuration

```bash
# Persist in .taskrc
task config <key>=<value>

# On-the-fly (doesn't persist)
task rc.<key>=<value> <command>

# Examples
task config default.command=next
task rc.confirmation=off list
task config weekstart=monday
```

## Key Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `confirmation` | `on` | Prompt for confirmation |
| `bulk` | `3` | Threshold for bulk confirmation (0=no limit) |
| `default.command` | `next` | Default report |
| `weekstart` | `sunday` | First day of week |
| `recurrence.confirmation` | `on` | Confirm recurrence propagation |
| `print.empty.columns` | `off` | Hide empty columns in reports |

## Contexts

Contexts are saved filters that scope commands:

```bash
# Define a context
task context define work project:Work +office

# Activate a context
task context work

# Show current context
task context

# List all contexts
task context list

# Deactivate context
task context none
```

## UDAs (User-Defined Attributes)

Extend Taskwarrior with custom fields:

```bash
# Define a UDA
task config uda.estimate.type=string
task config uda.estimate.label=Estimate

# Define a UDA with allowed values
task config uda.stage.type=string
task config uda.stage.label=Stage
task config uda.stage.values=todo,doing,done,review

# Use in a task
task add "Implement feature" estimate:2d stage:todo
```

## Reports

Customize built-in reports or create new ones:

```bash
# Custom report
task config report.my-report.columns=id,project,priority,due,description
task config report.my-report.filter=status:pending
task config report.my-report.sort=urgency-
```

## Aliases

Create command shortcuts:

```bash
task config alias.todo="list"
task config alias.today="list due:today"
task config alias.blocked="list blocked"
```

Then use: `task todo`, `task today`, `task blocked`
