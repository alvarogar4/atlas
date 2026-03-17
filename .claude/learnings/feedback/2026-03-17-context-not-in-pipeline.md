---
date: "2026-03-17 10:20:41"
sha: "9b29614"
category: "missing-check"
status: applied
applied-date: "2026-03-17 14:56:26"
target: "skills/marketing_content/"
change-type: "create+update"
observed-workflows:
  subagents: ["atlas:atlas:content_reviewer", "atlas:atlas:market_researcher", "atlas:atlas:locate_knowledge", "atlas:atlas:analyze_knowledge"]
  skills: ["atlas:marketing_content", "atlas:humanizer"]
  commands: []
---

# 0_context.md is not part of the content lifecycle pipeline

## Observation

The `0_context.md` file exists in content folders but is not a formal step in the content lifecycle pipeline. The user wants it to be a compulsory, conversational step that serves as the central point of the content workflow. Currently the pipeline is: research (1_research.md) -> plan (2_plan.md) -> write (3_draft) -> review (4_review) -> results (5_results). The `0_context.md` is created informally but not enforced, not documented as a step, and not checked by downstream workflows.

## Context

Writing a blog draft for the rudel.ai launch. The `0_context.md` file contained critical framing decisions (source available vs open source, no company names, no investor mentions, exact numbers, design philosophy, shipping philosophy) that the user had carefully curated. The agent initially looked at the wrong brain (atlas-brain instead of obsessionDB-brain) and had to be corrected. The context file was the single source of truth for all the nuanced decisions, but the pipeline doesn't formally require it or reference it.

## Analysis

The content lifecycle in SKILL.md defines steps 1-5 but `0_context.md` is not mentioned anywhere in the pipeline. The research workflow doesn't create it, the plan workflow doesn't require it, and the write workflow doesn't check for it. It exists as an ad-hoc file that the user creates manually to capture the angle, constraints, tone, narrative structure, and framing decisions for a piece of content. Because it's not formalized, downstream workflows (research, plan, write) don't explicitly read it or validate against it. The user wants this to be step 0: a compulsory, conversational intake step where the user and agent align on what the content is about before any research or planning begins.
