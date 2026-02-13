---
date: 2026-02-13T12:00:00+01:00
researcher: Atlas
git_commit: (no commits yet - fresh repo)
branch: main
repository: atlas
topic: "Atlas vs Jarvis Architecture Comparison + Issues Audit"
tags: [research, architecture, consolidation, jarvis, atlas, skills, commands, conversational, issues]
status: complete
last_updated: 2026-02-13
last_updated_by: Atlas
last_updated_note: "Added comprehensive issues audit for conversational rework"
---

# Research: Atlas vs Jarvis Architecture Comparison + Issues Audit

**Date**: 2026-02-13
**Repository**: atlas (compared against ../jarvis)

## Research Question

Compare Atlas with Jarvis: how commands were consolidated into skills, what changed structurally, and identify all issues preventing Atlas from being truly conversational.

## Summary

Atlas v2.0.0 consolidated Jarvis's 54 components into 9 (0 commands, 4 skills, 5 agents). But **the commands were moved into skills without changing the interaction model**. The skills still behave like CLI programs: argument parsing, dispatch tables, usage screens, rigid step numbering, and slash-command references everywhere. A second pass is needed to make Atlas conversational while preserving all functionality.

---

## Part 1: Structural Comparison (Jarvis → Atlas)

### Component Count

| Metric | Jarvis v1.9.1 | Atlas v2.0.0 |
|--------|---------------|--------------|
| Commands | 28 | 0 |
| Skills | 21 | 4 |
| Agents | 5 | 5 |
| Total | 54 | 9 |
| Indirection layers | 3 (command → skill → agent) | 1 (skill → agent) |

### What Was Absorbed Where

| Jarvis Commands | Absorbed Into Atlas Skill |
|----------------|--------------------------|
| 5 core_* commands + 10 project_* commands | `second_brain_foundation` |
| 11 marketing_content/calendar/theme commands | `marketing_content` |
| 2 business commands | `business_strategy` |

| Jarvis Skills | Absorbed Into Atlas Skill |
|--------------|--------------------------|
| `core_setup_context`, `core_error_handling`, `core_memory_ops`, `core_agent_orchestration`, `project_structure` (5) | `second_brain_foundation` |
| `marketing_content_creation`, `marketing_content_metrics`, `marketing_content_review`, `marketing_marketing_ops`, 5 `marketing_write_*` skills, `marketing_visual_identity` (11) | `marketing_content` |
| `marketing_image_ai_prompting`, `marketing_image_processing`, `marketing_image_schema_generation` (3) | `marketing_visuals` |
| `business_decision_framework` (1) | `business_strategy` |

### Atlas Skill Structure

```
skills/
├── second_brain_foundation/     # Knowledge + project management
│   ├── SKILL.md                 # Setup + error patterns + dispatch
│   ├── reference/               # folder-structure.md, project-templates.md
│   ├── workflows/               # setup, capture, search, help
│   └── project/                 # manage (CRUD), define (wizards)
├── marketing_content/           # Content lifecycle
│   ├── SKILL.md                 # Shared patterns + dispatch
│   ├── reference/               # metrics.md, review-checklist.md
│   ├── channels/                # blog, linkedin, twitter, email, hackernews, social
│   ├── workflow/                # research, plan, write, review, results
│   ├── calendar/                # plan, view
│   └── themes/                  # manage
├── marketing_visuals/           # Visual assets (internal only)
│   ├── SKILL.md                 # Decision tree + canvas sizes
│   ├── guides/                  # ai-prompting.md
│   └── tools/                   # processing.md, schema-generation.md + assets
└── business_strategy/           # Analysis + decisions + reviews
    ├── SKILL.md                 # Framework selection + dispatch
    ├── frameworks/              # 12 framework templates
    ├── templates/               # decision-log.md
    └── workflows/               # analyze, decision, review
```

### What Was Preserved Identically

- Content pipeline: research → plan → write → review → results
- Numbered file convention: 1_research.md through 5_results-{channel}.md
- Checkpoint enforcement (STOP AND WAIT)
- Agent orchestration: locate_knowledge → analyze_knowledge → domain agent
- All frameworks, templates, channel guides, review checklists
- PARA method knowledge base structure
- Project isolation with on-demand directory creation
- 5 agents (renamed only: jarvis → atlas, simplified setup references)

---

## Part 2: Issues Audit

### Issue 1: Skills Still Behave Like CLI Commands

**Severity: Fundamental**

The commands directory was deleted but the interaction model wasn't changed. Every SKILL.md contains:

- **`argument-hint` frontmatter** in 3 of 4 skills — e.g., `argument-hint: "<action> [channel] [topic]"` (marketing_content/SKILL.md:7)
- **Argument parsing instructions** — e.g., "Parse the first argument to determine the action" (second_brain_foundation/SKILL.md:54)
- **Action dispatch tables** routing string arguments to files — 3 SKILL.md files have these
- **"No Arguments → Show Usage" blocks** rendering CLI help screens — found in **13+ locations** across the codebase
- **`**Trigger**` lines** with exact slash syntax — found in **20+ workflow files**

