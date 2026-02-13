# Project Management

Consolidated project CRUD operations.

---

## Action: project-create

### Setup
Execute **Basic Setup** from SKILL.md.

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

4. Set as active project — update `~/.claude/CLAUDE.md`:
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

## Action: project-list

### Setup
Execute **Basic Setup** from SKILL.md.

### Process

1. Read active project from `~/.claude/CLAUDE.md` → `ATLAS_ACTIVE_PROJECT`
2. List all directories in `{BRAIN_PATH}/projects/`
3. For each project, count content topics and drafts by channel
4. Display with active indicator (*)

### Output Format

```
Projects in {BRAIN_PATH}/projects/:

  * active-project
    - Content topics: 8
    - Drafts: blog (3), linkedin (5), twitter (2)
    - Last activity: 2025-12-20

    another-project
    - Content topics: 0
    - Last activity: 2025-12-15

To switch projects, just tell me which one to use.
```

---

## Action: project-use

### Setup
Execute **Basic Setup** from SKILL.md.

### Validation
Verify project exists in `{BRAIN_PATH}/projects/`. If not, list available projects.

### Process

1. Update `~/.claude/CLAUDE.md`:
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
Execute **Basic Setup** from SKILL.md.

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
