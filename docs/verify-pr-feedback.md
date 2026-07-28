# Verify PR Feedback

Pragmatically verify PR review findings against the repo code — exercise the code, reason about intent, and classify each finding as real, wrong, or partial.

## Prerequisites

- `uv sync` to install the `fetch-pr-review` command
- **For GitHub repos:** `gh` CLI installed and authenticated (`gh auth login`)
- **For Forgejo/Gitea repos:** `curl` (usually pre-installed). Set `FORGEJO_TOKEN` or `FJ_TOKEN` env var for private repos. Public repos work without auth.

## Usage

### 1. Invoke the skill

```
/verify-pr-feedback
```

### 2. Provide findings

**Option A — PR URL (recommended):**

The skill runs `uv run fetch-pr-review <url>` automatically. Auto-detects forge from the URL:
- `github.com/...` → uses `gh api`
- `codeberg.org/...`, `git.example.com/...` → uses Forgejo REST API

```
https://github.com/owner/repo/pull/42
https://codeberg.org/owner/repo/pulls/7
```

**Option B — paste findings inline:**

```
Reviewer: "The retry logic will cause 3-second delays"
Reviewer: "fetch_user() is missing error handling for 404s"
```

### 3. Get verdicts

For each finding the skill:

1. **Locates** the code with full context (callers, tests, types)
2. **Exercises** it via type-check, tests, lint, or a runtime repro
3. **Reasons** about intent from commit history, ADRs, and architecture
4. **Classifies** as **Real**, **Wrong**, or **Partial** with evidence

## Script reference

```
uv run fetch-pr-review <PR-URL | owner/repo/number>
```

Auto-detects forge from the remote URL. Fetches via `gh api` (GitHub) or Forgejo REST API via `curl` — no model tokens consumed for fetching. Auth is handled by `gh` (GitHub) or `FORGEJO_TOKEN`/`FJ_TOKEN` env var (Forgejo).

Outputs structured markdown grouped by reviewer and file.

## Workflow

```
PR review arrives
      ↓
/verify-pr-feedback <url>
      ↓
Script fetches all findings (free — CLI/API, not model tokens)
      ↓
Skill verifies each finding against the codebase
      ↓
Report: Real / Wrong / Partial with evidence
      ↓
You decide what to act on
```
