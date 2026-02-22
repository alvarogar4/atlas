---
name: atlas:second_brain
description: Core operations for the personal knowledge base. Use WHENEVER the user mentions notes, memories, knowledge, brain, ideas, captures, projects, or wants to store/retrieve/organize information. This skill provides the patterns for all knowledge base operations.
tools: Read, Write, Grep, Glob, Bash, AskUserQuestion, Task
user_invocable: true
---

# Second Brain Foundation

Core operations for the personal knowledge base using the PARA method.

## Config

Atlas reads configuration from multiple sources in priority order:

### Config Chain

1. **Conversation context**: Check current `system-reminder` for `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values already loaded from CLAUDE.md
2. **`.env` file**: Read `.env` in the plugin folder
3. **Error**: "Brain not configured. Let's set it up — where should I store your knowledge base?"

### Reading `.env`

```bash
# Source .env from the plugin folder (supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT, ATLAS_PATH_*)
# The plugin folder is the directory containing this SKILL.md
```

### Config Levels

**Basic** (knowledge base root only):

- Required: `ATLAS_BRAIN_PATH`
- Provides: `BRAIN_PATH`

**Project** (active project context):

- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Optional: `ATLAS_PATH_{NAME}` entries (per-project external paths)
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`
- `PROJECT_PATH` resolution:
  1. Convert `ACTIVE_PROJECT` to uppercase, replace `-` with `_` → `{NAME}`
  2. If `ATLAS_PATH_{NAME}` is set → `PROJECT_PATH = that value`
  3. Otherwise → `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
- If no active project: list available projects, ask user to choose

**Full** (brand resources for content):

- All Project variables plus reads context.md, brand-voice.md and visual-identity.md into context:
- `BRAND_VOICE = {PROJECT_PATH}/marketing/brand-voice.md`
- `VISUAL_IDENTITY = {PROJECT_PATH}/marketing/visual-identity.md`

Use the extracted path values **literally** — they are NOT shell environment variables.

## Capabilities

### Knowledge Operations

| What the user wants                                  | Workflow                            |
| ---------------------------------------------------- | ----------------------------------- |
| Save an idea, capture a thought, remember something  | `workflows/capture.md`              |
| Find files about a topic, search notes               | `workflows/search.md` (search mode) |
| What do I know about X, recall, synthesize knowledge | `workflows/search.md` (recall mode) |
| Set up Atlas, initialize brain                       | `workflows/setup.md`                |

### Project Management

| What the user wants                | Workflow                             |
| ---------------------------------- | ------------------------------------ |
| Create a new project               | `project/manage.md` → create section |
| Link an external project           | `project/manage.md` → link section   |
| Unlink an external project         | `project/manage.md` → unlink section |
| List all projects, show projects   | `project/manage.md` → list section   |
| Switch to a project, use project X | `project/manage.md` → use section    |
| Show project details, project info | `project/manage.md` → info section   |

### Project Definition (Interactive Wizards)

| What the user wants                      | Workflow                                  |
| ---------------------------------------- | ----------------------------------------- |
| Define what this project is, set context | `project/define.md` → context section     |
| Define strategy, set goals, vision       | `project/define.md` → strategy section    |
| Define brand voice, tone                 | `project/define.md` → brand section       |
| Define visual identity, colors, style    | `project/define.md` → visuals section     |
| Define audience persona, target user     | `project/define.md` → audience section    |
| Document a competitor                    | `project/define.md` → competitors section |

### Invisible Actions

These should happen automatically without the user needing to ask:

- When user expresses any idea → offer to capture it
- When user asks about a topic → decide between search (file discovery) and recall (deep synthesis) based on the question
- When user mentions a project name → check if it exists and offer to switch

## Agent Orchestration

Atlas uses a locate -> analyze -> domain-agent pattern:

1. **`atlas:locate_knowledge`** — Fast file discovery. Returns paths only, never reads content. Use for: search, finding context before analysis, checking what exists.
2. **`atlas:analyze_knowledge`** — Deep content analysis. Receives paths from `atlas:locate_knowledge`. Use for: recall, understanding patterns, synthesizing knowledge.
3. **Domain agents** — Specialized work. `atlas:market_researcher` for web research, `atlas:content_reviewer` for quality checks, `atlas:strategist` for framework application.

When to use which:

- "Find files about X" → `atlas:locate_knowledge` only
- "What do I know about X" → `atlas:locate_knowledge` → `atlas:analyze_knowledge` (sequentially always, pass the paths from the first to the second)
- "Research the market for X" → `atlas:locate_knowledge` (check existing) → `atlas:market_researcher` (web search)
- "Analyze our competitive position" → `atlas:locate_knowledge` → `atlas:market_researcher` → `atlas:strategist`

### File Ownership Rule

Subagents return data as structured text. The **main agent owns all file creation**. When spawning any subagent, include in the prompt: "Do NOT create any files or folders. Return your findings as text." This prevents duplicate output when the main agent also writes files as part of its workflow.

## Error Handling

### Setup Errors

- **Brain path not configured**: Stop execution, tell user to run setup.
- **Active project missing**: Stop execution, list available projects, ask user to choose.

### File Errors

- **Required file missing**: Stop, show prerequisite. Never create or guess content.
- **Optional file missing**: Warn user, suggest creating it, proceed if confirmed.

### Validation Errors

- **Invalid project name**: Must be kebab-case (lowercase, hyphens only). Show format and example.
- **Duplicate content**: Present options: proceed with different angle, update existing, or cancel.

### General Principles

1. Never fail silently — always inform user
2. Be specific — include file paths, exact errors, clear next steps
3. Don't guess — if data is missing, say so
4. Offer solutions — every error includes what to do next
5. Preserve work — save partial progress when possible
6. Validate early — check prerequisites before starting work

## Reference Files

- **Folder structure**: `reference/folder-structure.md` — single source of truth for PARA structure
- **Project templates**: `reference/project-templates.md` — all file templates for project assets
