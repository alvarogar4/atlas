# Atlas Conversational Rework Implementation Plan

## Overview

Transform Atlas from a CLI-command-based interaction model to a truly conversational one. Atlas v2.0.0 consolidated Jarvis's 54 components into 9, but preserved the CLI-style interaction patterns verbatim. This plan addresses all 12 issues identified in `thoughts/research/2026-02-13-atlas-vs-jarvis-comparison.md` — removing argument parsing, dispatch tables, usage blocks, and 237 slash-command references while preserving all workflow logic, checkpoints, agent orchestration, and file conventions.

Additionally: add `.env` config support and deduplicate shared patterns.

## Current State Analysis

**Repository**: 70 source files (4 SKILL.md, 14 workflow files, 5 agents, 6 channels, 12 frameworks, root files)

**CLI patterns to remove**:
- 3 `argument-hint` frontmatter entries (SKILL.md lines 6)
- 3 dispatch tables with 34 combined entries
- 13+ "No Arguments -> Show Usage" blocks (100+ lines of man-page help)
- 20+ `**Trigger**` lines in workflow files
- 237 `/atlas:` slash-command references across 23 files

**Duplication to consolidate**:
- Config reading: 8 files hardcode `~/.claude/CLAUDE.md`
- Framework selection table: 4 copies with different phrasing
- Content folder discovery: 6 copies with 2 incompatible variants
- Channel validation/table: 3 copies
- Command reference: 3 copies (CLAUDE.md, help.md, README.md)

**What stays unchanged**:
- All 12 framework templates in `business_strategy/frameworks/`
- All 6 channel guideline files in `marketing_content/channels/`
- All reference files (`metrics.md`, `review-checklist.md`, `folder-structure.md`, `project-templates.md`)
- Decision log template
- Content folder structure convention (`{date}_{topic}/1_research.md` through `5_results-{channel}.md`)
- STOP AND WAIT checkpoint enforcement
- Agent orchestration (locate -> analyze -> domain-agent)
- All output format templates in workflow files

## Desired End State

After this plan is complete:

1. **No CLI patterns remain** — No dispatch tables, argument parsing, usage blocks, or Trigger lines in any file
2. **Skills are knowledge docs** — SKILL.md files describe capabilities, intent routing, shared patterns, and references to workflow files
3. **Workflows are guides** — Workflow files describe step-by-step processes without CLI scaffolding. Next-step suggestions use natural language
4. **CLAUDE.md is a personality doc** — Describes who Atlas is, what it can do, how it detects intent, and how it behaves proactively. No command tables
5. **Config is portable** — Single config pattern with `.env` -> `~/.claude/CLAUDE.md` chain, defined once
6. **No duplication** — Each piece of knowledge has one source of truth
7. **Slash commands still work** — Skills remain `user_invocable: true`, so power users can still type `/atlas:marketing:content research ai-trends`. But Atlas never _suggests_ slash commands

**Verification**: Read every `.md` file in the repo and confirm zero occurrences of:
- `argument-hint:` in frontmatter
- `## Action Dispatch` or `## No Arguments` sections
- `**Trigger**:` lines in workflow files
- `/atlas:` in output templates or next-step suggestions (allowed only in: SKILL.md description frontmatter for Claude Code routing)

## What We're NOT Doing

- **Not changing the skill/agent architecture** — 4 skills, 5 agents stays
- **Not renaming files or directories** — All paths remain stable
- **Not changing the content pipeline** — research -> plan -> write -> review -> results is preserved
- **Not modifying channel guidelines or framework templates** — These are reference knowledge, not interaction patterns
- **Not changing the PARA method or folder structure** — Brain organization stays identical
- **Not building a config management system** — Just a simple read chain, not an abstraction layer
- **Not changing `user_invocable`** — Skills stay invocable, we're changing what happens when they load
- **Not touching `marketing_visuals/tools/`** — Processing scripts and schema generation assets are unchanged

---

## Implementation Approach

Four phases, ordered by dependency:

1. **Phase 1: SKILL.md Transformation** — Rewrite all 4 SKILL.md files. This includes the new config pattern, intent routing, state detection, and deduplication of shared patterns. SKILL.md is the entry point for everything, so it must be correct first.
2. **Phase 2: Workflow Transformation** — Clean all 14+ workflow/project files. Remove CLI scaffolding, replace slash-command references with natural language, reference shared patterns from SKILL.md.
3. **Phase 3: CLAUDE.md Rewrite** — Transform the personality doc from command reference to conversational behavior guide.
4. **Phase 4: Agents + Cleanup** — Update agent config references, delete orphaned files, simplify README.md.

---

## Phase 1: SKILL.md Transformation

### Overview

Rewrite all 4 SKILL.md files from CLI dispatchers to conversational knowledge docs. Define the `.env` config chain once. Add intent-to-action mapping. Consolidate duplicated patterns.

### Changes Required

#### 1. `skills/second_brain_foundation/SKILL.md` (139 lines -> ~120 lines)

**File**: `skills/second_brain_foundation/SKILL.md`

**Remove**:
- Line 6: `argument-hint: "<action> [args]"` — delete entirely
- Lines 52-75: "Action Dispatch" section (dispatch table + "Parse the first argument" instruction)
- Lines 77-111: "No Arguments -> Show Usage" block (35 lines of CLI help)

**Rewrite Setup section** (lines 13-50) to define the canonical config chain:

```markdown
## Config

Atlas reads configuration from multiple sources in priority order:

### Config Chain

1. **Conversation context**: Check current `system-reminder` for `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT` already loaded from CLAUDE.md
2. **`.env` file**: Read `.env` in the current working directory (or repo root)
3. **`~/.claude/CLAUDE.md`**: Parse for `ATLAS_BRAIN_PATH=` and `ATLAS_ACTIVE_PROJECT=`
4. **Error**: "Brain not configured. Let's set it up — where should I store your knowledge base?"

### Reading `.env`

```bash
# Source .env if it exists (supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT)
if [ -f .env ]; then source .env; fi
if [ -f "$PWD/.env" ]; then source "$PWD/.env"; fi
```

### Config Levels

**Basic** (knowledge base root only):
- Required: `ATLAS_BRAIN_PATH`
- Provides: `BRAIN_PATH`

**Project** (active project context):
- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
- If no active project: list available projects, ask user to choose

**Full** (brand resources for content):
- All Project variables plus:
- `BRAND_VOICE = {PROJECT_PATH}/marketing/brand-voice.md`
- `VISUAL_IDENTITY = {PROJECT_PATH}/marketing/visual-identity.md`

Use the extracted path values **literally** — they are NOT shell environment variables.
```

