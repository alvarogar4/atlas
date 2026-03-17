---
date: "2026-02-26 19:46:39"
sha: "c051d39"
category: "missing-check"
status: applied
applied-date: "2026-03-17 14:21:20"
target: "skills/marketing_content/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:marketing_content", "atlas:second_brain"]
  commands: []
---

# Agent skipped calendar workflow when reviewing upcoming content

## Observation

User asked to review next week's content. Agent loaded the marketing_content skill (which clearly maps "View content calendar" → `calendar/view.md` & `second_brain/entities/calendar.md`) but never read those workflow files. Instead, it globbed for `calendar*.md` files, found nothing, and fell back to listing content folders by date — reconstructing the schedule manually from folder names.

## Context

User asked "I need to discuss next weeks content. Can you review it for me? What do we need to prepare." The agent loaded both `atlas:marketing_content` and `atlas:second_brain` skills, then went straight to globbing for files instead of following the skill's documented calendar workflow.

## Analysis

The marketing_content skill defines a clear capability table: "View content calendar → `calendar/view.md` & `second_brain/entities/calendar.md`". The agent matched the user's intent (reviewing upcoming content) but skipped the skill's prescribed workflow. It should have:

1. Read `calendar/view.md` from the skill directory to understand how to locate and display the calendar
2. Read `second_brain/entities/calendar.md` to understand the calendar entity structure
3. Found and read the actual calendar file using those instructions

Instead it improvised with Glob patterns that didn't match anything. This is a missing-check: the skill was loaded but its workflow routing was not followed for the calendar-specific path.
