---
date: "2026-04-02 19:32:42"
sha: "07ca6aa"
category: "missing-check"
status: pending
observed-workflows:
  subagents: ["atlas:content_reviewer"]
  skills: ["atlas:second_brain", "atlas:marketing_content", "atlas:humanizer", "atlas:marketing_visuals"]
  commands: []
---

# Review workflow applies corrections to drafts but doesn't append corrections log to the draft file

## Observation

The corrections were applied to the draft files (humanizer fixes, reviewer fixes) but the corrections log was not appended to the bottom of each `3_draft-{channel}.md` file as the review workflow specifies. The workflow at `workflow/review.md` step 6 says to "append a combined corrections section at the bottom of `3_draft-${channel}.md`" with a specific markdown format listing humanizer fixes and reviewer fixes with line numbers and before/after text.

## Context

Working on the projections-vs-materialized-views blog post (ClickHouse Deep Dive series #7). Three drafts were written (blog, linkedin, twitter) and then reviewed in parallel using three `atlas:content_reviewer` subagents. After receiving the review results, the main agent applied all fixes directly to the draft files via Edit tool calls, but skipped the step of appending the corrections log to each draft file. The corrections were instead only captured in the separate `4_review-{channel}.md` files.

## Analysis

The agent correctly applied the fixes (edits to the draft files) and correctly created the review files (`4_review-{channel}.md`), but missed the intermediate step of appending the corrections log directly into the draft files themselves. This is a missing-check issue: the review workflow has a specific instruction (step 6) to append corrections to the draft, and the agent skipped it, jumping from applying fixes to creating the review file. The corrections log in the draft serves a different purpose than the review file: it lets someone reading the draft see what was changed without opening a separate file.
