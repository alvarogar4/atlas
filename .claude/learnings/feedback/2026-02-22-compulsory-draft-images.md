---
date: "2026-02-22 22:40:56"
sha: "03455a3"
category: "missing-check"
status: pending
observed-workflows:
  subagents: []
  skills: ["atlas:marketing_content", "atlas:marketing_visuals"]
  commands: []
---

# Image generation should be compulsory during content draft phase

## Observation

The content writing workflow should include image generation as a compulsory step during the draft phase, not optional or post-hoc. The agent should evaluate how many images are needed and for what purpose based on the channel:

- **Blogs**: Can have several images (social card + in-content images)
- **Twitter/LinkedIn**: At most one image per post
- **Threads**: Several if necessary, though less common

The agent should assess the image needs as part of drafting, not wait for the user to request them.

## Context

General feedback about the marketing content writing workflow. Currently, image generation via `atlas:marketing_visuals` is available but not enforced as part of the draft phase. The writing workflow completes drafts without considering visual assets, leaving image creation as a separate, optional step.

## Analysis

The writing workflow skills (`skills/marketing_content/channels/*.md` and `skills/marketing_content/workflow/write.md`) don't mandate image generation during drafting. This is a missing-check: the draft phase should include an image assessment step where the agent determines the number and purpose of images based on channel conventions, then generates them as part of the draft output. The `atlas:marketing_visuals` skill exists but isn't wired into the writing workflow as a required step.
