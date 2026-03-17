---
date: "2026-03-17 10:19:10"
sha: "9b29614"
category: "missing-check"
status: applied
applied-date: "2026-03-17 14:01:40"
target: "skills/marketing_content/workflow/plan.md, skills/marketing_content/workflow/write.md, skills/marketing_content/workflow/review.md"
change-type: "update"
observed-workflows:
  subagents: ["atlas:atlas:content_reviewer"]
  skills: ["atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# Blog title generated too long and not SEO-optimized on first draft

## Observation

The blog title generated in the first draft was too long and didn't work for SEO. The user had to reject it and ask for alternatives. The title "We Analyzed 1,573 AI Coding Sessions. Here's What Nobody Is Measuring." was 71 characters (over the 60-char SEO limit documented in the blog channel guidelines) and didn't front-load the primary keyword ("AI coding agent analytics").

## Context

Writing a blog draft for the rudel.ai launch post. The plan included three title options, all of which exceeded the 60-character SEO limit. The write workflow picked option 1 without validating it against the blog channel's own SEO requirements (title under 60 chars, primary keyword front-loaded).

## Analysis

The blog channel guidelines explicitly state: "Keep under 60 characters (Google truncates after 60)" and "Front-load the keyword when possible." The write workflow generated a title that violated both rules. The plan workflow also proposed three titles that all exceeded the limit, meaning the SEO check was missed at planning time too. The root cause is a missing validation step: neither the plan nor the write workflow enforces the documented title length and keyword placement constraints before presenting the title to the user.
