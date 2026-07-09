---
name: taskwarrior-annotate
description: Add and remove annotations on Taskwarrior tasks. Annotations are timestamped notes attached to tasks for additional context.
---

# Taskwarrior: Annotations

Annotations are timestamped notes attached to tasks. They preserve additional context, discussions, or progress notes.

## Add an Annotation

```bash
task <id> annotate <annotation text>
```

Examples:

```bash
task 1 annotate Spoke to the client, they want it in blue
task 2 annotate "Found the root cause in auth.ts line 42"
task 3 annotate "Blocked until DevOps provisions the staging server"
```

Each annotation is timestamped automatically.

## Remove an Annotation

```bash
task <id> denotate <annotation text>
```

Must match the exact annotation text:

```bash
task 1 denotate "Spoke to the client, they want it in blue"
```

## View Annotations

Annotations appear in the task's `info` display:

```bash
task <id> info
```

They also show up in the `long` report and custom reports that include the `description` column (which shows annotation count).

## Limits

- Cannot add annotations during `task add` — add them after creation
- Annotation text is matched literally for `denotate`

## Use Cases

- Recording investigation findings: `task 5 annotate "Discovered the bug is in validate()"`
- Client feedback: `task 3 annotate "Client approved the new design"`
- Blockers: `task 7 annotate "Waiting for legal review"`
- Decisions made: `task 2 annotate "Decided to use PostgreSQL over MySQL"`
