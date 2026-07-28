---
name: verify-pr-feedback
description: Take PR review findings and pragmatically verify each one against the repo code — exercise the code, reason about intent, and classify each finding as real, wrong, or partial.
---

# Verify PR Feedback

Take PR review findings and verify each one against the codebase. Findings can be wrong, partial, or dead-on — your job is to determine which by exercising the code and reasoning about intent.

## Input

The user supplies PR review findings — inline comments, a review summary, or a list.

**If given a PR URL or `owner/repo/number`:** fetch findings automatically:

```bash
uv run fetch-pr-review <PR-URL | owner/repo/number>
```

`fetch-pr-review` auto-detects the forge from the remote URL — run `uv run forge-detect` first if you need to know which forge ahead of time. Detection logic (via script, not manual reasoning):

| Forge | Backend |
|-------|---------|
| GitHub | `gh api` |
| GitLab | `glab api` (future) |
| Bitbucket | `bb api` (future) |
| Forgejo/Gitea (Codeberg, self-hosted) | Forgejo REST API via `curl` + `FORGEJO_TOKEN`/`FJ_TOKEN` |

Outputs every review summary and inline comment as structured markdown with the reviewer, file path, and line number.

**If pasted inline:** read findings directly from the conversation.

## Process

### For each finding, run this loop:

### 1. Locate the code

Find every file and line the finding touches. Read the surrounding context — not just the hunk, but the full function, module, and callers. Grep for usages, tests, and related types.

### 2. Exercise the code

Run whatever proves or disproves the claim:

- **Compile/type-check**: `uv run pyright`, `npx tsc --noEmit`, etc.
- **Tests**: Run tests in the affected area, not the full suite unless needed.
- **Lint**: Run the project's linter on the affected files.
- **Runtime**: If the finding claims a runtime behavior (crash, wrong output, performance), write and run a minimal reproduction script. Do not guess — run it.
- **Existing tests**: Grep for tests covering the affected function. Read them. Run them.

If the finding is about style or design (no runtime claim), skip exercising and go to reasoning.

### 3. Reason about intent

Read beyond the diff. Ask:

- Why was the code written this way? Check commit history, PR descriptions, ADRs, `CONTEXT.md`.
- Does the finding account for the full context, or just the hunk?
- Is the finding technically correct but practically irrelevant (nitpicking a path that never runs)?
- Does the finding suggest a change that conflicts with existing architecture decisions?
- Would fixing it introduce risk elsewhere?

### 4. Classify

| Verdict | Meaning |
|---------|---------|
| **Real** | Finding is correct. The issue exists. Should be addressed. |
| **Wrong** | Finding is incorrect. The code is fine as-is. Provide evidence. |
| **Partial** | Finding has a kernel of truth but misses context, overstates severity, or suggests the wrong fix. |

### 5. Output

For each finding, produce:

```
## Finding: <restatement>

**Verdict:** Real | Wrong | Partial

**Evidence:**
- What you ran (type-check, test, reproduction script)
- What the output showed
- Relevant code context

**Reasoning:**
- Why the finding is or isn't valid
- Context the finding missed (if any)
- What would need to be true for it to be real

**Action:**
- Real → "Fix by: <specific suggestion>"
- Wrong → "No action needed. <evidence>"
- Partial → "Address the real part: <what>. Ignore the rest: <what>"
```

## Boundaries

This skill only verifies and reports. It does not implement fixes, make commits, or push changes. It does not engage in discussion with the reviewer — its output is for the user to decide what to act on.
