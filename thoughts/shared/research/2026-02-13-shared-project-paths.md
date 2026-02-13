---
date: 2026-02-13T12:22:48Z
researcher: atlas
git_commit: 78c8fa9a9911c8bcd5562d7cf551267c64892ed9
branch: main
repository: atlas
topic: "Support shared project paths outside main brain"
tags: [research, codebase, config, projects, shared-paths]
status: complete
last_updated: 2026-02-13
last_updated_by: atlas
---

# Research: Support Shared Project Paths Outside Main Brain

**Date**: 2026-02-13T12:22:48Z
**Researcher**: atlas
**Git Commit**: 78c8fa9
**Branch**: main
**Repository**: atlas

## Research Question

Atlas needs to support projects that live outside the main brain path (e.g., in a shared repo), so that `PROJECT_PATH` is not always derived as `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`.

## Summary

Currently, `PROJECT_PATH` is **always** derived as `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}` — hardcoded in the Config Chain (`SKILL.md:39`). Every agent and workflow uses this formula. To support shared/external projects, we need to introduce an optional `ATLAS_PROJECT_PATH` override that, when set, replaces the derived path.

The change touches **3 layers**: config chain definition, all 5 agents, and project management workflows.

## Current Architecture

### Config Chain (source of truth: `skills/second_brain_foundation/SKILL.md:14-47`)

```
ATLAS_BRAIN_PATH + ATLAS_ACTIVE_PROJECT
        ↓
PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}   ← always this formula
        ↓
BRAND_VOICE = {PROJECT_PATH}/marketing/brand-voice.md
VISUAL_IDENTITY = {PROJECT_PATH}/marketing/visual-identity.md
```

### Where PROJECT_PATH derivation is defined/used

| File | Lines | What it does |
|------|-------|-------------|
| `skills/second_brain_foundation/SKILL.md` | 39 | **Defines** the formula: `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}` |
| `agents/marketing_content_reviewer.md` | 21 | **Derives** `PROJECT_PATH = ${ATLAS_BRAIN_PATH}/projects/${ATLAS_ACTIVE_PROJECT}` |
| `agents/core_locate_knowledge.md` | 107-109 | **Uses** `${ATLAS_BRAIN_PATH}/` and `${PROJECT_PATH}/` in scope table |
| `agents/core_analyze_knowledge.md` | 27-30 | Reads config chain, uses PROJECT_PATH |
| `agents/business_strategist.md` | 16-19 | Reads config chain, uses PROJECT_PATH |
| `agents/marketing_market_researcher.md` | 16-19 | Reads config chain, uses PROJECT_PATH |
| `skills/second_brain_foundation/project/manage.md` | 19,24,67,96 | Creates/lists/validates in `{BRAIN_PATH}/projects/` |
| `skills/second_brain_foundation/reference/folder-structure.md` | 10,35,78-86 | Documents structure under `projects/{name}/` |
| `skills/marketing_content/SKILL.md` | 54 | Discovers content folder under `${PROJECT_PATH}/marketing/content/` |
| `CLAUDE.md` | 182 | Proactive check: `{BRAIN_PATH}/projects/` |

## Proposed Solution: `ATLAS_PROJECT_PATH` Override

### New config variable

Add an **optional** `ATLAS_PROJECT_PATH` env var. When set, it overrides the derived `PROJECT_PATH`:

```
If ATLAS_PROJECT_PATH is set → PROJECT_PATH = ATLAS_PROJECT_PATH
Else → PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}  (current behavior)
```

### Changes Required

#### 1. Config Chain — `skills/second_brain_foundation/SKILL.md`

**Lines 37-39**: Update the Project config level to support the override.

Current:
```
**Project** (active project context):
- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
```

New:
```
**Project** (active project context):
- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Optional: `ATLAS_PROJECT_PATH` (overrides default project location)
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`
- `PROJECT_PATH` resolution:
  1. If `ATLAS_PROJECT_PATH` is set → use it directly
  2. Otherwise → `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
```

**Lines 18-20**: Add `ATLAS_PROJECT_PATH` to the config chain parsing:
- Step 1: Check conversation context for `ATLAS_PROJECT_PATH`
- Step 2: Check `.env` for `ATLAS_PROJECT_PATH`
- Step 3: Check `~/.claude/CLAUDE.md` for `ATLAS_PROJECT_PATH=`

#### 2. All 5 Agents — Config blocks

Each agent has a config block that references the Config Chain. They need to also parse `ATLAS_PROJECT_PATH`:

