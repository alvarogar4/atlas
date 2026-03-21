---
date: "2026-03-21 15:20:26"
sha: "dcdd1e8"
category: "missing-check"
status: applied
applied-date: "2026-03-21 15:22:58"
target: "CLAUDE.md"
change-type: "update"
observed-workflows:
  subagents: []
  skills: ["atlas:second_brain", "atlas:humanizer"]
  commands: []
---

# Humanizer not loaded for ad-hoc writing tasks outside content pipeline

## Observation

When asked to write lightweight content (emails, articles, general writing for others) — whether using the atlas brain or not — the humanizer skill is frequently not loaded. The content pipeline (marketing content workflow) does load it, but ad-hoc writing requests bypass it entirely.

## Context

Any scenario where the user asks Atlas to write text meant for other people: drafting an email, writing a short article, composing a message, etc. These are outside the formal content creation pipeline but still produce text that should sound human and natural.

## Analysis

The humanizer loading is currently tied to the content pipeline workflow (marketing content creation steps). The CLAUDE.md states "All written content goes through the humanizer skill" but the trigger logic in practice only fires during the formal content lifecycle (research → plan → write → review). Lightweight writing tasks don't enter that pipeline, so the humanizer check is never triggered. This is a missing-check: there's no instruction that explicitly tells the agent to load the humanizer for any text written for external consumption, regardless of whether it goes through the content pipeline.
