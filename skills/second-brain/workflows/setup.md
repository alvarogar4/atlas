# Workflow: Setup

**Purpose**: Initialize the brain directory and configure Atlas.

## Process

### 1. Check if Already Configured

Follow the Config Chain from SKILL.md. If `ATLAS_BRAIN_PATH` is found in any source, tell user it's already configured, show the path, ask if they want to reconfigure.

If not found: Proceed to step 2.

### 2. Ask for Brain Path (REQUIRED)

**DO NOT SKIP. DO NOT ASSUME A DEFAULT.**

Ask the user (use a structured question tool such as AskUserQuestion if your harness has one):

```
Where should I store your knowledge base?

Examples:
- ~/brain
- ~/Documents/second-brain
- ~/Dropbox/brain
```

Wait for user's response before proceeding.

### 3. Save Configuration

Create or update the shared config file `${ATLAS_CONFIG:-~/.config/atlas/.env}` (create `~/.config/atlas/` if needed):

```
ATLAS_BRAIN_PATH={USER_PROVIDED_PATH}
```

### 4. Create Directory Structure

```bash
mkdir -p {USER_PROVIDED_PATH}/{inbox,projects,areas,resources,archives,.context}
mkdir -p {USER_PROVIDED_PATH}/areas/{decisions,reviews}
mkdir -p {USER_PROVIDED_PATH}/resources/{market,strategy}
```

### 5. Create Preferences Template

Write to `{BRAIN_PATH}/.context/preferences.md`:

```markdown
---
created: {timestamp}
type: preferences
---

# Preferences

## Communication
- Be direct, skip pleasantries
- Use bullet points for options
- Default language: English (Spanish from Spain if I write in Spanish)

## Technical
- Preferred languages: [fill in]
- Testing framework: [fill in]
- Code style: [fill in]

## Decision Making
- Always consider scalability
- Document trade-offs
- Prefer simple over clever

## Areas of Focus
- [fill in your areas]

## Current Projects
- [fill in active projects]
```

### 6. Create Brain README

Write to `{BRAIN_PATH}/README.md`:

```markdown
# Second Brain

Personal knowledge base using PARA method.

## Structure

- **inbox/** - Quick captures, unprocessed
- **projects/** - Active work with deadlines
- **areas/** - Ongoing responsibilities
- **resources/** - Reference material
- **archives/** - Completed/inactive

## Quick Start

- Capture an idea by telling Atlas to save it
- Search your notes by asking about any topic
- Deep recall by asking "what do I know about X?"
```

### 7. Search Tools (optional)

Atlas finds notes with grep out of the box. Two optional tools add to it (`reference/search-tools.md`): QMD for ranked keyword and meaning search, and the Obsidian CLI for links and tags. Do not install or switch on either one. Only record what is already there, with the user's yes:

- **QMD.** If `command -v qmd` finds it and `qmd status` exits 0, ask whether Atlas should use it for the brain. On a yes, add `ATLAS_QMD_CMD=` with the absolute path that `command -v qmd` printed. The value is one executable by absolute path, never a command line: if the user reaches QMD another way (another machine over ssh), ask them for a wrapper script and save its path. Atlas does not use QMD without this line.
- **Refreshing QMD's index.** Ask whether Atlas may run `qmd update` (it re-reads changed files and runs any update command they attached to a collection). Only on a yes, add `ATLAS_QMD_REFRESH=1`. Atlas then runs `qmd update` before the first search of a session and, in Claude Code, after an agent writes a note in the brain. Atlas never runs `qmd embed` or `qmd pull`: vectors stay the user's setup.
- **Obsidian CLI.** If the Obsidian app is running (`pgrep -x Obsidian`) and `obsidian version` prints a version, add `ATLAS_OBSIDIAN_CMD=obsidian`. On macOS the app binary also answers CLI commands: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`. Don't start Obsidian to find out.

Skip this step silently when neither tool is present.

### 8. Confirm

```
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
