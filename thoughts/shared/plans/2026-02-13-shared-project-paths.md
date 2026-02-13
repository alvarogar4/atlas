# Shared Project Paths Implementation Plan

## Overview

Add support for projects that live outside the main brain directory. Each external project gets a persistent per-project env var (`ATLAS_PATH_{NAME}`), and all Atlas operations treat them identically to local projects.

## Current State Analysis

`PROJECT_PATH` is always derived as `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}` — hardcoded in the Config Chain (`skills/second_brain_foundation/SKILL.md:39`). All 5 agents and project management workflows use this formula. There is no way to point a project to an external directory.

### Key Discoveries:

- `SKILL.md:39` — defines the hardcoded formula
- `marketing_content_reviewer.md:21` — the only agent with an explicit inline derivation
- Other 4 agents reference the Config Chain indirectly via "Read ... using the Config Chain" instructions
- `manage.md:17-24,67,96` — all CRUD operations assume `{BRAIN_PATH}/projects/`
- `core_locate_knowledge.md:107-109` — scope table uses `${ATLAS_BRAIN_PATH}/` and `${PROJECT_PATH}/`
- `marketing_content/SKILL.md:54` — content folder discovery uses `${PROJECT_PATH}/marketing/content/`
- ~20+ downstream files consume `{PROJECT_PATH}` without deriving it — they work automatically once resolution is correct

## Desired End State

Atlas supports per-project external paths via persistent env vars:

```env
# .env
ATLAS_BRAIN_PATH=/Users/alvaro/brain
ATLAS_ACTIVE_PROJECT=obsessiondb

# Per-project external paths (persistent, one per project)
ATLAS_PATH_OBSESSIONDB=/path/to/obsessiondb-project
ATLAS_PATH_GYMBROS=/path/to/gymbros-project
```

**Resolution logic:**
1. Get `ATLAS_ACTIVE_PROJECT` (e.g., `obsessiondb`)
2. Convert to uppercase, replace `-` with `_` → `OBSESSIONDB`
3. Look for `ATLAS_PATH_OBSESSIONDB` in config chain
4. If found → `PROJECT_PATH = /path/to/obsessiondb-project`
5. Otherwise → `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}` (current behavior)

**Invariants:**
- PARA root (inbox, areas, resources, archives) always uses `ATLAS_BRAIN_PATH`
- External paths point to the project directory (contains context.md, strategy/, marketing/)
- Per-project vars persist in `.env`/`CLAUDE.md` until explicitly removed
- External projects appear in project-list alongside local ones
- Brain-wide searches include all registered external project paths

**Verification:**
- Setting `ATLAS_ACTIVE_PROJECT=obsessiondb` with `ATLAS_PATH_OBSESSIONDB=/some/path` → `PROJECT_PATH = /some/path`
- Setting `ATLAS_ACTIVE_PROJECT=personal-brand` (no ATLAS_PATH_PERSONAL_BRAND) → `PROJECT_PATH = {BRAIN_PATH}/projects/personal-brand`
- `project-list` shows both local projects from `{BRAIN_PATH}/projects/` and all `ATLAS_PATH_*` entries
- `project-link obsessiondb /some/path` → adds `ATLAS_PATH_OBSESSIONDB=/some/path` to `.env` and `~/.claude/CLAUDE.md`
- Switching from `obsessiondb` to `personal-brand` does NOT remove `ATLAS_PATH_OBSESSIONDB`
- `locate_knowledge` brain-scope search checks `ATLAS_BRAIN_PATH` + all `ATLAS_PATH_*` directories

## What We're NOT Doing

- No registry file (`.context/linked-projects.json`) — env vars are the registry
- No separate brain roots — external paths are project directories, not full PARA brains
- No auto-cleanup of `ATLAS_PATH_*` when switching projects — they persist
- No changes to downstream files that consume `{PROJECT_PATH}` (channels, workflows, themes, etc.)

## Implementation Approach

Bottom-up: update the config chain definition first (source of truth), then update all consumers (agents, project management), then documentation. This ensures the resolution logic is defined once and referenced everywhere.

## Phase 1: Config Chain — Source of Truth

### Overview

Update the Config Chain in `SKILL.md` to define per-project path resolution. This is the single source of truth that all agents and skills reference.

### Changes Required:

#### 1. `skills/second_brain_foundation/SKILL.md`

**Lines 14-21 — Config Chain**: Add `ATLAS_PATH_*` to the config chain parsing.

