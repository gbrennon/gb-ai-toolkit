---
name: taskwarrior-done
description: Mark tasks as completed in Taskwarrior. Supports en passant modifications and undoing completions.
---

# Taskwarrior: Complete Tasks

The `done` command marks tasks as completed, setting status to `completed`, adding an `end` date, and updating `modified` date.

## Basic Usage

```bash
task <id> done
```

Example:

```bash
$ task add Paint the door
Created task 1.
$ task 1 done
Completed task 1 'Paint the door'.
Completed 1 task.
```

## Multiple Tasks

```bash
task 1 2 3 done
task 1-10 done
```

## En Passant (modifications while completing)

You can make additional changes during completion:

```bash
# Remove a tag while completing
task 1 done -important

# Fix typo in description while completing
task 1 done /teh/the/

# Change project while completing
task 1 done project:Archive

# Add a tag while completing
task 1 done +completed-q2

# Combine multiple changes
task 1 done -important /teh/the/ project:Archive +q2
```

### Text Added as Annotation

Text that isn't a recognized attribute is added as an annotation:

```bash
task 1 done Paint dried overnight
# Adds "Paint dried overnight" as an annotation to the completed task
```

## UUID Reference After Completion

Once completed, the task loses its numeric ID. Reference it by UUID:

```bash
task 937bb9e4-25df-42a7-a52e-bd47edb23ccd info
```

## Undo a Completion

```bash
task undo
```

Reverts the last modification (including a `done` command).

## Related

- `task log "Already done task"` — record an already-completed task
- `task <id> delete` — mark as deleted (not completed)
- `task undo` — revert last change