**Add new "Capabilities" section** replacing the dispatch table:

```markdown
## Capabilities

### Knowledge Operations

| What the user wants | Workflow |
|---|---|
| Save an idea, capture a thought, remember something | `workflows/capture.md` |
| Find files about a topic, search notes | `workflows/search.md` (search mode) |
| What do I know about X, recall, synthesize knowledge | `workflows/search.md` (recall mode) |
| Set up Atlas, initialize brain | `workflows/setup.md` |

### Project Management

| What the user wants | Workflow |
|---|---|
| Create a new project | `project/manage.md` → create section |
| List all projects, show projects | `project/manage.md` → list section |
| Switch to a project, use project X | `project/manage.md` → use section |
| Show project details, project info | `project/manage.md` → info section |

### Project Definition (Interactive Wizards)

| What the user wants | Workflow |
|---|---|
| Define what this project is, set context | `project/define.md` → context section |
| Define strategy, set goals, vision | `project/define.md` → strategy section |
| Define brand voice, tone | `project/define.md` → brand section |
| Define visual identity, colors, style | `project/define.md` → visuals section |
| Define audience persona, target user | `project/define.md` → audience section |
| Document a competitor | `project/define.md` → competitors section |

### Invisible Actions

These should happen automatically without the user needing to ask:
- When user expresses any idea → offer to capture it
- When user asks about a topic → decide between search (file discovery) and recall (deep synthesis) based on the question
- When user mentions a project name → check if it exists and offer to switch
```

**Add new "Agent Orchestration" section**:

```markdown
## Agent Orchestration

Atlas uses a locate -> analyze -> domain-agent pattern:

1. **locate_knowledge** — Fast file discovery. Returns paths only, never reads content. Use for: search, finding context before analysis, checking what exists.
2. **analyze_knowledge** — Deep content analysis. Receives paths from locate_knowledge. Use for: recall, understanding patterns, synthesizing knowledge.
3. **Domain agents** — Specialized work. `market_researcher` for web research, `content_reviewer` for quality checks, `strategist` for framework application.

When to use which:
- "Find files about X" → locate_knowledge only
- "What do I know about X" → locate_knowledge → analyze_knowledge
- "Research the market for X" → locate_knowledge (check existing) → market_researcher (web search)
- "Analyze our competitive position" → locate_knowledge → strategist
```

**Keep unchanged**: Error Handling section (lines 113-133), Reference Files section (lines 135-139).

---

#### 2. `skills/marketing_content/SKILL.md` (166 lines -> ~140 lines)

**File**: `skills/marketing_content/SKILL.md`

**Remove**:
- Line 6: `argument-hint: "<action> [channel] [topic]"`
- Lines 28-43: "Action Dispatch" table
- Lines 44-74: "No Arguments -> Show Usage" block (31 lines of CLI help)
- Lines 160-165: Error handling section with slash-command references

**Rewrite Setup section** (lines 13-27):

```markdown
## Config

Follow the **Config Chain** from `second_brain_foundation/SKILL.md` (project-level config required).

Requires: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`
```

This replaces the 12-line section that hardcodes `~/.claude/CLAUDE.md` and includes slash-command error messages.

**Add new "Content Lifecycle" section** replacing the dispatch table:

```markdown
## Content Lifecycle

Content follows a strict pipeline. Each step produces a numbered file:

```
research (1_research.md) → plan (2_plan.md) → write (3_draft-{channel}.md) → review (4_review-{channel}.md) → [publish] → results (5_results-{channel}.md)
```

**Starting point detection**: When a user wants to create content, determine where to start:
- "I want to write about X" → Check if research exists. If not, start at research
- "Let's plan content for X" → Check if research exists. If not, start at research
- "Review my blog post about X" → Check if draft exists. If not, tell user to write first
- Always enforce: research before plan, plan before write, write before review

### Capabilities

| What the user wants | Workflow |
|---|---|
| Research a content topic | `workflow/research.md` |
| Plan content structure | `workflow/plan.md` |
| Write content for a channel | `workflow/write.md` |
| Review content quality (mandatory) | `workflow/review.md` |
| Document content performance | `workflow/results.md` |
| View content calendar | `calendar/view.md` |
| Plan quarterly content | `calendar/plan.md` |
| Create a content theme | `themes/manage.md` → add section |
| List themes | `themes/manage.md` → list section |
| Edit a theme | `themes/manage.md` → edit section |
| Archive a theme | `themes/manage.md` → remove section |

### State Detection

Before starting any content workflow, check for existing work:

```bash
TOPIC_SLUG=$(echo "{topic}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${TOPIC_SLUG}* 2>/dev/null | head -1)
```

If folder found, check which files exist to determine current state:
- Has `1_research.md` → research done
- Has `2_plan.md` → planning done
- Has `3_draft-{channel}.md` → draft exists for that channel
- Has `4_review-{channel}.md` → review done for that channel
- Has `5_results-{channel}.md` → results recorded

Report state to user: "I found existing work on this topic: [research done, blog draft in progress]. Where would you like to continue?"
```

**Keep unchanged**: Content Folder Structure (lines 76-89), Channel Validation (lines 100-104), Channel Writing Guidelines table (lines 106-117), Shared Writing Patterns (lines 119-158).

**Rewrite Error Handling** (lines 160-165):

```markdown
## Error Handling