Current:
```
1. **Conversation context**: Check current `system-reminder` for `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT` already loaded from CLAUDE.md
2. **`.env` file**: Read `.env` in the current working directory (or repo root)
3. **`~/.claude/CLAUDE.md`**: Parse for `ATLAS_BRAIN_PATH=` and `ATLAS_ACTIVE_PROJECT=`
4. **Error**: "Brain not configured. Let's set it up — where should I store your knowledge base?"
```

New:
```
1. **Conversation context**: Check current `system-reminder` for `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values already loaded from CLAUDE.md
2. **`.env` file**: Read `.env` in the current working directory (or repo root)
3. **`~/.claude/CLAUDE.md`**: Parse for `ATLAS_BRAIN_PATH=`, `ATLAS_ACTIVE_PROJECT=`, and `ATLAS_PATH_*=` entries
4. **Error**: "Brain not configured. Let's set it up — where should I store your knowledge base?"
```

**Lines 25-29 — Reading `.env`**: Add comment about `ATLAS_PATH_*` vars.

Current:
```bash
# Source .env if it exists (supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT)
```

New:
```bash
# Source .env if it exists (supports ATLAS_BRAIN_PATH, ATLAS_ACTIVE_PROJECT, ATLAS_PATH_*)
```

**Lines 37-40 — Project Config Level**: Update to include per-project path resolution.

Current:
```
**Project** (active project context):
- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
- If no active project: list available projects, ask user to choose
```

New:
```
**Project** (active project context):
- Required: `ATLAS_BRAIN_PATH` + `ATLAS_ACTIVE_PROJECT`
- Optional: `ATLAS_PATH_{NAME}` entries (per-project external paths)
- Provides: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`
- `PROJECT_PATH` resolution:
  1. Convert `ACTIVE_PROJECT` to uppercase, replace `-` with `_` → `{NAME}`
  2. If `ATLAS_PATH_{NAME}` is set → `PROJECT_PATH = that value`
  3. Otherwise → `PROJECT_PATH = {BRAIN_PATH}/projects/{ACTIVE_PROJECT}`
- If no active project: list available projects, ask user to choose
```

#### 2. `.env.example`

Current:
```env
# Atlas Configuration
# Copy to .env and customize values

# Path to your knowledge base (second brain)
ATLAS_BRAIN_PATH=~/brain

# Active project
ATLAS_ACTIVE_PROJECT=my-project
```

New:
```env
# Atlas Configuration
# Copy to .env and customize values

# Path to your knowledge base (second brain)
ATLAS_BRAIN_PATH=~/brain

# Active project
ATLAS_ACTIVE_PROJECT=my-project

# Per-project external paths (optional)
# Format: ATLAS_PATH_{PROJECT_NAME_UPPERCASE}
# Use for projects that live outside {BRAIN_PATH}/projects/
# ATLAS_PATH_MYPROJECT=/path/to/external/project
```

### Success Criteria:

#### Automated Verification:

- [x] `.env.example` contains `ATLAS_PATH_` documentation
- [x] `SKILL.md` contains the 3-step `PROJECT_PATH` resolution logic
- [x] `SKILL.md` Config Chain mentions `ATLAS_PATH_*` in all 3 source steps

#### Manual Verification:

- [x] Config Chain section is clear and unambiguous — a new reader can understand the resolution order

---

## Phase 2: Agent Config Blocks

### Overview

Update all 5 agents to parse `ATLAS_PATH_*` variables and resolve `PROJECT_PATH` using the new logic.

### Changes Required:

#### 1. `agents/marketing_content_reviewer.md`

**Lines 16-21 — Config block**: This is the only agent with an explicit inline derivation.

Current:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` and `ATLAS_ACTIVE_PROJECT` using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Derive `PROJECT_PATH = ${ATLAS_BRAIN_PATH}/projects/${ATLAS_ACTIVE_PROJECT}`.
```

New:
```markdown
## Config

Read `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Derive `PROJECT_PATH` using the Config Chain resolution:
1. Convert `ACTIVE_PROJECT` to uppercase, replace `-` with `_` → `{NAME}`
2. If `ATLAS_PATH_{NAME}` is set → use it as `PROJECT_PATH`
3. Otherwise → `PROJECT_PATH = ${ATLAS_BRAIN_PATH}/projects/${ATLAS_ACTIVE_PROJECT}`
```

#### 2. `agents/core_locate_knowledge.md`

**Lines 26-29 — Config block**:

Current:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` (and `ATLAS_ACTIVE_PROJECT` if needed) using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`
```

