---
name: multi-model-iterative-review
description: "Multi-model iterative code review: 2 parallel reviewers share findings across multiple rounds, then a meta-reviewer synthesizes a verdict and action plan. Non-consensus — optimizes for engineering quality, not agreement. Project-agnostic; customize focus areas per invocation."
---

Multi-model iterative code review pipeline. Reviews **what was done** — the current state of the codebase, not a PR diff. Two reviewer agents work in parallel, share findings via IRC between rounds, and a third meta-reviewer produces the final verdict and action plan.

Customize per invocation by specifying: focus areas for each reviewer, coding standards to enforce, number of rounds (default 3), and project-specific conventions.

## When to use

- After implementing a multi-file feature or refactor and want a second opinion
- When correctness, consistency, and design quality matter more than speed
- When you want to catch blind spots a single model or single round would miss
- When the user says "review what I did," "review for X," or names specific files to review

## Default models

Use three distinct model personalities to avoid correlated errors. Override per invocation if the user specifies different agents.

| Role | Agent ID | Default focus |
|------|----------|---------------|
| Reviewer A | `devstral` | Architecture, design quality, correctness, error handling, edge cases |
| Reviewer B | `qwen3.5` | Consistency, codestyle, conventions, dead code, naming |
| Meta-reviewer | `meta-reviewer` | Synthesize findings, resolve contradictions, produce verdict and action plan |

## Process

### 1. Determine review scope and parameters

Identify what to review. The user will typically say "review what I just did," name specific files/directories, or provide a ref (`main`, a commit SHA, a branch). If a ref is given, use `git diff <ref>...HEAD` to determine changed files.

Capture:
- The list of changed or target files
- If available: `git log` for context, any referenced issues or spec documents

Extract or default the following parameters from the user's prompt:

| Parameter | Default | How to override |
|-----------|---------|-----------------|
| Max rounds | 3 | "do N rounds," "up to 5 rounds" |
| Reviewer A focus | Architecture, design, correctness, edge cases | "review for X," "focus on Y" |
| Reviewer B focus | Consistency, conventions, codestyle, dead code | "check for X patterns," "audit Y" |
| Project conventions | Discovered from repo | "use PEP 695," "follow Rust idioms," "strict TypeScript" |
| Standards sources | `.editorconfig`, linter configs, contributing docs | "per CONTRIBUTING.md," "ignore X" |

Do NOT send full file contents as text blobs — tell each reviewer the file paths so they can use `read`, `grep`, and `lsp` to explore the codebase themselves.

### 2. Tier 1 — Round 1 (parallel)

Spawn both reviewers simultaneously via `task` with `agent: "reviewer"`.

**`devstral` template:**
```
Your focus: <Reviewer A focus from parameters>.

Review the following files: <file list>

Context: <what was done, commit log if available>
Project conventions: <standards, idioms, rules to enforce>

Rules:
- Evaluate correctness, design quality, and architecture
- Flag bugs, missing edge cases, wrong abstractions, missing abstractions
- Flag anything that would make the code hard to maintain or extend
- Under 400 words. Format: numbered findings with severity (critical/high/medium/low)
```

**`qwen3.5` template:**
```
Your focus: <Reviewer B focus from parameters>.

Review the following files: <file list>

Context: <what was done, commit log if available>
Project conventions: <standards, idioms, rules to enforce>

Rules:
- Evaluate consistency with existing codebase conventions
- Flag dead code, unused imports, inconsistent patterns, missing exports
- Flag anti-patterns, naming issues, documentation gaps
- Under 400 words. Format: numbered findings with severity (critical/high/medium/low)
```

### 3. IRC sharing (between rounds)

After BOTH reviewers finish a round, instruct them to IRC-share their findings with each other:

```irc
send to="devstral" message="Found findings: <brief summary>. Any disagreements or gaps in your analysis?"
send to="qwen3.5" message="Found findings: <brief summary>. Any disagreements or gaps in your analysis?"
```

Each reviewer then investigates the other's findings against their own and reports:
- Findings they agree with
- Findings they disagree with (with technical reasoning)
- Gaps the other reviewer missed

If the two reviewers arrive at substantially different conclusions (different files flagged, different severity assessments), or if either reports gaps in the other's analysis, proceed to the next round.

### 4. Additional rounds (up to configured max)

Each subsequent round:
1. Each reviewer receives the other's latest findings + the IRC discussion from the prior round
2. They re-investigate the code with fresh eyes, focusing on disagreements and gaps
3. They produce an updated report — a deeper investigation of contested points, not a repetition
4. IRC-share again

Stop when: (a) the max round count is reached, OR (b) both reviewers report "no substantive disagreements remain."

**Critical rule:** models MUST NOT aim for consensus. They MUST defend their position with technical reasoning when they believe they are correct. Disagreement is a signal, not a problem to smooth over.

### 5. Tier 2 — Meta-review

Spawn a third agent via `task` with `agent: "reviewer"`, Agent ID `meta-reviewer`:

```
You are a senior software engineer acting as a meta-reviewer. Below are the final reports from two parallel reviewers who examined the same codebase changes through multiple iterative rounds, sharing and challenging each other's findings.

## Reviewer A — devstral
<verbatim devstral final report>

## Reviewer B — qwen3.5
<verbatim qwen3.5 final report>

## IRC discussion log (all rounds)
<verbatim IRC exchanges>

Your job:
1. For each finding from both reviewers, state: ACCEPT, REJECT, or DEFER (with clear reasoning)
2. Resolve contradictions — when reviewers disagree, you decide based on technical merit, not compromise
3. Assign a final priority: CRITICAL (must fix), HIGH (should fix), MEDIUM (fix if time), LOW (nice to have)
4. Produce a numbered action plan the main agent can execute directly — each item includes a one-line fix instruction
5. A final verdict: APPROVE (merge as-is), REVISE (fix critical+high then merge), or REJECT (redesign needed)

Be decisive. Disagreement between reviewers is information, not a problem to split the difference on. Pick the technically stronger argument.
Under 400 words.
```

### 6. Act on the plan

Read the meta-review verdict and action plan. Fix all **CRITICAL** and **HIGH** priority items. For each:
1. Make the change
2. Verify (run affected tests, typecheck)
3. Track what was fixed

Do not yield until at least all CRITICAL items are resolved. Report deferred items to the user.

### 7. Present output

Display all reports distinctly — never merge or rerank:

```
## Tier 1 — Reviewer A (<focus>)
<final verbatim report>

## Tier 1 — Reviewer B (<focus>)
<final verbatim report>

## Tier 2 — Meta-Review Verdict
**Verdict:** APPROVE / REVISE / REJECT
<numbered action plan>

## Actions Taken
- Fixed: <item> — <description>
- Deferred: <item> — <reason>
```

## Boundaries

- Reviews the current state of working code, not a PR diff
- Configurable rounds (default 3, user can specify more or fewer)
- Project-agnostic — customize focus areas and conventions per invocation
- Models optimize for quality, not consensus — disagreements are surfaced, not smoothed over
- Meta-reviewer is the final arbiter; its verdict and action plan are authoritative
- CRITICAL items must be resolved before yielding
- Does not push, commit, or open PRs
