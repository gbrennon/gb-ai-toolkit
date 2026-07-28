---
name: review
description: Review the changes since a fixed point (commit, branch, tag, or merge-base) along two axes — Standards (does the code follow this repo's documented coding standards?) and Spec (does the code match what the originating issue/PRD asked for?). Runs both reviews in parallel sub-agents and reports them side by side.
---

Two-axis review of the diff between `HEAD` and a fixed point the user supplies:

- **Standards** — does the code conform to this repo's documented coding standards?
- **Spec** — does the code faithfully implement the originating issue / PRD / spec?

Both axes run as **parallel sub-agents** so they don't pollute each other's context, then this skill aggregates their findings.

## Process

### 0. Detect the forge

Run `uv run forge-detect` to learn which forge this repo uses (github, gitlab, bitbucket, codeberg, gitea). All forge operations below auto-detect from the remote URL.

### 1. Identify the spec source

1. Issue references in the commit messages — fetch via `uv run forge-issue view <ref>`.
2. A path the user passed as an argument.
3. A PRD/spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature.
4. If nothing is found, ask the user where the spec is.

### 2. Identify the standards sources

Collect the list of files that document how code should be written: `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `CONTEXT.md`, `docs/adr/`, `.editorconfig`, lint/type configs.

### 3. Spawn both sub-agents in parallel

Send a single message with two sub-agent calls. Each reads the diff and reports findings independently.

### 4. Aggregate

Present the two reports under `## Standards` and `## Spec` headings. Do **not** merge or rerank findings — the two axes are deliberately separate.