New:
```markdown
## Config

Read `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Resolve `PROJECT_PATH` per the Config Chain (check `ATLAS_PATH_{NAME}` first, then default to `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`).
```

**Lines 105-109 — Scope Configuration table**: Add note about external project paths.

Current:
```markdown
| Scope             | Path                         | Use Case                          |
| ----------------- | ---------------------------- | --------------------------------- |
| `brain` (default) | `${ATLAS_BRAIN_PATH}/`      | Full recall, cross-project search |
| `project`         | `${PROJECT_PATH}/`           | Project-specific search           |
| `marketing`       | `${PROJECT_PATH}/marketing/` | Campaigns, blog, calendar         |
```

New:
```markdown
| Scope             | Path                                                          | Use Case                          |
| ----------------- | ------------------------------------------------------------- | --------------------------------- |
| `brain` (default) | `${ATLAS_BRAIN_PATH}/` + all `ATLAS_PATH_*` project dirs     | Full recall, cross-project search |
| `project`         | `${PROJECT_PATH}/`                                            | Project-specific search           |
| `marketing`       | `${PROJECT_PATH}/marketing/`                                  | Campaigns, blog, calendar         |
```

**After "Scope Detection" section (~line 119)**: Add a note about brain scope including external projects.

Add:
```markdown
### Brain Scope with External Projects

When searching in `brain` scope, include ALL known project paths:
1. Search `${ATLAS_BRAIN_PATH}/` (covers inbox, areas, resources, archives, and local projects)
2. For each `ATLAS_PATH_*` variable found in config → also search that directory

This ensures external projects are discoverable in brain-wide searches.
```

#### 3. `agents/core_analyze_knowledge.md`

**Lines 27-30 — Config block**:

Current:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` (and `ATLAS_ACTIVE_PROJECT` if needed) using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`
```

New:
```markdown
## Config

Read `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Resolve `PROJECT_PATH` per the Config Chain (check `ATLAS_PATH_{NAME}` first, then default to `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`).
```

#### 4. `agents/marketing_market_researcher.md`

**Lines 16-19 — Config block**: Same pattern as analyze_knowledge.

Current:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` (and `ATLAS_ACTIVE_PROJECT` if needed) using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`
```

New:
```markdown
## Config

Read `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Resolve `PROJECT_PATH` per the Config Chain (check `ATLAS_PATH_{NAME}` first, then default to `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`).
```

#### 5. `agents/business_strategist.md`

**Lines 16-19 — Config block**: Same pattern.

Current:
```markdown
## Config

Read `ATLAS_BRAIN_PATH` (and `ATLAS_ACTIVE_PROJECT` if needed) using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`
```

New:
```markdown
## Config

Read `ATLAS_BRAIN_PATH`, `ATLAS_ACTIVE_PROJECT`, and any `ATLAS_PATH_*` values using the Config Chain:
1. Check conversation context for values already loaded
2. Check `.env` in working directory
3. Check `~/.claude/CLAUDE.md`

Resolve `PROJECT_PATH` per the Config Chain (check `ATLAS_PATH_{NAME}` first, then default to `{BRAIN_PATH}/projects/{ACTIVE_PROJECT}`).
```

### Success Criteria:

#### Automated Verification:

- [x] All 5 agent files contain `ATLAS_PATH_*` in their Config block
- [x] `marketing_content_reviewer.md` no longer has the hardcoded derivation formula
- [x] `core_locate_knowledge.md` scope table references external project dirs for brain scope

#### Manual Verification:

- [x] Each agent's config block is consistent with the others
- [x] locate_knowledge brain-scope search instructions are clear about including external paths

---

## Phase 3: Project Management

### Overview

Update `manage.md` with a new `project-link` action, and modify `project-list` and `project-use` to handle external projects.

### Changes Required:

#### 1. `skills/second_brain_foundation/project/manage.md`

**Add new action — `project-link`** (after `project-create`, before `project-list`):

