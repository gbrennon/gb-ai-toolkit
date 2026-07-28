---
name: semver-pre-v1-breaking-changes
description: Use when planning breaking changes, refactors, or API renames in personal open source repos before v1.0.0 — especially forging-blocks
---

# Pre-v1 Semantic Versioning: No Backward Compatibility

## Rule

**Personal open source projects at major version 0 do NOT maintain backward compatibility until v1.0.0.**

Semantic Versioning (SemVer) §4: "Major version zero (0.y.z) is for initial development. Anything MAY change at any time. The public API SHOULD NOT be considered stable."

## Scope

- `forging-blocks` (and any other personal open source repo at 0.y.z)
- Public API renames, removals, re-exports, and signature changes
- Module reorganizations, class hierarchy restructuring, and type parameter changes
- Any change that would be BREAKING in a post-v1 world

## What this means

| Action | Pre-v1 | Post-v1 |
|--------|--------|---------|
| Rename a public class | Allowed, no deprecation shim | Requires deprecation cycle |
| Move a module to a subpackage | Allowed, update consumers directly | Requires re-export shim |
| Change a function signature | Allowed | Requires overload or new name |
| Remove a public export | Allowed | Breaking change — semver-major |
| Restructure type parameters | Allowed | Breaking change — semver-major |

## When NOT to apply

- Repos at v1.0.0 or above — normal SemVer rules
- Third-party libraries the user does not own
- Repos with a published stability guarantee

## Commit convention

Breaking changes in pre-v1 repos should still use `!` in the commit subject (`refactor!(foundation): ...`) to signal intent even though the major version stays at 0.

## Version bumps

- Pre-v1: bump MINOR for breaking changes (0.x.0), PATCH for fixes/additions (0.0.x)
- Post-v1: bump MAJOR for breaking changes (x.0.0), MINOR for additions, PATCH for fixes

## Red flags

**Never:**
- Keep a deprecated shim or alias "just in case" for a pre-v1 project — dead weight
- Avoid a rename or restructure because it would be breaking — that's the point of 0.y.z
- Add backward-compatibility re-exports after moving modules — clean cutover only

**Always:**
- Clean up ALL consumers when renaming/moving — grep project-wide, no orphans
- Document breaking changes in the commit body
- Use `!` in conventional commit subjects for breaking changes
