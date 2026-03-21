# Entity: Project

## Purpose

Projects are isolated silos for different businesses or clients. Each project contains its own context, strategy, competitors, brand, and content. All projects live inside the brain under `projects/`. Projects that need their own git history can have a separate repo inside their folder (gitignored from the main brain repo).

## Storage

- **Path**: `{BRAIN_PATH}/projects/{name}/` — one directory per project
- **Type**: Collection (multiple per brain)
- **Name rule**: kebab-case (lowercase, hyphens, numbers only)

## Template

Use the Project README template from `templates/readme.md` when creating.

## Management

- **Create**: Validate name is kebab-case. Check project doesn't already exist. Create directory and README.md using template. Set as active project in `.env`.
- **List**: List all projects in `{BRAIN_PATH}/projects/`. Show content stats and active indicator.
- **Use**: Switch active project. Validate project exists. Update `ATLAS_ACTIVE_PROJECT` in `.env`.
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

4. Generate `dashboard.base` using the Default Project Dashboard Template from `reference/obsidian-bases.md`. This provides an Obsidian Bases view with Recent Activity, Content Pipeline, and Strategy & Competitors tabs.

5. Set as active project — update `.env`:
   - If `ATLAS_ACTIVE_PROJECT=` exists, update it
   - Otherwise, add `ATLAS_ACTIVE_PROJECT={name}` after `ATLAS_BRAIN_PATH`

6. Output:

```
Project created: {name}

Structure:
  projects/{name}/
  ├── README.md
  └── dashboard.base

Folders are created on-demand as you define each aspect.
Open dashboard.base in Obsidian for a live project overview.

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

## List Flow

### Setup

Execute **Basic** config from SKILL.md.

### Process

1. Read active project from `.env` → `ATLAS_ACTIVE_PROJECT`
2. List all directories in `{BRAIN_PATH}/projects/`
3. For each project, count content topics and drafts by channel
4. Display with active indicator (\*)

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

To switch projects, just tell me which one to use.
```

## Use Flow

### Setup

Execute **Basic** config from SKILL.md.

### Validation

Verify project exists:

1. Check `{BRAIN_PATH}/projects/{name}` exists
2. If not found → list available projects

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
