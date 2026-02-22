---
date: "2026-02-22 12:54:02"
sha: "cceb44b"
category: "wrong-pattern"
status: pending
observed-workflows:
  subagents: []
  skills: ["atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# Migrate skill prompts from markdown to JSON format

## Observation

JSON-structured prompts have been observed to work really well. The atlas plugin skills currently use markdown-based prompts. They should be migrated to JSON format for better structure and consistency.

## Context

User has seen that JSON-formatted prompts produce better results and wants to migrate the atlas plugin's prompt definitions (skills, workflows, channels) to use JSON instead of plain markdown.

## Analysis

The current atlas skills (marketing_content, humanizer, marketing_visuals, etc.) define their prompts, workflows, and instructions in markdown files. JSON provides more explicit structure for prompt definitions: clear field separation, enforced schema, and less ambiguity in how the agent parses instructions. Markdown relies on heading hierarchy and prose which can be interpreted loosely. JSON forces discrete, well-defined fields that the model can parse deterministically. This is a wrong-pattern issue: the current format works but a better-performing format is available.