```markdown
---

## Action: project-link

Link an external project directory so Atlas treats it like a local project.

### Setup
Execute **Basic Setup** from SKILL.md.

### Arguments
- `{name}` — project name (kebab-case)
- `{path}` — absolute path to the external project directory

### Validation
1. Project name must be kebab-case
2. Path must exist and be a directory
3. Path should contain at least a `README.md` or `context.md` (warn if not, but proceed)

### Process

1. Validate the path exists:
   ```bash
   # If path doesn't exist → error: "Directory not found: {path}"
   ls -d {path}
   ```

2. Convert project name to env var format:
   - Uppercase the name
   - Replace `-` with `_`
   - Result: `ATLAS_PATH_{NAME}`

3. Add to `.env`:
   - If `ATLAS_PATH_{NAME}=` exists, update the value
   - Otherwise, append `ATLAS_PATH_{NAME}={path}`

4. Add to `~/.claude/CLAUDE.md`:
   - If `ATLAS_PATH_{NAME}=` exists, update the value
   - Otherwise, add `ATLAS_PATH_{NAME}={path}` after other `ATLAS_` variables

5. Set as active project — update `ATLAS_ACTIVE_PROJECT={name}` in both locations

6. Output:

```
Linked external project: {name}
Path: {path}
Variable: ATLAS_PATH_{NAME}={path}

Active project set to: {name}

This project will be available in project-list and works like any other project.
To unlink: tell me to unlink the project.
```

---

## Action: project-unlink

Remove the link to an external project. Does NOT delete any files.

### Setup
Execute **Basic Setup** from SKILL.md.

### Arguments
- `{name}` — project name to unlink

### Process

1. Convert name to env var: `ATLAS_PATH_{NAME}`
2. Remove `ATLAS_PATH_{NAME}=` from `.env`
3. Remove `ATLAS_PATH_{NAME}=` from `~/.claude/CLAUDE.md`
4. If this was the active project, clear `ATLAS_ACTIVE_PROJECT`

5. Output:

```
Unlinked project: {name}
Removed: ATLAS_PATH_{NAME}

No files were deleted. The project directory still exists at its original location.
```
```

**Update `project-list` action** (current lines 59-86):

Current process step 2:
```
2. List all directories in `{BRAIN_PATH}/projects/`
```

New process:
```
2. List all directories in `{BRAIN_PATH}/projects/` (local projects)
3. Scan config (.env and ~/.claude/CLAUDE.md) for all `ATLAS_PATH_*` variables (external projects)
4. Merge into a single list. For each project:
   - If it has an `ATLAS_PATH_*` entry → show as external with path
   - Otherwise → show as local
```

Current output format:
```
Projects in {BRAIN_PATH}/projects/:

  * active-project
    - Content topics: 8
    ...
```

New output format:
```
Projects:

  * active-project
    - Content topics: 8
    - Drafts: blog (3), linkedin (5), twitter (2)
    - Last activity: 2025-12-20

    another-project
    - Content topics: 0
    - Last activity: 2025-12-15

    obsessiondb (external: /path/to/obsessiondb)
    - Content topics: 3
    - Drafts: blog (1)
    - Last activity: 2025-12-18

To switch projects, just tell me which one to use.
```

**Update `project-use` action** (current lines 90-111):

Current validation:
```
Verify project exists in `{BRAIN_PATH}/projects/`. If not, list available projects.
```

New validation:
```
Verify project exists:
1. Check `{BRAIN_PATH}/projects/{name}` (local)
2. Check for `ATLAS_PATH_{NAME}` variable (external)
3. If neither found → list available projects (both local and external)
```

### Success Criteria:

#### Automated Verification:

- [x] `manage.md` contains `project-link` action
- [x] `manage.md` contains `project-unlink` action
- [x] `project-list` references both local and `ATLAS_PATH_*` projects
- [x] `project-use` validation checks both local and external

#### Manual Verification:

- [x] `project-link obsessiondb /some/path` → adds env var, sets active project
- [x] `project-list` shows both local and external projects with correct labels
- [x] `project-use obsessiondb` works for an external project
- [x] `project-use personal-brand` works for a local project (no disruption)
- [x] `project-unlink obsessiondb` → removes env var only, no file deletion

---

## Phase 4: Documentation

### Overview

Update CLAUDE.md, AGENTS.md, .env.example (done in Phase 1), and folder-structure reference.

### Changes Required:

#### 1. `CLAUDE.md`

**Line 14 — Knowledge Base Location**: Add mention of per-project paths.

Current:
```
**Knowledge Base Location**: Configured via setup → stored in `.env` or `~/.claude/CLAUDE.md` as `ATLAS_BRAIN_PATH`
```

New:
```
**Knowledge Base Location**: Configured via setup → stored in `.env` or `~/.claude/CLAUDE.md` as `ATLAS_BRAIN_PATH`

**External Project Paths**: Per-project `ATLAS_PATH_{NAME}` variables in `.env` or `~/.claude/CLAUDE.md`
```

