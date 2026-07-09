---
name: taskwarrior-start-stop
description: Track active work sessions in Taskwarrior. Start and stop tasks to record when work begins and ends, enabling timesheet reports and active task filtering.
---

# Taskwarrior: Start and Stop Tasks

Use `start` and `stop` to track when you begin and end work on tasks. This enables time tracking, active task views, and timesheet reports.

## Start a Task

```bash
task <id> start
```

Marks the task as active — sets the `start` timestamp and tags it as ACTIVE.

```bash
$ task 1 start
Started task 1 'Implement login page'.
```

Starting a task that's already started updates its start time.

### En Passant on Start

```bash
task 1 start -important   # Remove tag while starting
task 1 start +in-progress # Add tag while starting
```

## Stop a Task

```bash
task <id> stop
```

Removes the active status — clears the `start` timestamp.

```bash
$ task 1 stop
Stopped task 1 'Implement login page'.
```

## View Active Tasks

```bash
task active
task start.age     # Shows how long each task has been active
```

## Timesheet Report

```bash
task timesheet
# Shows a weekly breakdown of started/stopped tasks
```

## Automation Notes

When used autonomously by an AI agent:

1. **Start** before beginning work to track it: `task <id> start`
2. **Stop** after completing the work phase: `task <id> stop`
3. Use `task active` to check what's currently in progress
4. Use `task timesheet` to report on time spent

## Example Workflow

```bash
task add "Implement user authentication" project:Auth priority:H
# -> Created task 12

task 12 start
# -> Started task 12

# ... agent works on the task ...

task 12 stop
# -> Stopped task 12

task 12 done
# -> Completed task 12
```
