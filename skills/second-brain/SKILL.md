---
name: second-brain
description: Core operations for the personal knowledge base. Use WHENEVER the user mentions notes, memories, knowledge, brain, ideas, captures, projects, or wants to store/retrieve/organize information. This skill provides the patterns for all knowledge base operations.
---

# Second Brain Foundation

Core operations for the personal knowledge base using the PARA method.

## Config

Atlas reads configuration from multiple sources in priority order:

### Config Chain

1. **Conversation context**: `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT` values already in context (system reminders, CLAUDE.md, AGENTS.md)
2. **Shell environment**: `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, `ATLAS_PATH_*` exported in the environment
3. **Shared config file**: `${ATLAS_CONFIG:-~/.config/atlas/.env}`. This is the canonical location, read by every agent
4. **Legacy `.env`**: `.env` at the root of the Atlas repo or Claude Code plugin folder (two levels above this SKILL.md). Read-only fallback for installs that predate the shared file
5. **Error**: "Brain not configured. Let's set it up — where should I store your knowledge base?"

### Reading `.env`

```bash
# Supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT, ATLAS_PATH_*
CONFIG="${ATLAS_CONFIG:-$HOME/.config/atlas/.env}"
[ -f "$CONFIG" ] && cat "$CONFIG"
```

All writes (setup, creating or switching projects) go to the shared config file, never to the legacy `.env`. If only the legacy file exists, copy its values into the shared file on the first write.

### Config Levels

**Basic** (knowledge base root only):

- Required: `ATLAS_BRAIN_PATH`
- Provides: `BRAIN_PATH`

**Project** (active project context):

- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`
- `PROJECT_PATH` resolution: `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
- If no active project: list available projects, ask user to choose
- `STRUCTURE = {PROJECT_PATH}/STRUCTURE.md` — if this file exists, it is **authoritative** for that project's folder layout, naming, frontmatter, and cross-linking (see [Project Structure Spec](#project-structure-spec))

**Full** (brand resources for content):

- All Project variables plus reads these into context:
- `CONTEXT = {PROJECT_PATH}/context.md`
- `STRATEGY = {PROJECT_PATH}/strategy/strategy.md`
- `BRAND_VOICE = {PROJECT_PATH}/marketing/brand-voice.md`
- `VISUAL_IDENTITY = {PROJECT_PATH}/marketing/visual-identity.md`

Use the extracted path values **literally** — they are NOT shell environment variables.

### Project Structure Spec

A project may pin its own folder layout, file naming, frontmatter, and cross-link style in a `STRUCTURE.md` at its root (`{PROJECT_PATH}/STRUCTURE.md`). These specs are often team-imposed and intentionally differ from the Atlas PARA default.

**Precedence**: when `{PROJECT_PATH}/STRUCTURE.md` exists, it is the **authoritative source** for that project — where files go, how they are named, what frontmatter they carry, and how they link. The plugin default (`reference/folder-structure.md`) becomes the **fallback**: consult it only for what `STRUCTURE.md` leaves unspecified. On any conflict (paths, phase files, frontmatter keys, wikilinks vs markdown links), `STRUCTURE.md` wins.

**When to read it**: read `STRUCTURE.md` before any operation that depends on layout — capture, content creation, file placement, naming, frontmatter, or cross-linking. Never assume the default PARA layout for a project that ships a `STRUCTURE.md`.

**No spec**: if `{PROJECT_PATH}/STRUCTURE.md` is absent, use `reference/folder-structure.md` exactly as before.

## Capabilities

### Knowledge Operations

| What the user wants                                  | Workflow                            |
| ---------------------------------------------------- | ----------------------------------- |
| Save an idea, capture a thought, remember something  | `workflows/capture.md`              |
| Find files about a topic, search notes               | `workflows/search.md` (search mode) |
| What do I know about X, recall, synthesize knowledge | `workflows/search.md` (recall mode) |
| Set up Atlas, initialize brain                       | `workflows/setup.md`                |

### Project Foundations

| What the user wants                      | Workflow                         |
| ---------------------------------------- | -------------------------------- |
| Define what this project is, set context | `foundations/context.md`         |
| Define strategy, set goals, vision       | `foundations/strategy.md`        |
| Define brand voice, tone                 | `foundations/brand-voice.md`     |
| Define visual identity, colors, style    | `foundations/visual-identity.md` |

### Entity Management

| What the user wants                        | Entity                                                  |
| ------------------------------------------ | ------------------------------------------------------- |
| Create, list, switch, or view project info | `entities/project.md`                                   |
| Create, list, edit, or archive themes      | `entities/theme.md`                                     |
| Create, list, edit, or delete competitors  | `entities/competitor.md`                                |
| Create, list, edit, or delete audiences    | `entities/audience.md`                                  |
| Plan or view content calendar              | `entities/calendar.md` & `marketing-content/calendar/*` |

### Invisible Actions

These should happen automatically without the user needing to ask:

- When user expresses any idea → offer to capture it
- When user asks about a topic → decide between search (file discovery) and recall (deep synthesis) based on the question
- When user mentions a project name → check if it exists and offer to switch
- **When a project becomes active** → check for `{PROJECT_PATH}/STRUCTURE.md`; if present, treat it as the authoritative structure/naming/frontmatter/linking spec for that project (plugin defaults are fallback) per [Project Structure Spec](#project-structure-spec)
- **Before any git operation scoped to a project** (pull, push, status, branch, commit) → a project can be its own git repo nested inside the brain (separate remote, separate branch, often team-shared and gitignored from the brain repo). NEVER assume the brain-root repo covers it and NEVER infer repo membership from the parent. Always resolve the real boundary first with `git -C {PROJECT_PATH} rev-parse --show-toplevel` (and `--abbrev-ref HEAD`), then operate on that repo. A nested project repo is invisible to the brain repo's `git status`, so a clean / "up to date" parent does NOT mean the project is synced.
- **After creating or updating any file** → populate the `related` frontmatter property with vault-root paths to connected files per `reference/cross-referencing.md`

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

### Portability (any agent)

Atlas runs in Claude Code as a plugin and in any other agent that loads Agent Skills (Codex, Cursor, Gemini CLI, Copilot, OpenCode and others). Workflows are written with Claude Code names; translate them like this:

- **`atlas:<name>`** is the Atlas skill or subagent `<name>`. Skills live in `{SKILLS_DIR}/<name>/SKILL.md`.
- **`{SKILLS_DIR}`** is the folder holding the Atlas skills, i.e. the parent of this skill's directory (`${CLAUDE_PLUGIN_ROOT}/skills` in Claude Code).
- **Subagents**: each Atlas agent is defined in `{SKILLS_DIR}/second-brain/agents/<name>.md` (`locate_knowledge`, `analyze_knowledge`, `market_researcher`, `content_reviewer`, `strategist`). In Claude Code, dispatch with `subagent_type: atlas:<name>`. In a harness that can spawn subagents with a custom prompt, spawn one with that file's body as its instructions. Otherwise, follow the file yourself inline and keep its output contract.
- **Asking the user**: use the harness's structured question tool if it has one (AskUserQuestion in Claude Code). Otherwise ask in plain text, one question at a time, and wait for the answer.

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
- **Cross-referencing**: `reference/cross-referencing.md` — `related` property format, tag guidelines, series navigation
- **Obsidian features**: `reference/obsidian.md` — callouts, embeds, highlights, comments, CLI commands, defuddle extraction
- **Obsidian Bases**: `reference/obsidian-bases.md` — `.base` file schema, formulas, views, default project dashboard template
- **Project templates**: `templates/` — individual template files for all project assets