- **Missing prerequisite**: Tell user which step is needed first and offer to start it. Example: "This topic needs research before we can plan. Want me to start researching?"
- **Content folder not found**: "I don't see any work on this topic yet. Want to start with research?"
- **Agent failure**: Log error, present partial results, offer to retry
- **Checkpoint timeout**: Save progress, allow resume
```

---

#### 3. `skills/business_strategy/SKILL.md` (106 lines -> ~80 lines)

**File**: `skills/business_strategy/SKILL.md`

**Remove**:
- Line 6: `argument-hint: "<action> [args]"`
- Lines 22-36: "Action Dispatch" section (dispatch table + "Parse the first argument")
- Lines 38-70: "No Arguments -> Show Usage" block (33 lines of CLI help)

**Rewrite Setup** (lines 13-20):

```markdown
## Config

Follow the **Config Chain** from `second_brain_foundation/SKILL.md` (basic config required, project config for project-scoped analysis).

Requires: `BRAIN_PATH` (minimum), `ACTIVE_PROJECT` (when analyzing a specific project)
```

**Add new "Capabilities" section**:

```markdown
## Capabilities

| What the user wants | Workflow |
|---|---|
| Analyze a strategic question, understand position | `workflows/analyze.md` |
| Document a business decision | `workflows/decision.md` |
| Weekly/monthly/quarterly review | `workflows/review.md` |

### Intent Detection for Review Period

When user asks for a review, determine the period:
- "weekly review", "how was this week" → weekly mode
- "monthly review", "month in review" → monthly mode
- "quarterly review", "Q1 review", "strategic review" → quarterly mode
- "review" with no qualifier → default to weekly
```

**Keep unchanged**: Framework Selection Guide (lines 72-88), Storage Locations (lines 98-105).

**Rewrite Error Handling** (lines 90-96):

```markdown
## Error Handling

- **Brain not configured**: "Let's set up Atlas first — where should I store your knowledge base?"
- **No active project** (when needed): List available projects, ask user to choose
- **Required file missing**: Explain what's needed and offer to create it
- **External service failure**: Retry once, continue with available data. Never fabricate information
```

---

#### 4. `skills/marketing_visuals/SKILL.md` (61 lines -> ~75 lines)

**File**: `skills/marketing_visuals/SKILL.md`

This skill is already clean (no CLI patterns, `user_invocable: false`). Only additive changes.

**Add "Workflow Chaining" section** after the Decision Tree (after line 18):

```markdown
## Workflow Chaining

Visual tools compose together for common workflows:

| Scenario | Chain |
|---|---|
| Blog hero image | `guides/ai-prompting.md` → generate image → `tools/processing.md` (crop to 1200x600) → optimize |
| Schema diagram | `tools/schema-generation.md` (HTML+CSS → PNG) → `tools/processing.md` (optimize) |
| Photo for social | `tools/processing.md` (remove background → crop to 1080x1080 → polish → optimize) |
| OG card | `guides/ai-prompting.md` → generate → `tools/processing.md` (crop to 1200x630) |

Always read the project's visual identity first for brand colors and style defaults.
```

**Keep everything else unchanged.**

### Success Criteria

#### Automated Verification:
- [x] `grep -r 'argument-hint' skills/*/SKILL.md` returns zero results
- [x] `grep -r '## Action Dispatch' skills/*/SKILL.md` returns zero results
- [x] `grep -r '## No Arguments' skills/*/SKILL.md` returns zero results
- [x] `grep -r 'Parse the first argument' skills/*/SKILL.md` returns zero results
- [x] `grep -c '/atlas:' skills/second_brain_foundation/SKILL.md` returns 0 (no slash-command references)
- [x] `grep -c '/atlas:' skills/marketing_content/SKILL.md` returns 0
- [x] `grep -c '/atlas:' skills/business_strategy/SKILL.md` returns 0
- [x] Each SKILL.md has a "Capabilities" or "Content Lifecycle" section with an intent-to-workflow table
- [x] `second_brain_foundation/SKILL.md` has a "Config" section defining the `.env` chain
- [x] Other SKILL.md files reference `second_brain_foundation/SKILL.md` for config

#### Manual Verification:
- [ ] Invoking `/atlas:second_brain:foundation` still loads the skill (user_invocable works)
- [ ] Natural language like "save this idea" can be routed via the intent table
- [ ] Config reads from `.env` when present, falls back to `~/.claude/CLAUDE.md`

---

## Phase 2: Workflow Transformation

### Overview

Clean all 14 workflow files + 2 project files. Remove CLI scaffolding (Trigger lines, usage blocks, slash-command references). Replace argument parsing with "determine from conversation context". Keep all actual workflow logic, checkpoints, and agent orchestration.

### Pattern: What Changes in Every Workflow File

For each workflow file, apply these transformations:

1. **Remove `**Trigger**: /atlas:...` line** (usually line 3)
2. **Remove `## No Arguments -> Show Usage` block** (10-35 lines of CLI help)
3. **Replace `Parse arguments` step** with "Determine {topic/channel} from conversation context"
4. **Replace content folder discovery** with "Follow Content Folder Discovery from SKILL.md" (marketing workflows only)
5. **Replace slash-command next-step suggestions** with natural language
6. **Replace slash-command error messages** with conversational alternatives
7. **Keep**: Purpose line, checkpoint enforcement, actual process steps, agent orchestration, output format templates

### Changes Required

#### 1. `second_brain_foundation/workflows/setup.md`

**File**: `skills/second_brain_foundation/workflows/setup.md`

**Remove**: Line 3 (`**Trigger**: /atlas:second_brain:foundation setup`)

**Update**: Line 11 — change check from `~/.claude/CLAUDE.md` only to the full config chain:

```markdown
### 1. Check if Already Configured

Follow the Config Chain from SKILL.md. If `ATLAS_BRAIN_PATH` is found in any source, tell user it's already configured, show the path, ask if they want to reconfigure.
```

**Update**: Step 3 (lines 33-48) — support writing config to `.env` as well:

```markdown
### 3. Save Configuration

Ask the user where to store the config:

Options:
1. `.env` file in current directory (portable, works with any tool)
2. `~/.claude/CLAUDE.md` (Claude Code-specific)

**If `.env`**: Create or update `.env`:
```
ATLAS_BRAIN_PATH={USER_PROVIDED_PATH}
```

**If `~/.claude/CLAUDE.md`**: Append Atlas configuration section (same as current).
```

