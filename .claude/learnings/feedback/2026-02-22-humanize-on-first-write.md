---
date: "2026-02-22 13:11:40"
sha: "2847038"
category: "missing-check"
status: applied
applied-date: "2026-02-22 18:17:11"
target: "skills/marketing_content/workflow/write.md"
change-type: "update"
observed-workflows:
  subagents: ["code:codebase-locator"]
  skills: ["atlas:marketing_visuals", "atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# Humanizer anti-patterns must be applied during initial content write, not as a second pass

## Observation

User asked to reduce AI detection on LinkedIn/Twitter drafts that were scoring 100% AI-detected. The agent successfully rewrote the content to pass AI detection, but the user's feedback is clear: "this must be the result on the first round." The initial drafts (from the original write workflow) should have already been non-detectable. The humanizer pass should not be a separate remediation step after the fact.

## Context

Working on marketing content for "The problem with 'best practices' in data engineering" post. The drafts (3_draft-linkedin.md and 3_draft-twitter.md) had already been written and reviewed (4_review files existed). When the user tested them against AI detectors, they scored 100% AI-detected. The agent then had to diagnose structural AI patterns (uniform decision structure, rule-of-three, too-clean argument arc, rhetorical questions with neat answers, identical paragraph templates) and rewrite both drafts. This rewrite should not have been necessary if the write workflow had properly internalized the humanizer constraints from the start.

## Analysis

The `atlas:marketing_content` write workflow and/or the `atlas:humanizer` skill are not being applied effectively during the initial content generation. The MEMORY.md already documents this exact insight: "Writing with brand voice + humanizer as primary constraints from the start produces noticeably less detectable text than writing first and polishing after." The structural patterns (uniform paragraph lengths, template-based sections, rule-of-three, too-clean logical flow) are the hardest to fix post-hoc because they're baked into how the content was generated. The write workflow needs to enforce these structural constraints during generation, not just check vocabulary patterns after.
