# Project Management

Consolidated project CRUD operations.

---

## Action: project-create

### Setup

Execute **Basic** config from SKILL.md.

### Validation

Project name must be kebab-case (lowercase, hyphens, numbers only). If invalid, show format and example.

### Process

1. Check project doesn't already exist:

   ```bash
   # If {BRAIN_PATH}/projects/{name} exists → error
   ```

2. Create minimal structure:

   ```bash
   mkdir -p {BRAIN_PATH}/projects/{name}
   ```

3. Generate README.md using template from `reference/project-templates.md`.

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

---

## Action: project-link

Link an external project directory so Atlas treats it like a local project.

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

---

## Action: project-unlink

Remove the link to an external project. Does NOT delete any files.

### Setup

Execute **Basic** config from SKILL.md.

### Arguments

- `{name}` — project name to unlink

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

---

## Action: project-list

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

### Output Format

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

---

## Action: project-use

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

---

## Action: project-info

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

### Output Format

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