**Update**: Step 6 (lines 92-114) — Brain README should not contain slash commands:

Replace lines 109-113 with:
```markdown
## Quick Start

- Capture an idea by telling Atlas to save it
- Search your notes by asking about any topic
- Deep recall by asking "what do I know about X?"
```

**Update**: Step 7 confirm output (lines 116-134) — replace slash commands:

```markdown
Atlas initialized!

Brain location: {path}

Directories created:
- inbox/
- projects/
- areas/
- resources/
- archives/
- .context/

Next steps:
1. Edit {path}/.context/preferences.md with your preferences
2. Try capturing your first idea — just tell me something to remember
```

---

#### 2. `second_brain_foundation/workflows/capture.md`

**File**: `skills/second_brain_foundation/workflows/capture.md`

**Remove**: Line 3 (`**Trigger**: /atlas:second_brain:foundation idea [text]`)
**Remove**: Lines 7-21 (entire "No Arguments -> Show Usage" block + "Then stop.")

**Replace** with:

```markdown
**Purpose**: Quick capture an idea to inbox with minimal friction.

**Prerequisite**: The user provides or implies an idea to save. If nothing to capture is clear from the conversation, ask "What would you like me to save?"
```

The rest of the file (lines 23-57) stays unchanged — the capture process itself is clean.

---

#### 3. `second_brain_foundation/workflows/search.md`

**File**: `skills/second_brain_foundation/workflows/search.md`

**Remove**: Line 5 (`**Trigger**: /atlas:second_brain:foundation search [query]`)
**Remove**: Line 32 (`**Trigger**: /atlas:second_brain:foundation recall [topic]`)

**Update** the "no results" message on line 26:

```markdown
If no results: "No notes found for '{query}'. Want me to capture something about this topic?"
```

(Removes the `/atlas:second_brain:foundation idea` reference)

The rest stays unchanged — agent orchestration and recall process are clean.

---

#### 4. `second_brain_foundation/workflows/help.md` — DELETE

**File**: `skills/second_brain_foundation/workflows/help.md`

**Delete this file entirely.** It's 94 lines of pure CLI command reference. In the conversational model, CLAUDE.md's capabilities section handles "what can you do?" questions. The intent routing tables in SKILL.md handle "how do I do X?" routing.

Also remove the `help` entry from the capabilities table in `second_brain_foundation/SKILL.md` (it was already excluded from the rewrite above).

---

#### 5. `second_brain_foundation/project/manage.md`

**File**: `skills/second_brain_foundation/project/manage.md`

**Remove all Trigger lines**: Lines 9, 65, 98, 124

**Update project-create output** (lines 37-59) — remove slash commands from next-steps:

```markdown
5. Output:

Project created: {name}

Structure:
  projects/{name}/
  └── README.md

Folders are created on-demand as you define each aspect.

Active project set to: {name}

Next steps (recommended order):
  1. Define what this project is (context)
  2. Define project strategy
  3. Document competitors
  4. Define brand voice
  5. Define visual identity
  6. Define target audience

Want to start defining the project context?
```

**Update project-list output** (line 91) — remove slash command:

```markdown
To switch projects, just tell me which one to use.
```

(Replaces: `Use: /atlas:second_brain:foundation project-use [name] to switch`)

---

#### 6. `second_brain_foundation/project/define.md`

**File**: `skills/second_brain_foundation/project/define.md`

**Remove all Trigger lines**: Lines 13, 54, 92, 129, 164, 202

**Update all "Next:" output lines** to natural language:

- Line 47: `Next: project-strategy to define strategy` → `Next: Want to define the project strategy?`
- Line 85: `Next: project-competitors or project-brand` → `Next: Want to document competitors or define brand voice?`
- Line 122: `Next: project-visuals for visual identity` → `Next: Want to define the visual identity?`

---

#### 7. `marketing_content/workflow/research.md`

**File**: `skills/marketing_content/workflow/research.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content research <topic>`)
**Remove**: Lines 11-32 (entire "No Arguments -> Show Usage" block, 22 lines)

**Update** line 40:

```markdown
1. **Determine topic**: Use the topic from conversation. Slugify for folder naming.
```

(Replaces: `1. **Parse arguments**: All arguments = topic (used as folder slug).`)

**Update** lines 69-73 — reference SKILL.md's canonical pattern:

```markdown
5. **Check for existing content folder** (follow Content Folder Discovery from SKILL.md):
```

(Keep the actual bash code since workflows need to be executable, but add the reference.)

**Update** output template (lines 207-214):

```markdown
### Output

Research saved: ${CONTENT_FOLDER}/1_research.md

Review the research file. Ready to plan the content structure?
```

(Replaces: `run: /atlas:marketing:content plan {topic}`)

---

#### 8. `marketing_content/workflow/plan.md`

**File**: `skills/marketing_content/workflow/plan.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content plan <topic>`)
**Remove**: Lines 11-32 (entire "No Arguments -> Show Usage" block)

**Update** line 40: `1. **Determine topic**: Use the topic from conversation.`

**Remove** channel table duplicate (lines 67-74) — already in SKILL.md. Replace with:

```markdown
Read the corresponding writing guidelines from the channel files listed in SKILL.md.
```

**Update** line 47: `If not found → "I don't see a content folder for this topic. Want to start with research?"`

**Update** line 54: `If missing → "Research hasn't been done yet for this topic. Want to start there?"`

**Update** output template (lines 144-152):

```markdown
### Output

Content brief approved and saved: ${CONTENT_FOLDER}/2_plan.md

Ready to write? Which channel should we start with?
```

**Remove** line 182: `**Status**: Brief approved. Ready for /atlas:marketing:content write <channel> {topic}`

Replace with: `**Status**: Brief approved. Ready for writing.`

---

#### 9. `marketing_content/workflow/write.md`

**File**: `skills/marketing_content/workflow/write.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content write <channel> <topic>`)
**Remove**: Lines 24-53 (entire "No Arguments -> Show Usage" block, 30 lines)

**Remove** channel table duplicate (lines 9-18) — already in SKILL.md. Replace with:

```markdown
## Channel-Specific Guidelines (CRITICAL)

**You MUST read the appropriate channel guidelines before writing.** See the channel table in SKILL.md.
```

