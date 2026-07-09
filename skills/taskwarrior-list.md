---
name: taskwarrior-list
description: List, filter, and view tasks in Taskwarrior using built-in reports and custom filters. Monitor pending, completed, blocked, and overdue tasks.
---

# Taskwarrior: List and View Tasks

Taskwarrior provides multiple built-in reports for viewing tasks.

## Standard Reports

```bash
# Most urgent tasks (default)
task next

# Simple list of pending tasks
task list

# Minimal view
task ls

# All tasks (pending + completed + deleted)
task all

# Long format with all details
task long

# Minimal format
task minimal

# Overdue tasks
task overdue

# Blocked tasks (waiting on dependencies)
task blocked

# Blocking tasks (blocking others)
task blocking

# Started tasks (active)
task active

# Recurring tasks only
task recurring

# Waiting tasks
task waiting

# Recently modified/new
task newest
task oldest

# Completed tasks
task completed
```

## Task ID and UUID

Pending tasks show a numeric ID.
Completed/deleted tasks don't have IDs — use UUID instead:

```bash
task <id> info              # View by numeric ID (pending only)
task <uuid> info            # View by UUID (any status)
```

## Filtering

Combine filters to narrow results:

```bash
# By project
task project:Home
task project:Work

# By priority
task priority:H
task priority:H or priority:M

# By tag
task +important
task +work -meeting

# By status
task status:pending
task status:completed
task status:deleted

# By due date
task due:today
task due:tomorrow
task due.before:today
task due.after:2025-01-01

# By description (regex)
task /search term/

# Multiple filters (AND by default)
task project:Work +urgent priority:H

# OR filter
task '(project:Work or project:Home)'
task '(priority:H or priority:M) and +important'
```

## View Single Task Details

```bash
task <id> info
```

Shows all attributes, annotations, tags, timestamps, dependency graph, urgency score.

## Count Tasks

```bash
task count
task count project:Home
task count +important
```

## Custom Reports

Reports are configurable in `~/.taskrc`:

```
report.my-report.columns = id,project,priority,due,description
report.my-report.filter = status:pending
report.my-report.sort = urgency-
```

Then run:

```bash
task my-report
```
