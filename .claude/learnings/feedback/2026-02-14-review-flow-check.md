---
date: "2026-02-14 12:06:27"
sha: "e91c905"
category: "missing-check"
status: applied
applied-date: "2026-02-22 18:16:17"
target: "skills/marketing_content/workflow/review.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills:
    [
      "atlas:second_brain",
      "atlas:marketing_content",
      "atlas:business_strategy",
      "atlas:marketing_visuals",
      "humanizer",
    ]
  commands: []
---

# Content review should include a flow/structure check

## Observation

Atlas review should include a flow review. Content should avoid unnecessary back and forth between ideas. Ideas should follow a simple, insightful, linear schema. Tech articles especially should be linear to make them easy to understand. Plot twists and non-linear structure are fine when there's a clear reason, but the default should be a logical progression that's easy to follow.

## Context

User was editing a blog post (atlas-compound-effect) and noticed structural issues: the inflection section (Stage 3) only addressed two of four problems from the dip (Stage 2), leaving the reader to wonder what happened to the other two. The post's flow had gaps where ideas introduced in one section weren't resolved in the corresponding section. This is a structural/flow problem that the review workflow should catch automatically.

## Analysis

The content review workflow (`marketing_content/workflow/review.md`) currently checks for brand voice, writing quality, and AI patterns, but does not include a structural flow review. It doesn't verify that ideas introduced in one section are resolved or addressed in corresponding sections, that the article follows a logical linear progression, or that the reader can follow the argument without confusion. This is a missing-check: the review skill lacks a flow/structure dimension that would catch disjointed or incomplete idea arcs before the user has to spot them manually.
