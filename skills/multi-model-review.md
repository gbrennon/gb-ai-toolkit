---
name: multi-model-review
description: "3-tier review pipeline: 2 parallel reviewers (standards + spec) then a meta-reviewer that synthesizes findings into an action plan. Acts on the plan before yielding. Prevents single-reviewer blind spots."
---

Run a 3-tier code review pipeline: two parallel reviewers (standards + spec), then a meta-reviewer that synthesizes their findings into an actionable plan, then act on the plan before yielding.

## Process

### 1. Determine the diff range

If the user provided a ref (commit SHA, branch name, tag, `main`), use it. Otherwise default to `main`.

Validate the ref resolves:

```bash
git rev-parse <ref>
```

Capture:

```bash
git diff <ref>...HEAD
git log <ref>..HEAD --oneline --no-decorate
```

If the diff is empty, report no changes to review and stop.

### 2. Identify spec and standards sources

**Spec source** — Look for the originating specification in this order:
1. Issue references in commit messages (`#123`, `Closes #45`, etc.)
2. A path the user passed as an argument
3. A spec file under `docs/`, `specs/`, or `.scratch/` matching the branch name or feature
4. If nothing found, the spec reviewer will skip and report "no spec available"

**Standards sources** — Any repository files documenting code conventions: `CODING_STANDARDS.md`, `CONTRIBUTING.md`, `.editorconfig`, `tsconfig.json` strict settings, etc.

### 3. Tier 1 — Parallel reviews

Spawn two review subagents simultaneously using `task` with `agent: "reviewer"`:

**Agent ID `devstral` — Standards review**
- Assignment includes: the full `git diff <ref>...HEAD` output, the commit log, paths to standards-source files
- Prompt: "You are a standards-focused code reviewer. Review this diff against documented coding standards. Report every violation per file/hunk. Distinguish hard violations (broken rules, antipatterns, type safety issues, missing error handling) from judgement calls (style preferences, subjective conventions). Skip anything tooling (formatter, linter) enforces. Under 400 words."

**Agent ID `qwen3.5` — Spec/Functionality review**
- Assignment includes: the full diff output, the commit log, and the spec content if found (or "no spec available")
- Prompt: "You are a spec-focused code reviewer. Review this diff for correctness: (a) logic errors or missing edge cases, (b) functions or behaviors that look incomplete or broken, (c) test coverage concerns — untested paths or insufficient assertions. If a spec was provided, check each requirement against the diff and report mismatches. Under 400 words."

### 4. Read both Tier-1 results

Wait for both subagents to finish. Read their full outputs. Keep them verbatim for the final report.

### 5. Tier 2 — Meta-review

Spawn a third subagent using `task` with `agent: "reviewer"`, Agent ID `meta-reviewer`:

- Assignment includes:
  - The diff context (what changed at a high level, file list, commit subjects)
  - The verbatim output from `devstral` (standards review)
  - The verbatim output from `qwen3.5` (spec review)
  - Prompt: "You are a senior engineer running a deepseek v4 pro model. Review both code reviews below and produce a combined action plan. For each finding: (a) state whether to act on it or dismiss and why, (b) assign priority (critical/high/medium/low), (c) give a one-line fix instruction for the main agent to execute. Resolve any contradictions between the two reviews. Output as a numbered action plan the main agent can execute directly. Under 300 words."

### 6. Act on the plan

Read the meta-review result. Fix all **critical** and **high** priority items from the action plan. For each fix:

1. Make the change
2. Verify correctness (rerun tests, typecheck, or visual check as appropriate)
3. Track what was fixed

Do not yield until at least all critical items are resolved. Medium/low items may be deferred but must be reported to the user.

### 7. Present combined output

Display all three reports distinctly — never merge or rerank:

```
## Tier 1 — Standards Review (devstral)
<verbatim output>

## Tier 1 — Spec Review (qwen3.5)
<verbatim output>

## Tier 2 — Meta-Review (deepseek v4 pro)
<action plan>

## Actions Taken
- Fixed: <item> — <brief description of fix>
- Fixed: <item> — <brief description of fix>
- Deferred: <item> — <reason>
```

## Boundaries

This skill reviews code and acts on the findings. It does not push or open PRs. It does not replace the user's own review. The three reports are always kept separate — never merge or rerank findings across reviewers.