**Update** line 61: `1. **Determine channel and topic**: Use the channel and topic from conversation.`

**Update** line 66-67 — reference SKILL.md discovery:

```markdown
2. **Find content folder** (follow Content Folder Discovery from SKILL.md):
```

**Update** line 74: `If missing → "The content brief isn't ready yet. Want to create one?"`

**Update** output template (lines 143-150):

```markdown
### Output

Draft saved: ${CONTENT_FOLDER}/3_draft-${channel}.md

Ready for quality review?
```

---

#### 10. `marketing_content/workflow/review.md`

**File**: `skills/marketing_content/workflow/review.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content review <channel> <topic>`)
**Remove**: Lines 27-50 (entire "No Arguments -> Show Usage" block)

**Update** line 58: `1. **Determine channel and topic**: Use the channel and topic from conversation.`

**Update** line 66: `If missing → "I don't see a draft for this channel yet. Want to write it?"`

**Update** line 151: `Next: Edit draft manually, then let me re-review.` (removes slash command)

**Update** output (lines 200-206):

```markdown
### Output

Content is ready! You can now:
- Copy content from the draft to your publishing platform
- Use image prompts in resources/ to generate visuals

After publishing, I can help track performance results.
```

---

#### 11. `marketing_content/workflow/results.md`

**File**: `skills/marketing_content/workflow/results.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content results <channel> <topic>`)
**Remove**: Lines 12-34 (entire "No Arguments -> Show Usage" block)

**Update** line 42: `1. **Determine channel and topic**: Use the channel and topic from conversation.`

---

#### 12. `marketing_content/calendar/plan.md`

**File**: `skills/marketing_content/calendar/plan.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content calendar-plan`)

No other changes needed — this file is already relatively clean.

---

#### 13. `marketing_content/calendar/view.md`

**File**: `skills/marketing_content/calendar/view.md`

**Remove**: Line 3 (`**Trigger**: /atlas:marketing:content calendar-view`)

No other changes needed.

---

#### 14. `marketing_content/themes/manage.md`

**File**: `skills/marketing_content/themes/manage.md`

**Remove all Trigger lines**: Lines 9, 89, 129, 182

**Remove all "No Arguments -> Show Usage" blocks**:
- Lines 14-30 (theme-add usage)
- Lines 134-147 (theme-edit usage)
- Lines 188-200 (theme-remove usage)

**Update output** in theme-add (lines 76-83) — replace slash commands:

```markdown
### Output

Theme created: {name}
Path: marketing/themes/{slug}.md

Next steps:
- Plan quarterly content with this theme
- Start researching content for this theme

Want to do either of these now?
```

---

#### 15. `business_strategy/workflows/analyze.md`

**File**: `skills/business_strategy/workflows/analyze.md`

**Remove**: Line 3 (`**Trigger**: /atlas:business:strategy analyze [topic]`)

**Remove** framework table duplicate (lines 39-52) — already in SKILL.md. Replace with:

```markdown
4. **Select appropriate framework** from the Framework Selection Guide in SKILL.md.
```

**Update** output (line 97): `Next: Review full analysis or document a decision about this topic.`

(Replaces: `Next: Review full analysis or /atlas:business:strategy decision {topic}`)

---

#### 16. `business_strategy/workflows/decision.md`

**File**: `skills/business_strategy/workflows/decision.md`

**Remove**: Line 3 (`**Trigger**: /atlas:business:strategy decision [topic]`)

No other slash-command references to update.

---

#### 17. `business_strategy/workflows/review.md`

**File**: `skills/business_strategy/workflows/review.md`

**Remove**: Lines 5 (`**Trigger**: /atlas:business:strategy review...`)

**Update** mode selection (lines 7-13) — remove argument parsing:

```markdown
## Mode Selection

Determine the review period from the conversation:
- Weekly review, "this week" → Weekly
- Monthly review, "this month" → Monthly
- Quarterly review, "this quarter", strategic review → Quarterly
- Just "review" with no qualifier → Default to weekly
```

---

### Success Criteria

#### Automated Verification:
- [x] `grep -r '^\*\*Trigger\*\*' skills/` returns zero results
- [x] `grep -r '## No Arguments' skills/` returns zero results
- [x] `grep -r 'Parse arguments' skills/` returns zero results
- [x] `grep -c '/atlas:' skills/marketing_content/workflow/research.md` returns 0 (was 6)
- [x] `grep -c '/atlas:' skills/marketing_content/workflow/plan.md` returns 0 (was 11)
- [x] `grep -c '/atlas:' skills/marketing_content/workflow/write.md` returns 0 (was 8)
- [x] `grep -c '/atlas:' skills/marketing_content/workflow/review.md` returns 0 (was 8)
- [x] `grep -c '/atlas:' skills/marketing_content/workflow/results.md` returns 0 (was 5)
- [x] `grep -c '/atlas:' skills/second_brain_foundation/project/manage.md` returns 0 (was 9)
- [x] `grep -c '/atlas:' skills/second_brain_foundation/project/define.md` returns 0 (was 6)
- [x] `grep -c '/atlas:' skills/business_strategy/workflows/analyze.md` returns 0 (was 2)
- [x] `skills/second_brain_foundation/workflows/help.md` does not exist (deleted)
- [x] Framework table appears only in `business_strategy/SKILL.md`, not in `workflows/analyze.md`
- [x] Channel table appears only in `marketing_content/SKILL.md`, not in `workflow/write.md` or `workflow/plan.md`

#### Manual Verification:
- [ ] Each workflow still has STOP AND WAIT checkpoints preserved
- [ ] Agent orchestration blocks (subagent_type) are unchanged
- [ ] Content folder discovery references SKILL.md pattern
- [ ] Next-step suggestions use natural language, not slash commands
- [ ] Output format templates are preserved

---

## Phase 3: CLAUDE.md Rewrite

### Overview

Transform CLAUDE.md from a command reference manual (25% command tables) into a conversational behavior guide with intent detection, flow awareness, and state detection. Keep all personality/style sections and framework reference tables.

### Changes Required