| Agent file | Lines to update |
|-----------|----------------|
| `agents/core_locate_knowledge.md` | 26-29 (add ATLAS_PROJECT_PATH to config reading) |
| `agents/core_analyze_knowledge.md` | 27-30 |
| `agents/marketing_market_researcher.md` | 16-19 |
| `agents/marketing_content_reviewer.md` | 16-21 (update derivation formula) |
| `agents/business_strategist.md` | 16-19 |

The `marketing_content_reviewer.md` is the most explicit — line 21 says:
```
Derive `PROJECT_PATH = ${ATLAS_BRAIN_PATH}/projects/${ATLAS_ACTIVE_PROJECT}`.
```
This needs to become:
```
Derive `PROJECT_PATH`:
- If `ATLAS_PROJECT_PATH` is set → use it directly
- Otherwise → `${ATLAS_BRAIN_PATH}/projects/${ATLAS_ACTIVE_PROJECT}`
```

#### 3. Project Management — `skills/second_brain_foundation/project/manage.md`

**project-create** (lines 17-24): Currently creates projects at `{BRAIN_PATH}/projects/{name}`. For shared projects, this doesn't apply — the directory already exists externally. Options:
- Add a "link external project" action that sets `ATLAS_PROJECT_PATH` without creating directories
- Or: keep create as-is for local projects, add new action for external ones

**project-list** (line 67): Currently lists `{BRAIN_PATH}/projects/`. Shared projects won't appear there. Need to also list any configured `ATLAS_PROJECT_PATH` projects.

**project-use** (lines 96-102): Currently only verifies in `{BRAIN_PATH}/projects/`. Need to also accept switching to a shared project by setting `ATLAS_PROJECT_PATH`.

#### 4. `.env` and `.env.example`

Add optional `ATLAS_PROJECT_PATH`:

```env
# Optional: Override project path (for shared/external projects)
# ATLAS_PROJECT_PATH=/path/to/shared/project
```

#### 5. `CLAUDE.md` — Documentation

**Line 11**: Add mention of `ATLAS_PROJECT_PATH`
**Line 182**: Update proactive behavior to also check `ATLAS_PROJECT_PATH`

#### 6. `AGENTS.md` — Mirror CLAUDE.md changes

Same updates as CLAUDE.md.

#### 7. Folder Structure Reference — `reference/folder-structure.md`

Add a note that projects can also live externally when `ATLAS_PROJECT_PATH` is configured.

### Files That Do NOT Need Changes

These files use `{PROJECT_PATH}` as a resolved variable (not the derivation formula), so they work automatically once the resolution is correct:

- All channel files (`skills/marketing_content/channels/*.md`)
- All workflow files (`skills/marketing_content/workflow/*.md`)
- Calendar files (`skills/marketing_content/calendar/*.md`)
- Theme management (`skills/marketing_content/themes/manage.md`)
- Project definition (`skills/second_brain_foundation/project/define.md`)
- Marketing visuals (`skills/marketing_visuals/`)
- Business strategy workflows (`skills/business_strategy/workflows/*.md`)
- Business strategy SKILL.md

These all consume `{PROJECT_PATH}` — they don't derive it. Once the config chain resolves it correctly, they work with any path.

## Summary of Changes

| Priority | File | Change |
|----------|------|--------|
| **P0** | `skills/second_brain_foundation/SKILL.md` | Update Config Chain to support `ATLAS_PROJECT_PATH` override |
| **P0** | `.env.example` | Add optional `ATLAS_PROJECT_PATH` |
| **P1** | `agents/marketing_content_reviewer.md` | Update explicit derivation formula |
| **P1** | `agents/core_locate_knowledge.md` | Add `ATLAS_PROJECT_PATH` to config reading |
| **P1** | `agents/core_analyze_knowledge.md` | Add `ATLAS_PROJECT_PATH` to config reading |
| **P1** | `agents/marketing_market_researcher.md` | Add `ATLAS_PROJECT_PATH` to config reading |
| **P1** | `agents/business_strategist.md` | Add `ATLAS_PROJECT_PATH` to config reading |
| **P2** | `skills/second_brain_foundation/project/manage.md` | Add "link external project" action, update list/use |
| **P2** | `CLAUDE.md` | Document new variable, update proactive behaviors |
| **P2** | `AGENTS.md` | Mirror CLAUDE.md changes |
| **P3** | `skills/second_brain_foundation/reference/folder-structure.md` | Add note about external projects |
| **P3** | `README.md` | Update configuration docs |

**Total files to modify**: 12
**Files that work automatically**: ~20+ (all consumers of `{PROJECT_PATH}`)
