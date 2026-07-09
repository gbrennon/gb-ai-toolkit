---
name: taskwarrior-delete
description: Delete tasks in Taskwarrior, undo deletions, and purge tasks permanently. Understand the difference between delete (soft) and purge (hard).
---

# Taskwarrior: Delete and Undo Tasks

## Delete a Task

```bash
task <id> delete
```

Marks a task as deleted (soft delete) — status changes to `deleted`, end date set, but data is retained.

```bash
$ task 1 delete
Deleted task 1 'Spam task'.
```

### Multiple Deletion

```bash
task 1 2 3 delete
task 1-10 delete
task project:Abandoned delete
```

## Undo Last Change

Reverts the **single most recent** command (add, modify, done, delete, start, stop):

```bash
task undo
```

Useful for accident recovery. Only one level of undo is supported.

```bash
$ task 1 delete
Deleted task 1 'Spam task'.
$ task undo
Undid command 'delete'.
Restored task 1.
```

## Purge (Permanent Removal)

Since Taskwarrior 2.6.0. Completely removes a deleted task from the database:

```bash
task <id> purge
```

Only works on tasks already in `deleted` status. Cannot be undone.

```bash
$ task 1 purge
Purged task 1 'Old spam task'.
```

## Log an Already-Completed Task

```bash
task log "Already did the thing"
task log "Fixed the bug" project:Support due:2025-01-01
```

Creates a task immediately in `completed` status with `entry` and `end` dates set.

## Duplicate a Task

```bash
task <id> duplicate
```

Clones an existing task with a fresh ID and new timestamps:

```bash
$ task 3 duplicate
Duplicated task 3 as task 4 'Original description'.
```
