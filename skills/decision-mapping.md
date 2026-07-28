---
name: decision-mapping
description: Turn a loose idea into a sequenced map of investigation tickets, then drive them to resolution one at a time.
---

This skill is invoked when a loose idea requires more than one agent session to turn into a plan. It creates a stateful decision map in a markdown file, and drives the user through a sequence of tickets to resolve the open questions - which may require either prototyping, research or discussion.

## The Decision Map

The decision map is a single compact Markdown file, one per planning effort, git-tracked alongside the project. It is the canonical artifact — the **whole map is loaded as context into every session**, so it must stay compact.

Assets created during tickets should be linked to from the map, not duplicated within it.

Numbered entries ("tickets"), each its own section keyed by its number. Each ticket must be sized to one 100K token agent session.

## Ticket Types

- **Research**: Reading documentation, third-party API's, or local resources. Creates a markdown summary as an asset.
- **Prototype**: Writing UI or logic code to test a hypothesis. Uses the /prototype skill.
- **Discuss**: Conversation with the agent. Uses the /grilling and /domain-modelling skills. The default case.

## Invocation

### Bootstrap

User invokes with a loose idea.

1. Run a /grilling and /domain-modelling session to surface the open decisions.
2. Write a new decision map — mostly fog, frontier identified, trivially-decidable entries resolved inline.
3. Stop. Map-building is one session's work; do not also resolve tickets.

### Resume

User invokes with a path to an existing map and a ticket number.

1. Load the **whole map** as context.
2. Run a session to resolve the ticket, invoking skills as needed.
3. Record what the session resolved in the ticket's body.
4. Add newly-discovered tickets (with correct `blocked_by` edges).
5. Stop.

## Skipping The Decision Map

If the initial grilling results in no fog of war, offer the user the chance to skip the decision map. If they skip it, recommend either implementing directly or using `/to-prd` to schedule a multi-session implementation.
