---
name: taskwarrior-sync
description: Synchronize Taskwarrior tasks with a Task Server, export/import tasks as JSON, and manage remote backups.
---

# Taskwarrior: Sync, Export, and Import

## Export Tasks

Exports all tasks matching a filter as JSON:

```bash
task export
task export project:Work
task export status:completed
task export +important
```

Output is an array of JSON objects, one per task. Each object contains all attributes.

Useful for:
- Backups
- Programmatic processing
- Migration between instances

## Import Tasks

Import tasks from JSON:

```bash
task import <file.json>
task import < file.json
```

```bash
task import backup.json
```

The JSON format must match the `task export` output format.

## Synchronize with Task Server

Requires a configured Task Server (taskd) or Inthe.aml:

```bash
task sync
task sync init  # First time setup
```

Configuration in `~/.taskrc`:

```
taskd.server=your-server:53589
taskd.credentials=your-credentials
taskd.certificate=~/.task/certs/client.cert.pem
taskd.key=~/.task/certs/client.key.pem
taskd.ca=~/.task/certs/ca.cert.pem
```

## Backup

```bash
# Backup task database
tar czf ~/task-backup-$(date +%Y%m%d).tar.gz ~/.task/
```

Since v3.0, the database is `~/.task/taskchampion.sqlite3`.
