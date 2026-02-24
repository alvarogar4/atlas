---
date: "2026-02-22 12:02:06"
sha: "105e40b"
category: "missing-check"
status: applied
applied-date: "2026-02-22 18:31:07"
target: "skills/marketing_content/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: ["code:codebase-locator"]
  skills: ["atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# Missing trademark symbol when referencing third-party products

## Observation

Atlas wrote "ClickHouse" without the registered trademark symbol (®) in an X post draft. The user had to add "ClickHouse®" themselves. When the user then submitted their version with ® included, Atlas still didn't acknowledge or comment on the trademark, only fixing grammar/tone issues.

## Context

User asked for a quick standalone X post about ObsessionDB's decoupled architecture. Atlas drafted a tweet mentioning ClickHouse by name without the ® symbol. User corrected it to "ClickHouse®" in their version. Atlas reviewed the user's version and suggested tweaks but completely missed the trademark addition.

## Analysis

The content writing workflow (atlas:marketing_content) and its channel guidelines (twitter.md) have no guidance on trademark handling when referencing third-party products. The humanizer skill focuses on removing AI patterns but doesn't cover legal/branding requirements. There is no checklist step for verifying trademark symbols, attribution, or legal compliance when mentioning third-party brands in marketing content. This is a missing-check: the write and review workflows should include a trademark/attribution verification step, especially for product names that are registered trademarks (ClickHouse®, Kubernetes®, etc.).