**File**: `CLAUDE.md` (311 lines -> ~250 lines)

**Keep unchanged (lines 1-54)**: Identity, Communication Style, Collaboration Mode, Critical Thinking, My Expertise Areas — these are the personality core.

**Keep unchanged (lines 57-60)**: Knowledge Base Structure header and PARA Method reference.

**Rewrite "Knowledge Base Structure" tables (lines 62-89)** — remove "Created By" column:

```markdown
## Knowledge Base Structure (PARA Method)

> Follow `second_brain_foundation` skill → `reference/folder-structure.md` for complete structure.

### Project Structure

| Component | Location |
|---|---|
| Context | `context.md` |
| Strategy | `strategy/strategy.md` |
| Competitors | `competitors/{name}.md` |

### Marketing Structure

| Component | Location |
|---|---|
| Themes | `marketing/themes/{theme-slug}.md` |
| Calendars | `marketing/calendars/{year}-Q{n}.md` |
| Brand Voice | `marketing/brand-voice.md` |
| Visual Identity | `marketing/visual-identity.md` |
| Audiences | `marketing/audiences/{name}.md` |
```

(Removes the "Created By" column with 8 slash-command references)

**Keep unchanged (lines 91-110)**: "Working with the Knowledge Base" — capture/recall/organize guidelines.

**Replace "Available Skills" tables (lines 112-167, 56 lines)** with capabilities description:

```markdown
## What I Can Do

### Knowledge & Projects
I manage your personal knowledge base using the PARA method. I can capture ideas, search notes, do deep recall with synthesis, and manage multiple projects. Each project is an isolated silo with its own context, strategy, competitors, brand, and content.

**Key behaviors**:
- When you mention an idea → I offer to capture it to inbox
- When you ask "what do I know about X" → I do deep recall automatically (locate files, analyze content, synthesize)
- When you mention a project name → I check if it exists and offer context

### Content Creation
I manage the full content lifecycle: research → plan → write → review → results. Content is organized topic-first, with research and planning shared across channels (blog, linkedin, twitter, email, hackernews, social).

**Key behaviors**:
- When you say "write a blog post about X" → I check if research exists first, and start there if not
- When you mention a content topic → I check for in-progress work and report status
- Content review is mandatory before publishing — I'll always run it
- I never skip pipeline steps, even if you ask to jump ahead

### Business Strategy
I apply strategic frameworks to help you think through business questions: SWOT, Porter's Five Forces, PESTEL, Business Model Canvas, Blue Ocean, OKRs, and more. I also support periodic reviews (weekly, monthly, quarterly) and structured decision logging.

**Key behaviors**:
- When you ask a strategic question → I select the appropriate framework automatically
- When you need to make a decision → I use the decision framework with options analysis
- When you say "weekly review" → I find this week's activity and guide the reflection

### Visual Content
I help create visual assets: AI image prompts, schema diagrams (HTML+CSS → PNG), and photo processing (crop, background removal, optimization). Visual tools chain together for common workflows like blog hero images.
```

**Keep "Strategic Frameworks" table (lines 170-188)** — this is reference knowledge, not a command table.

**Keep "Marketing Frameworks" table (lines 191-200)** — same reason.

**Rewrite "Proactive Behaviors" section (lines 202-213)** — expand from abstract to actionable:

```markdown
## Proactive Behaviors

1. **Before answering questions** → Search the brain for related knowledge using `locate_knowledge` agent. Present relevant notes.
2. **After learning something new** → Offer to capture it: "Want me to save this to your knowledge base?"
3. **When user mentions a project** → Check if it exists in `{BRAIN_PATH}/projects/`. If found, load its context. If not, offer to create it.
4. **When user expresses content intent** → Determine correct pipeline starting point. Check for in-progress work on the topic first.
5. **When user mentions a content topic with existing work** → Find the content folder, report what stage it's at, and ask where to continue.
6. **When returning to a conversation about a topic** → Check for in-progress work (content folders, strategy docs) before starting fresh.
7. **When user says "save this" or "remember"** → Capture from conversation context to inbox, no further prompting needed.
8. **When user asks "what do I know about X"** → Use recall mode automatically (locate → analyze → synthesize).
9. **When patterns emerge across conversations** → Suggest documenting them as resources.
10. **When discussing campaigns** → Check for past campaign patterns and results to inform strategy.
11. **When making decisions** → Suggest using the decision framework with structured options.
12. **When setting goals** → Offer OKR structure from business strategy skill.
```

**Keep "Response Formats" section (lines 216-272)** unchanged — templates are useful.

**Replace "Project Workflow" section (lines 274-295)** — remove slash commands:

```markdown
## Project Workflow

Projects are isolated silos for different businesses/clients. Folders are created on-demand:

1. Create a project → Creates minimal structure with README.md
2. Set it as active → All subsequent operations target this project
3. Define context → What the project is, audience, differentiator
4. Define strategy → Vision, mission, goals, success metrics
5. Document competitors → Strengths, weaknesses, differentiation
6. Define brand voice → Personality, tone, key messages
7. Define visual identity → Colors, style, mood
8. Define audience personas → Demographics, goals, pain points
9. Add content themes → Topic areas with guidelines
10. Plan quarterly calendar → Phase objectives, scheduled content
11. Research a content topic → Sources, angle, differentiation
12. Plan content → Unified brief with per-channel outlines
13. Write content → Channel-specific draft
14. Review content → Mandatory quality check before publishing
```

**Keep "Content Review" section (lines 297-311)** unchanged.

**Remove the "Content Architecture" comment block (lines 82-89)** — this is now covered by the marketing_content SKILL.md "Content Lifecycle" section.

Actually, keep the Content Architecture block — it's a useful reference about how components relate.

### Success Criteria

#### Automated Verification:
- [x] `grep -c '/atlas:' CLAUDE.md` returns 0 (was 54)
- [x] `grep -c 'argument-hint\|dispatch\|No Arguments\|Show Usage' CLAUDE.md` returns 0
- [x] CLAUDE.md contains "## What I Can Do" section
- [x] CLAUDE.md contains "## Proactive Behaviors" with 12 entries
- [x] No "Created By" column in any table

