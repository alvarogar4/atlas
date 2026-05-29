---
date: "2026-04-09 13:01:28"
sha: "95881c9"
category: "missing-check"
status: pending
subagents: ["atlas:locate_knowledge", "atlas:analyze_knowledge", "atlas:market_researcher", "atlas:content_reviewer", "code:library-docs-researcher"]
skills: ["atlas:second_brain", "atlas:marketing_content", "atlas:humanizer"]
commands: []
target: "atlas:skills/marketing_content/workflow/review.md"
target-repo: "plugin:atlas"
change-type: "update"
---

# Review workflow: agent skipped saving 4_review files after fixing issues

## Context

Running the full content pipeline (context, research, plan, write, review) for ObsessionDB's ClickHouse Deep Dive Post #8 (Query Optimization). After writing drafts for blog, LinkedIn, and Twitter, the user asked for a review. The content_reviewer agent returned findings, all blockers and warnings were fixed in the draft files, but the 4_review-{channel}.md files were never created. The user had to explicitly ask for them.

## Observation

"this failed, didnt saved the reviews" - The agent completed the review, fixed all issues, and reported results to the user, but did not save the review files (step 7 of the review workflow). The user had to remind the agent to create them.

## Analysis

The review workflow (review.md) has a clear step 7: "Save reviewer findings as review file: ${CONTENT_FOLDER}/4_review-${channel}.md". The agent skipped this step, jumping from fixing issues (step 6) directly to presenting results (step 8). The root cause is that the review was done in a non-standard way: instead of following the review workflow step-by-step per channel, the agent spawned one content_reviewer that reviewed all three channels simultaneously, then fixed issues across all files, then forgot the file-saving step. The workflow is designed per-channel, and collapsing it into one pass made it easy to lose track of the save step.

## Proposed Improvement

Add an explicit reminder in the review workflow between step 6 (apply fixes) and step 8 (present results) that makes the file save harder to skip. The current step 7 is a single line that's easy to overlook when the agent is focused on fixing issues.

Proposed change to `review.md`, step 7:

```markdown
7. **Save reviewer findings as review file (MANDATORY):** `${CONTENT_FOLDER}/4_review-${channel}.md`

Use the Review Output Format below. This file is a required pipeline artifact. Do NOT proceed to the checkpoint without saving it. If reviewing multiple channels, save one review file per channel.
```

The key additions are: marking it MANDATORY, stating it's a required pipeline artifact, adding the "do NOT proceed" gate, and noting the multi-channel case explicitly.
