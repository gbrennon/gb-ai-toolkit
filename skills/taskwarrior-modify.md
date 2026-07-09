---
name: taskwarrior-modify
description: Modify existing Taskwarrior tasks — change descriptions, add/remove tags, update projects, priorities, due dates, and more.
---

# Taskwarrior: Modify Tasks

The `modify` command changes existing tasks. It supports replacement, regex substitution, attribute changes, and bulk operations.

## Basic Usage

```bash
# Replace entire description
task 1 modify This is the new description

# Multiple tasks
task 1 3 5-10 modify -home +garden

# Using filter with modify
task project:outdoors modify +garden
task /planting/ modify -home +garden
```

## Changing Task Description

```bash
# Replace description entirely
task 1 modify New description goes here

# Regex substitution (s/from/to/)
task 1 modify /teh/the/
task 1 modify /old text/new text/

# Prepend text to description
task 1 prepend "URGENT: "

# Append text to description
task 1 append " (see notes)"
```

## Changing Attributes

```bash
# Change project
task 1 modify project:NewProject

# Change priority
task 1 modify priority:H
task 1 modify priority:

# Change due date
task 1 modify due:tomorrow
task 1 modify due:

# Add tags
task 1 modify +important +work

# Remove tags
task 1 modify -important

# Combine changes
task 1 modify +tag /from/to/ project:New priority:H depends:2 due:tomorrow recur:weekly New description
```

## Bulk Modification

Modify multiple tasks at once:

```bash
task 1-100 modify +later
task project:Home modify priority:H
task +meeting modify project:Meetings
```

### Bulk Threshold

By default, modifying more than 3 tasks requires confirmation.
Disable with:

```bash
task rc.bulk=0 modify ...
# Or in .taskrc: bulk=0
```

## Recurring Task Modification

When modifying a recurring task, Taskwarrior asks whether to propagate:

```bash
task 2 modify /pay/Pay/
# "This is a recurring task. Do you want to modify all pending recurrences?"
# Answer: yes/no
```

## Critical: Description + Tags vs. Description Text

**If the task description contains text that looks like tags** (e.g., `+code-review` or `+epic:1.4` as literal text), `modify` with `+tag`/`-tag` arguments will:

1. **Add/remove the actual Taskwarrior tag** from the task's tag list
2. **Replace the entire description** if bare text is present

Example — task has description: `Review PR #42 +code-review +epic:1.4:infrastructure`

```bash
# DANGEROUS: This replaces the description with "-code-review" AND removes the tag
task 1 modify -code-review

# SAFE: Use regex to modify only specific parts of the description
task 1 modify /+code-review//

# SAFE: Add/remove real tags separately from description changes
task 1 modify +urgent               # Only adds tag, doesn't touch description
task 1 modify /urgent//             # Remove text from description (regex)
task 1 modify description:new text  # Does NOT work; use bare text to replace
```

**Rule of thumb:** Any bare text (text not prefixed by `project:`, `due:`, `+`, `-`, or `/`) becomes the **new description**. Use `/regex/` substitutions to change parts of the description without replacing it entirely.

## Limits

- Without `status:pending` in your filter, modify affects completed/deleted tasks too
- With `rc.confirmation=off`, `rc.bulk=0`, `rc.recurrence.confirmation=off`, be careful — changes are immediate
