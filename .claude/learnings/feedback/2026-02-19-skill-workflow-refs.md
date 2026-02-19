---
date: "2026-02-19 16:31:13"
sha: "361dc0a"
category: "unclear-instruction"
status: applied
applied-date: "2026-02-19 16:42:38"
target: "skills/second_brain_foundation/SKILL.md"
change-type: "update"
observed-workflows:
  subagents: ["atlas:atlas:core:locate_knowledge", "code:codebase-locator"]
  skills: ["atlas:second_brain_foundation", "atlas:humanizer"]
  commands: []
---

# Skill references in second_brain_foundation don't guide the agent to the right workflow files

## Observation

When Atlas needed to create a content plan (2_plan.md), it could not find the workflow file for content planning. The agent used a codebase-locator subagent to search for the workflow, which means the skill's internal references were not clear enough for the agent to resolve the file path directly.

## Context

User asked to create a content plan for a Hacker News article about SigNoz + SharedMergeTree. The research phase (1_research.md) was already saved. Atlas needed to move to the plan phase but didn't know which workflow file defines the plan format. The second_brain_foundation skill SKILL.md references workflows like `workflows/capture.md` and `workflows/search.md` but the content creation workflows (research, plan, write, review) are likely in the marketing_content skill, not second_brain_foundation. The agent searched inside second_brain_foundation instead of loading the marketing_content skill.

## Analysis

Two issues compound here:

1. The second_brain_foundation SKILL.md capability table mentions content lifecycle (research, plan, write, review, results) but doesn't clarify that these workflows live in a different skill (atlas:marketing_content). The agent assumed the workflow files were inside second_brain_foundation's directory.

2. The agent should have loaded `atlas:marketing_content` skill when content creation started, since the task is writing a HN article (content creation, not knowledge management). The skill discovery step didn't identify marketing_content as relevant for this task.
