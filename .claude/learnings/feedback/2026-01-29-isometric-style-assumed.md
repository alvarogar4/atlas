---
date: "2026-01-29 15:48:16"
sha: "no-git"
category: wrong-pattern
status: pending
observed-workflows:
  subagents: []
  skills: ["atlas:marketing_visuals", "atlas:marketing_visuals"]
  commands: []
---

# AI image prompts defaulting to 3D isometric without asking

## Observation

The agent is taking 3D isometric style for granted since it's the example used in the skill. It should ask about style preference rather than assuming isometric.

## Context

User requested AI image prompts for blog post diagrams. Agent loaded the `atlas:marketing_visuals` skill which includes example prompts using 3D isometric style. Agent then generated all 5 image prompts using "Clean 3D isometric illustration" without first asking the user about their preferred style.

## Analysis

The skill documentation explicitly states under "Process > Step 2: Gather Requirements from User" that the agent should ask about style: "What visual style? - Clean/minimal, dramatic/bold, futuristic, classic/elegant, playful, organic, etc." The agent skipped this question and defaulted to the example's style (3D isometric). This is a "wrong-pattern" issue because the skill provides examples for illustration but the agent treated the example as the default instead of following the explicit requirement-gathering process.