#### Manual Verification:
- [ ] CLAUDE.md reads as a personality document, not a command manual
- [ ] "What can you do?" can be answered from CLAUDE.md content alone
- [ ] Proactive behaviors describe HOW to do things (which agents to use), not just WHAT to do
- [ ] Project workflow is numbered steps in natural language

---

## Phase 4: Agents + Cleanup

### Overview

Update all 5 agent files to use the new config pattern. Delete orphaned files. Deduplicate the framework selection table from the strategist agent. Update `.env.example` and `README.md`.

### Changes Required

#### 1. All 5 Agent Files — Config Update

For each agent file, replace the hardcoded config line with a reference to the config chain.

**Files**: `agents/core_locate_knowledge.md`, `agents/core_analyze_knowledge.md`, `agents/marketing_market_researcher.md`, `agents/business_strategist.md`, `agents/marketing_content_reviewer.md`

**Current pattern** (varies slightly per agent):
```markdown
## Setup

Read `ATLAS_BRAIN_PATH` from `~/.claude/CLAUDE.md`.
```

**New pattern**:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` (and `ATLAS_ACTIVE_PROJECT` if needed) using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`
```

Specific files and lines:
- `core_locate_knowledge.md:26` — needs `ATLAS_BRAIN_PATH` only
- `core_analyze_knowledge.md:27` — needs `ATLAS_BRAIN_PATH` only
- `marketing_market_researcher.md:16` — needs `ATLAS_BRAIN_PATH` only
- `business_strategist.md:16` — needs `ATLAS_BRAIN_PATH` only
- `marketing_content_reviewer.md:16` — needs both `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT`

---

#### 2. `agents/business_strategist.md` — Deduplicate Framework Table

**File**: `agents/business_strategist.md`

**Remove** the framework selection table (lines 32-46). Replace with a reference:

```markdown
## Framework Selection

Use the Framework Selection Guide from the `business_strategy` skill's SKILL.md. Match the user's question to the appropriate framework.
```

This eliminates the 4th copy of the framework table (the other duplicate in `analyze.md` was already removed in Phase 2).

---

#### 3. Delete `skills/second_brain_foundation/workflows/help.md`

Already specified in Phase 2 but listing here for the cleanup checklist.

---

#### 4. Update `.env.example`

**File**: `.env.example`

**Current content** (5 lines):
```
# Atlas Configuration
# Copy to .env and customize

# Path to your knowledge base (second brain)
ATLAS_BRAIN_PATH=~/brain
```

**New content**:
```
# Atlas Configuration
# Copy to .env and customize values

# Path to your knowledge base (second brain)
ATLAS_BRAIN_PATH=~/brain

# Active project (optional, can be set interactively)
# ATLAS_ACTIVE_PROJECT=my-project
```

---

#### 5. Simplify `README.md`

**File**: `README.md`

**Rewrite the Quick Start section** (lines 14-28) — remove slash commands except for setup (which is the actual entry point):

```markdown
## Quick Start

```bash
# 1. Install the plugin
/install atlas

# 2. Initialize your knowledge base
/atlas:second_brain:foundation setup
```

After setup, Atlas works conversationally:
- "Save this idea: build a habit tracker CLI"
- "Research content about AI trends"
- "Analyze our market position using SWOT"
- "Weekly review"
```

**Rewrite Skills Reference section** (lines 70-116) — replace command tables with capability descriptions:

```markdown
## Capabilities

### Knowledge Management (`second_brain_foundation`)
PARA-based personal knowledge base with 16 operations: capture ideas, search notes, deep recall with synthesis, create and manage projects, define project context/strategy/brand/visuals/audience/competitors.

### Content Creation (`marketing_content`)
Full content lifecycle with 11 operations: research, plan, write, review, results tracking, calendar planning, theme management. Supports 6 channels: blog, linkedin, twitter, email, hackernews, social.

Pipeline: research → plan → write → review → [publish] → results

### Business Strategy (`business_strategy`)
Strategic frameworks with 6 operations: analyze (12 frameworks), document decisions, periodic reviews (weekly/monthly/quarterly).

### Visual Content (`marketing_visuals`)
Internal skill for image processing, schema diagrams, and AI prompt composition.
```

**Keep**: Plugin Structure tree (lines 32-65), Strategic Frameworks table (lines 118-133), Knowledge Base Structure (lines 135-162), Agents table (lines 164-172), Architecture comparison table (lines 186-194), Personality section (lines 196-203).

**Rewrite Configuration section** (lines 174-183):

```markdown
## Configuration

After running `/atlas:second_brain:foundation setup`, your brain path is stored in one of:
- `.env` file in your project (portable)
- `~/.claude/CLAUDE.md` (Claude Code-specific)

```
ATLAS_BRAIN_PATH=~/brain
ATLAS_ACTIVE_PROJECT=my-project
```
```

---

#### 6. Verify `hooks/hooks.json`

**File**: `hooks/hooks.json`

Keep as-is. Empty hooks `{"hooks": {}}` is valid plugin structure.

---

#### 7. Verify `channels/social.md` exists (Issue 12)

**File**: `skills/marketing_content/channels/social.md`

Confirmed: 108 lines with copywriting frameworks, channel best practices, content repurposing matrix, CTA best practices, quality checklist, and frontmatter template. No action needed.

### Success Criteria

#### Automated Verification:
- [x] `grep -r "Read.*ATLAS_BRAIN_PATH.*from.*~/.claude/CLAUDE.md" agents/` returns 0 (old pattern gone)
- [x] `grep -r "Config Chain" agents/` returns 5 (new pattern present in all agents)
- [x] `grep -c '/atlas:' agents/business_strategist.md` returns 0
- [x] `! test -f skills/second_brain_foundation/workflows/help.md` succeeds (file deleted)
- [x] `.env.example` contains both `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT`
- [x] `grep -c '/atlas:' README.md` is <= 2 (only setup command in Quick Start)
- [x] Framework selection table exists only in `skills/business_strategy/SKILL.md` (1 location)

#### Manual Verification:
- [ ] Agents can read config from `.env` file
- [ ] README.md reads as a product overview, not a CLI reference
- [ ] No orphaned file references (help.md links cleaned up)

---

## Testing Strategy

### Verification Script

After all phases, run this comprehensive check:

```bash
#!/bin/bash
# Run from atlas/ root

