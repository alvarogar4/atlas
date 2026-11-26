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
# Supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT, ATLAS_PATH_*, ATLAS_QMD_CMD, ATLAS_QMD_REFRESH, ATLAS_OBSIDIAN_CMD
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

### Project Knowledge Sources

The brain folder is always the primary source. Search it first, with the tool that fits the request (see [Finding Notes](#finding-notes)). An MCP query never replaces that step.

A project can also turn on an external knowledge source, usually a team brain behind an MCP server, in its own `{PROJECT_PATH}/AGENTS.md` or `STRUCTURE.md`. When the task relates to such a project, its context is split between the two places, so query that source as well and combine the results. Follow the project file's own connection steps. When the task relates to no project, or to a project that turns on no external source, use the brain folder only.

Personal notes (career, feedback, journal, anything outside a team-shared project) stay in the brain folder. Never write them into a project's external source.

## Finding Notes

Pick the search tool by the request, not by habit. grep is the habit, and it is the wrong default for a question: it returns unranked matches, and it misses notes written in other words or another language. This table is the only copy of the routing; `reference/search-tools.md` holds the measurements behind it and the grep commands.

| The request is...                                                             | Use                                                        | Why                                                                 |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------- |
| A path you already have (given, in memory, a convention)                      | Read it. No search                                         | Nothing to find                                                     |
| Inside a folder you already know (a client folder, a draft)                   | grep and ls in that folder                                 | Few files, exact strings pin them down                              |
| A question, a topic, "the note about X", location unknown                     | **QMD**: `lex:` keyword lines plus one `vec:` sentence     | Ranked; finds other words and other languages                       |
| A phrase or a name you remember from a note                                   | **QMD** `search` with the phrase in quotes                 | Finds it and ranks it first                                         |
| An exact string inside a note (identifier, code, error), a regular expression | `grep -F` or `grep -E`                                     | Byte-exact                                                          |
| A file name, or part of one                                                   | `find` or Glob                                             | grep reads contents, not names                                      |
| A note written or edited a moment ago, a file that is not Markdown            | grep                                                       | Reads the files as they are now                                     |
| What links to a note, tags, orphans, properties                               | **Obsidian CLI**                                           | Resolves links; a grep for a name also returns plain mentions       |
| QMD or the Obsidian CLI is not available here                                 | grep                                                       | Always there                                                        |

### The defaults, ready to run

When the check for a tool passes (below), these are the first call for a question, a topic or a remembered phrase, before any grep across the whole brain:

```bash
cd "{BRAIN_PATH}"
{QMD} update   # once per session, before the first search, only with ATLAS_QMD_REFRESH=1
# A question or a topic, location unknown. Add the vec: line only when `{QMD} status` shows embedded vectors
{QMD} query $'lex: key words\nlex: other key words\nvec: the question in plain words' --no-rerank -n 5 --format files
# A phrase or a name you remember
{QMD} search '"the phrase"' -n 5 --format files
# What links to a note (only while the Obsidian app is already running)
{OBSIDIAN} vault="{VAULT}" backlinks path="folder/note.md" format=json
```

If QMD also indexes collections outside `{BRAIN_PATH}`, add `-c <name>` for each collection inside it to every search. If the request is scoped to one folder (a project, a client), drop every result outside that folder before opening any, and search the folder with grep if none is left.

Three moments to switch tools:

- **A topic or question searched with grep across the whole brain returned more than about 10 files**, or none of the first ones fits, and QMD has not been tried yet: rerun it as a QMD query instead of narrowing the grep by hand. Exact strings, regular expressions, just-edited notes and non-Markdown files stay on grep, however many files match.
- **Before you move, rename or delete a note**: list its backlinks with the Obsidian CLI while the app is running, and update them in the same change. Without the CLI, grep for the note's name and path, but treat the hits as candidates: edit only links that resolve to the old path (another folder can hold a note with the same name, and many hits are plain mentions), and check `related` entries for the old path too.
- **A question in another language than the notes**: QMD with the `vec:` line in the user's language, when vectors are embedded. Without vectors, write the `lex:` lines in the notes' language.

Read the top 3 to 5 results before answering. If none fits, rephrase once, then fall back to grep.

### Checks and limits

- **grep and find always work.** QMD and the Obsidian CLI are optional. QMD is used only when the config names it (`ATLAS_QMD_CMD`, the absolute path of one executable) and it indexes the brain; check once per session. The Obsidian CLI (`ATLAS_OBSIDIAN_CMD`, or `obsidian`) only while the app is already running (check before every call) and always with the brain's vault named. Where a check fails, use grep and say nothing.
- **A quick lookup needs no agent.** Search directly, read the top 3 to 5 results, answer. Spawn `atlas:locate_knowledge` and `atlas:analyze_knowledge` for deep recall across many notes.
- **Atlas uses these tools, it does not set them up.** Never install QMD, run `{QMD} embed` or `{QMD} pull`, switch the Obsidian CLI on, or start Obsidian to search. Run `{QMD} update` only when the config has `ATLAS_QMD_REFRESH=1`.

The full check, the query syntax and the rules on collections are in `reference/qmd.md`; the Obsidian CLI's check and commands in `reference/obsidian.md` (Obsidian CLI). Read each once, before that tool's first call in a session.

## Brain Paths in Replies

When a chat reply, summary or report names a file or folder inside the brain, write the path relative to the brain root (`{BRAIN_PATH}`), with no leading `/`: `projects/acme-app/marketing/brand-voice.md`, `areas/health/README.md`. It is shorter, and it is the same form the `related` wikilinks use (`reference/cross-referencing.md`). A project that is its own git repo nested inside the brain gets the same form (`projects/{name}/...`).

Files outside the brain (code repos, scratch folders, agent config) keep their absolute paths, since they have no root the user would read them against. Shell commands still use the full path (`{BRAIN_PATH}/projects/...`); this rule is only about how paths are shown to the user.

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
- When user asks about a topic → decide between search (file discovery) and recall (deep synthesis) based on the question, and pick the search tool by the kind of request per [Finding Notes](#finding-notes): a question or a topic goes to QMD first when it is available, not to grep
- When user mentions a project name → check if it exists and offer to switch
- **When a project becomes active** → check for `{PROJECT_PATH}/STRUCTURE.md`; if present, treat it as the authoritative structure/naming/frontmatter/linking spec for that project (plugin defaults are fallback) per [Project Structure Spec](#project-structure-spec)
- **When the task relates to a project** → check its `AGENTS.md`/`STRUCTURE.md` for an external knowledge source (for example a team brain MCP). If it declares one, query it as well as the brain folder, per [Project Knowledge Sources](#project-knowledge-sources)
- **Before any git operation scoped to a project** (pull, push, status, branch, commit) → a project can be its own git repo nested inside the brain (separate remote, separate branch, often team-shared and gitignored from the brain repo). NEVER assume the brain-root repo covers it and NEVER infer repo membership from the parent. Always resolve the real boundary first with `git -C {PROJECT_PATH} rev-parse --show-toplevel` (and `--abbrev-ref HEAD`), then operate on that repo. A nested project repo is invisible to the brain repo's `git status`, so a clean / "up to date" parent does NOT mean the project is synced.
- **After creating or updating any file** → populate the `related` frontmatter property with vault-root paths to connected files per `reference/cross-referencing.md`

## Agent Orchestration

Atlas uses a locate -> analyze -> domain-agent pattern:

1. **`atlas:locate_knowledge`** — File discovery across the whole brain. Returns paths only, never reads content. Use for: broad searches, finding context before analysis, checking what exists. A single lookup is faster done directly (see [Finding Notes](#finding-notes)).
2. **`atlas:analyze_knowledge`** — Deep content analysis. Receives paths from `atlas:locate_knowledge`. Use for: recall, understanding patterns, synthesizing knowledge.
3. **Domain agents** — Specialized work. `atlas:market_researcher` for web research, `atlas:content_reviewer` for quality checks, `atlas:strategist` for framework application.

When to use which:

- "Where is the note about X" → search directly with the tool that fits; no agent
- "Find everything about X" → `atlas:locate_knowledge` only
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
2. Be specific — include file paths (brain paths relative to the brain root, see [Brain Paths in Replies](#brain-paths-in-replies)), exact errors, clear next steps
3. Don't guess — if data is missing, say so
4. Offer solutions — every error includes what to do next
5. Preserve work — save partial progress when possible
6. Validate early — check prerequisites before starting work

## Reference Files

- **Folder structure**: `reference/folder-structure.md` — single source of truth for PARA structure
- **Cross-referencing**: `reference/cross-referencing.md` — `related` property format, tag guidelines, series navigation
- **Search tools**: `reference/search-tools.md` — grep commands and the measurements behind the routing (the routing table itself is in [Finding Notes](#finding-notes))
- **QMD**: `reference/qmd.md` — config, availability check, commands, query syntax, index freshness
- **Obsidian features**: `reference/obsidian.md` — callouts, embeds, highlights, comments, the CLI (availability check and commands), defuddle extraction
- **Obsidian Bases**: `reference/obsidian-bases.md` — `.base` file schema, formulas, views, default project dashboard template
- **Project templates**: `templates/` — individual template files for all project assets
