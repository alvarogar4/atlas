# Entity: Project

## Purpose

Projects are isolated silos for different businesses or clients. Each project contains its own context, strategy, competitors, brand, and content. Projects can be local (inside the brain) or external (linked via path variables).

## Storage

- **Local path**: `{BRAIN_PATH}/projects/{name}/` — one directory per project
- **External path**: Configured via `ATLAS_PATH_{NAME}` in `.env`
- **Type**: Collection (multiple per brain)
- **Name rule**: kebab-case (lowercase, hyphens, numbers only)

## Template

Use the Project README template from `templates/readme.md` when creating.

## Management

- **Create**: Validate name is kebab-case. Check project doesn't already exist. Create directory and README.md using template. Set as active project in `.env`.
- **Link**: Link an external project directory. Validate path exists. Add `ATLAS_PATH_{NAME}={path}` to `.env`. Set as active.
- **Unlink**: Remove `ATLAS_PATH_{NAME}` from `.env`. Does NOT delete any files. Clear active project if it was the unlinked one.
- **List**: Merge local projects (`{BRAIN_PATH}/projects/`) and external projects (`ATLAS_PATH_*` in `.env`). Show content stats and active indicator.
- **Use**: Switch active project. Validate project exists (local or external). Update `ATLAS_ACTIVE_PROJECT` in `.env`.
- **Info**: Show project overview, context summary, content stats, and recent activity.

## Create Flow

### Setup

Execute **Basic** config from SKILL.md.

### Process

1. Check project doesn't already exist:

   ```bash
   # If {BRAIN_PATH}/projects/{name} exists → error
   ```

2. Create minimal structure:

   ```bash
   mkdir -p {BRAIN_PATH}/projects/{name}
   ```

3. Generate README.md using template from `templates/readme.md`.

4. Set as active project — update `.env`:
   - If `ATLAS_ACTIVE_PROJECT=` exists, update it
   - Otherwise, add `ATLAS_ACTIVE_PROJECT={name}` after `ATLAS_BRAIN_PATH`

5. Output:

```
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

## Link Flow

### Setup

Execute **Basic** config from SKILL.md.

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

4. Set as active project — update `ATLAS_ACTIVE_PROJECT={name}` in `.env`

5. Output:

```
Linked external project: {name}
Path: {path}
Variable: ATLAS_PATH_{NAME}={path}

Active project set to: {name}

This project will be available in project-list and works like any other project.
To unlink: tell me to unlink the project.
```

## Unlink Flow

Remove the link to an external project. Does NOT delete any files.

### Setup

Execute **Basic** config from SKILL.md.

### Process

1. Convert name to env var: `ATLAS_PATH_{NAME}`
2. Remove `ATLAS_PATH_{NAME}=` from `.env`
3. If this was the active project, clear `ATLAS_ACTIVE_PROJECT`

4. Output:

```
Unlinked project: {name}
Removed: ATLAS_PATH_{NAME}

No files were deleted. The project directory still exists at its original location.
```

## List Flow

### Setup

Execute **Basic** config from SKILL.md.

### Process

1. Read active project from `.env` → `ATLAS_ACTIVE_PROJECT`
2. List all directories in `{BRAIN_PATH}/projects/` (local projects)
3. Scan `.env` for all `ATLAS_PATH_*` variables (external projects)
4. Merge into a single list. For each project:
   - If it has an `ATLAS_PATH_*` entry → show as external with path
   - Otherwise → show as local
5. For each project, count content topics and drafts by channel
6. Display with active indicator (\*)

### Output

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

## Use Flow

### Setup

Execute **Basic** config from SKILL.md.

### Validation

Verify project exists:

1. Check `{BRAIN_PATH}/projects/{name}` (local)
2. Check for `ATLAS_PATH_{NAME}` variable (external)
3. If neither found → list available projects (both local and external)

### Process

1. Update `.env`:
   - If `ATLAS_ACTIVE_PROJECT=` exists, update the value
   - Otherwise, add `ATLAS_ACTIVE_PROJECT={name}` after `ATLAS_BRAIN_PATH`

2. Output:

```
Active project: {name}

Commands now use this project by default.
```

## Info Flow

### Setup

Execute **Basic** config from SKILL.md.

### Arguments

`[name]` is optional — uses active project if not provided.

### Process

1. Determine project (argument or active)
2. Read README.md
3. Read context.md if exists
4. Count content (topics, drafts by channel, audiences, competitors)
5. Show recent activity (last 5 modified files)

### Output

```
# Project: {name}

## Overview
[From README.md]

## Context
[From context.md or "Not defined yet — want to set up the project context?"]

## Stats
- Content topics: X
- Drafts: blog (Y), linkedin (Z)
- Audiences: X
- Competitors: X

## Recent Activity
- [timestamp] Created blog draft: topic
- [timestamp] Updated strategy
```

## Integration

- **Foundations** (`foundations/`): After creating a project, foundations define its context, strategy, brand voice, and visual identity
- **Entities**: Themes, competitors, audiences, and calendars are scoped to the active project
- **Content workflows**: All content operations target the active project's `marketing/content/` directory