echo "=== CLI Pattern Removal ==="
echo "argument-hint: $(grep -r 'argument-hint' skills/*/SKILL.md | wc -l) (expect 0)"
echo "Action Dispatch: $(grep -r '## Action Dispatch' skills/ | wc -l) (expect 0)"
echo "No Arguments: $(grep -r '## No Arguments' skills/ | wc -l) (expect 0)"
echo "Parse arguments: $(grep -r 'Parse arguments' skills/ | wc -l) (expect 0)"
echo "Parse the first: $(grep -r 'Parse the first' skills/ | wc -l) (expect 0)"
echo "Trigger lines: $(grep -r '^\*\*Trigger\*\*' skills/ | wc -l) (expect 0)"

echo ""
echo "=== Slash Command References ==="
echo "Total /atlas: in skills/: $(grep -r '/atlas:' skills/ --include='*.md' | grep -v 'SKILL.md:name:' | wc -l) (expect 0)"
echo "Total /atlas: in agents/: $(grep -r '/atlas:' agents/ | wc -l) (expect 0)"
echo "Total /atlas: in CLAUDE.md: $(grep -c '/atlas:' CLAUDE.md) (expect 0)"
echo "Total /atlas: in README.md: $(grep -c '/atlas:' README.md) (expect <=2)"

echo ""
echo "=== Config Pattern ==="
echo "Old config pattern in agents: $(grep -r 'from.*~/.claude/CLAUDE.md' agents/ | grep -v 'Config Chain' | wc -l) (expect 0)"
echo "Old config pattern in skills: $(grep -r 'from.*~/.claude/CLAUDE.md' skills/*/SKILL.md | grep -v 'Config Chain' | wc -l) (expect 0)"

echo ""
echo "=== Deduplication ==="
echo "Framework tables: $(grep -rl 'Porter.*Five Forces' skills/ agents/ | wc -l) (expect 1: SKILL.md only)"
echo "Channel tables in workflows: $(grep -rl 'channels/blog.md' skills/marketing_content/workflow/ | wc -l) (expect 0)"

echo ""
echo "=== Deleted Files ==="
echo "help.md exists: $(test -f skills/second_brain_foundation/workflows/help.md && echo YES || echo NO) (expect NO)"

echo ""
echo "=== New Sections ==="
echo "Capabilities sections: $(grep -rl '## Capabilities\|## Content Lifecycle\|## What I Can Do' skills/*/SKILL.md CLAUDE.md | wc -l) (expect 4)"
echo "Config Chain refs: $(grep -rl 'Config Chain' skills/*/SKILL.md agents/ | wc -l) (expect 7: 2 SKILL.md + 5 agents)"
```

### Manual Testing Checklist

1. [ ] Invoke `/atlas:second_brain:foundation` — skill loads, no crash
2. [ ] Invoke `/atlas:marketing:content` — skill loads, no crash
3. [ ] Invoke `/atlas:business:strategy` — skill loads, no crash
4. [ ] Say "save this idea: test the new conversational model" — capture workflow executes
5. [ ] Say "I want to write a blog post about AI trends" — agent detects content intent, checks for existing work, starts at research if none
6. [ ] Say "what can you do?" — Atlas describes capabilities from CLAUDE.md
7. [ ] Say "what do I know about marketing?" — recall mode activates (locate → analyze → synthesize)
8. [ ] Create `.env` with `ATLAS_BRAIN_PATH=~/test-brain` — config reads from .env
9. [ ] Remove `.env`, have `~/.claude/CLAUDE.md` config — config falls back correctly

## Performance Considerations

- No runtime performance impact — all changes are to markdown instruction files, not code
- Slightly reduced token usage per skill invocation (removed ~30-60 lines of CLI scaffolding per SKILL.md)
- Agent orchestration unchanged — same subagent patterns, same tools

## Migration Notes

- **No data migration needed** — Brain directory structure is unchanged
- **No config migration needed** — `~/.claude/CLAUDE.md` still works, `.env` is additive
- **Slash commands still work** — `user_invocable: true` preserved, so existing muscle memory works
- **Breaking change**: `help` action is removed. Users who type `/atlas:second_brain:foundation help` will get the skill loaded but no help workflow. CLAUDE.md and SKILL.md capabilities sections serve this purpose now.

## Issue Resolution Map

| Issue | Phase | Solution |
|---|---|---|
| 1. Skills behave like CLI commands | Phase 1 | Remove argument-hint, dispatch tables, usage blocks from all SKILL.md |
| 2. Slash-command references everywhere | Phase 2+3 | Replace 237 references with natural language |
| 3. CLAUDE.md is command reference | Phase 3 | Replace command tables with capability descriptions |
| 4. No intent-to-action mapping | Phase 1 | Add Capabilities tables mapping natural language to workflow files |
| 5. No workflow state awareness | Phase 1 | Add State Detection section to marketing_content/SKILL.md |
| 6. Config locked to Claude Code | Phase 1+4 | Config chain: .env → ~/.claude/CLAUDE.md, defined once |
| 7. Massive content duplication | Phase 1+2+4 | Framework table 4→1, channel table 3→1, config 8→1, commands 3→0 |
| 8. Marketing visuals lacks workflow context | Phase 1 | Add Workflow Chaining section to SKILL.md |
| 9. Orphaned/dead files | Phase 4 | Delete help.md, update .env.example |
| 10. Core knowledge actions should be invisible | Phase 1+3 | Invisible Actions in SKILL.md, proactive behaviors in CLAUDE.md |
| 11. Subagent orchestration implicit | Phase 1 | Agent Orchestration section in second_brain_foundation/SKILL.md |
| 12. Missing social channel file | Phase 4 | Verified: exists with 108 lines of content. No action needed. |

## References

- Research document: `thoughts/research/2026-02-13-atlas-vs-jarvis-comparison.md`
- Jarvis consolidation history: 9 planning documents from Jan-Feb 2026 in `../jarvis/thoughts/`