**Line 182 — Proactive behavior #3**: Update project check to include external projects.

Current:
```
3. **When user mentions a project** → Check if it exists in `{BRAIN_PATH}/projects/`. If found, load its context. If not, offer to create it.
```

New:
```
3. **When user mentions a project** → Check if it exists in `{BRAIN_PATH}/projects/` or has an `ATLAS_PATH_*` variable. If found, load its context. If not, offer to create or link it.
```

#### 2. `AGENTS.md`

Mirror the same changes from CLAUDE.md (AGENTS.md is a copy of CLAUDE.md per its header comment).

#### 3. `skills/second_brain_foundation/reference/folder-structure.md`

**After "Brain Root" section (~line 31)**: Add note about external projects.

Add:
```markdown
## External Projects

Projects can also live outside the brain via per-project path variables:

```env
# In .env or ~/.claude/CLAUDE.md
ATLAS_PATH_OBSESSIONDB=/path/to/obsessiondb
ATLAS_PATH_GYMBROS=/path/to/gymbros
```

External project directories follow the same structure as `projects/{project-name}/`:

```
/path/to/external-project/
├── README.md
├── context.md
├── strategy/
├── competitors/
└── marketing/
    ├── content/
    ├── calendars/
    ├── audiences/
    ├── themes/
    ├── brand-voice.md
    └── visual-identity.md
```

**Brain-level PARA** (inbox, areas, resources, archives) always uses `ATLAS_BRAIN_PATH`, regardless of which project is active.
```

### Success Criteria:

#### Automated Verification:

- [x] `CLAUDE.md` mentions `ATLAS_PATH_*` in identity section
- [x] `CLAUDE.md` proactive behavior #3 includes external project check
- [x] `AGENTS.md` mirrors CLAUDE.md changes
- [x] `folder-structure.md` has "External Projects" section

#### Manual Verification:

- [x] Documentation is clear for a new user setting up an external project
- [x] No contradictions between CLAUDE.md, AGENTS.md, SKILL.md, and folder-structure.md

---

## Testing Strategy

### Manual Testing Steps:

1. Add `ATLAS_PATH_OBSESSIONDB=/some/test/path` to `.env`
2. Set `ATLAS_ACTIVE_PROJECT=obsessiondb`
3. Verify Atlas resolves `PROJECT_PATH` to `/some/test/path`
4. Switch to `ATLAS_ACTIVE_PROJECT=personal-brand`
5. Verify `PROJECT_PATH` resolves to `{BRAIN_PATH}/projects/personal-brand`
6. Verify `ATLAS_PATH_OBSESSIONDB` is still in `.env` (not removed)
7. Run `project-list` — verify both local and external projects appear
8. Run `project-link gymbros /another/path` — verify env var is added
9. Run `project-unlink gymbros` — verify env var is removed, files untouched
10. Run brain-wide search — verify results include content from external project paths

## Performance Considerations

None. The only additional work is scanning for `ATLAS_PATH_*` variables during config parsing, which is negligible since there are typically 1-3 external projects at most.

## Summary of All Files

| Phase | File | Change |
|-------|------|--------|
| **P1** | `skills/second_brain_foundation/SKILL.md` | Add per-project path resolution to Config Chain |
| **P1** | `.env.example` | Add `ATLAS_PATH_*` documentation |
| **P2** | `agents/marketing_content_reviewer.md` | Replace hardcoded derivation with Config Chain resolution |
| **P2** | `agents/core_locate_knowledge.md` | Add config reading + external project brain-scope search |
| **P2** | `agents/core_analyze_knowledge.md` | Add config reading + resolution line |
| **P2** | `agents/marketing_market_researcher.md` | Add config reading + resolution line |
| **P2** | `agents/business_strategist.md` | Add config reading + resolution line |
| **P3** | `skills/second_brain_foundation/project/manage.md` | Add project-link/unlink, update list/use |
| **P4** | `CLAUDE.md` | Add external path docs, update proactive behavior |
| **P4** | `AGENTS.md` | Mirror CLAUDE.md changes |
| **P4** | `skills/second_brain_foundation/reference/folder-structure.md` | Add "External Projects" section |

**Total files to modify**: 11
**Files that work automatically**: ~20+ (all consumers of `{PROJECT_PATH}`)

## References

- Research: `thoughts/shared/research/2026-02-13-shared-project-paths.md`