Every workflow file starts with a `**Trigger**: '/atlas:...'` line and includes a "No Arguments → Show Usage" block that renders a man-page-style help screen with USAGE, DESCRIPTION, EXAMPLES, SEE ALSO sections.

**Locations**: second_brain_foundation/SKILL.md:52-111, marketing_content/SKILL.md:28-74, business_strategy/SKILL.md:22-70, and every workflow/*.md and project/*.md file.

### Issue 2: Slash-Command References Everywhere

**Severity: High**

Over **40 slash-command references** in output templates and next-step suggestions across the codebase. These force users into command syntax:

- research.md:213 → "run: `/atlas:marketing:content plan {topic}`"
- plan.md:149-152 → "`/atlas:marketing:content write blog {topic}`"
- write.md:148 → "`/atlas:marketing:content review ${channel} {topic}`"
- project/manage.md:37-59 → 6 slash-command references in next-steps output
- project/define.md:47,86,122 → next-step suggestions as slash commands
- workflows/help.md:5-66 → 60+ lines of pure slash-command listings
- CLAUDE.md:119-166 → 29 command table entries
- CLAUDE.md:280-295 → 14-step workflow as slash commands

### Issue 3: CLAUDE.md Is a Command Reference, Not a Personality Doc

**Severity: High**

The CLAUDE.md has good personality/style sections (lines 1-53) but then becomes a command manual:
- Lines 63-77: "Created By" columns listing slash commands
- Lines 115-166: Four tables of slash-command syntax (29 total entries)
- Lines 280-295: 14-step project workflow as numbered slash commands

The proactive behaviors (lines 203-212) are conversational but disconnected from the skill machinery. They say things like "check if related knowledge exists" but don't tell the agent HOW to do that without invoking a slash command.

**Missing from CLAUDE.md**:
- Intent detection patterns ("when user wants to create content, start with research")
- Flow awareness ("content goes through research → plan → write → review → results")
- In-progress work detection ("check for existing content folders before starting")
- Session resumption ("when returning to a topic, find where we left off")

### Issue 4: No Intent-to-Action Mapping

**Severity: High**

The SKILL.md `description` fields match at the skill level ("Use when working with marketing content") but not at the action level within a skill. When a user says "I want to write a blog post about AI":

1. The agent matches `marketing_content` skill ✓
2. But must then determine: start at `research` (not `write`) ✗
3. Must know the pipeline ordering ✗ (only defined in usage blocks)
4. Must know `write` requires `plan` which requires `research` ✗ (only defined as error messages in each workflow)

There's no natural-language-to-action bridge. The agent must parse the dispatch table like a CLI.

### Issue 5: No Workflow State Awareness

**Severity: Medium**

Content folders encode workflow state via numbered files (1_research.md, 2_plan.md, etc.) but:
- No proactive behavior tells the agent to check for in-progress workflows
- No mechanism to detect "user is continuing a topic" vs "user is starting fresh"
- Each workflow independently discovers the content folder via the same bash glob pattern (duplicated 6 times)
- Between workflow steps, next-step suggestions are slash commands, not natural flow

### Issue 6: Config Locked to Claude Code

**Severity: Medium**

Configuration is stored in `~/.claude/CLAUDE.md` — referenced in **18 files** across the codebase. This path is:
- Claude Code-specific (won't work with Codex, OpenClaw, Cursor, etc.)
- Not the same as `.env` (which exists as `.env.example` but is never read by any code)
- Hardcoded throughout (no abstraction or fallback chain)

Plugin cache paths (`~/.claude/plugins/cache/atlas-marketplace/atlas/*/`) appear in 4 locations in marketing_visuals/tools/*.md — also Claude Code-specific.

### Issue 7: Massive Content Duplication

**Severity: Medium**

| Duplicated Content | Copies | Locations |
|-------------------|--------|-----------|
| Full command reference tables | 3 | CLAUDE.md, help.md, README.md |
| Strategic frameworks selection table | 4 | CLAUDE.md, business_strategy/SKILL.md, analyze.md, business_strategist agent |
| Config-reading instructions | 8 | 3 SKILL.md files + 5 agent files |
| Content folder discovery bash glob | 6 | SKILL.md + 5 workflow files |
| Channel validation list | 6+ | SKILL.md, write.md, review.md, CLAUDE.md, etc. |
| Marketing frameworks (PAS/AIDA/BAB) | 2+ | CLAUDE.md, SKILL.md |

### Issue 8: Marketing Visuals Lacks Workflow Context

**Severity: Low**

The `marketing_visuals/SKILL.md` has a decision tree (photo editing? diagram? AI prompt?) but doesn't explain how tools chain together. Real-world workflow: generate AI image → crop to format → add schema overlay → optimize for web. This chaining is the power of the visual tools but isn't documented.

### Issue 9: Orphaned/Dead Files

**Severity: Low**

- `.env.example` — contains `ATLAS_BRAIN_PATH=~/brain` but no code reads `.env`
- `hooks/hooks.json` — empty (`{"hooks": {}}`)
- `workflows/help.md` — 60+ lines of pure CLI help that would be unnecessary in a conversational model

### Issue 10: Core Knowledge Actions Should Be Invisible

**Severity: Medium**

Operations like "save this idea", "what do I know about X", "remember this" are core brain operations that should feel natural, not require knowing `/atlas:second_brain:foundation idea [text]`. The `capture.md` workflow has a "No Arguments → Show Usage" block (lines 7-19) — for something that should be triggered by "hey, save this for later."

Similarly, `search` vs `recall` is a distinction the user shouldn't need to make. The agent should decide based on the question: "find files about X" = search, "what do I know about X" = recall (deep synthesis).

### Issue 11: Subagent Orchestration Pattern Is Implicit

**Severity: Low**

The locate → analyze → domain-agent pattern was in `core_agent_orchestration` in Jarvis. In Atlas it's absorbed into `second_brain_foundation/SKILL.md` but it's mixed with setup and error handling. Workflow files reference agents by name but the orchestration pattern itself isn't clearly documented as a reusable pattern.

### Issue 12: Missing Social Channel File

**Severity: Low**

`channels/social.md` is listed in the skill structure but the analysis notes it was "created" during consolidation. Need to verify it actually exists and has content (vs. being a stub or missing).

---

## Part 3: What a Conversational Atlas Would Need

### 1. CLAUDE.md as Personality + Intent Detection

Replace command tables with:
- **Capabilities described naturally**: "I can help you research, plan, write, and review content for any channel"
- **Intent patterns**: "When you mention writing content, I'll guide you through the full lifecycle"
- **Flow awareness baked in**: "Content always starts with research, even if you say 'write a blog post'"
- **State detection**: "I'll check if there's work in progress before starting fresh"

Keep: communication style, collaboration mode, critical thinking, proactive behaviors (expanded), frameworks tables (these are reference knowledge, not commands).

### 2. Skills as Knowledge, Not Command Parsers

SKILL.md files should:
- Drop `argument-hint` frontmatter
- Drop dispatch tables and "Parse the first argument" instructions
- Drop "No Arguments → Show Usage" blocks
- Instead: describe what the skill knows, what workflows exist, and how they connect
- The agent loads the skill when the domain is relevant, reads the workflows it needs

### 3. Workflow Files as Guides, Not Scripts

Workflow files should:
- Drop `**Trigger**: '/atlas:...'` headers
- Drop "No Arguments → Show Usage" blocks
- Keep the actual workflow logic, checkpoints, agent orchestration
- Replace slash-command next-step suggestions with natural language: "Now let's plan the content" instead of "Run `/atlas:marketing:content plan {topic}`"
- Keep the numbered-file convention (1_research.md, etc.) — this is great filesystem state

### 4. Portable Config

- Support `.env` file as primary config source
- Fall back to `~/.claude/CLAUDE.md` for Claude Code
- Abstract config reading into one pattern in SKILL.md that agents reference
- Single source of truth, not 18 hardcoded paths

### 5. Deduplication

- Command reference: CLAUDE.md only (remove from help.md and README or auto-generate)
- Frameworks table: business_strategy/SKILL.md only (agent reads it from there)
- Config reading: define once in second_brain_foundation, reference from others
- Content folder discovery: define once in marketing_content/SKILL.md, reference from workflows

### 6. Expanded Proactive Behaviors

Add:
- "When user expresses intent to create content → determine correct starting point and begin"
- "When user mentions a topic with existing content → find the content folder and report status"
- "When returning to a conversation about a topic → check for in-progress work"
- "When user says 'save this' or 'remember this' → capture from conversation context"
- "When user asks 'what do I know about X' → do deep recall automatically"

---

## Historical Context (from jarvis/thoughts/)

9 research/planning documents from Jan-Feb 2026 planned the consolidation:
1. Template simplification (Jan 20)
2. Branding capabilities audit (Jan 16)
3. Skill consolidation Phase 1 — 21 → 14 skills (Feb 12)
4. Commands-into-skills feasibility (Feb 12)
5. Combined architecture plan — still had 6 orphan skills (Feb 12)
6. External marketing skills gap analysis (Feb 12)
7. Clean 4-skill architecture — zero orphans (Feb 12)
8. Atlas 2.0 implementation plan — 8 phases (Feb 12)
9. Atlas 4-skill final pass — absorb remaining 7 intermediate skills (Feb 12)

The key insight was that `marketing_writing` shouldn't exist separately because writing IS the content pipeline's write step.

**What wasn't addressed in those plans**: The interaction model itself. The consolidation focused on reducing components (21 skills → 4, 28 commands → 0) but preserved the CLI-style interaction patterns verbatim. The "conversational" aspect was noted as a goal but not designed.
