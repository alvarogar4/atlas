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

Atlas finds notes with grep out of the box. Two optional tools add to it (`reference/search-tools.md`): QMD for ranked keyword and meaning search, and the Obsidian CLI for links and tags. Do not install or switch on either one. Only record what is already there:

- If `qmd status` works, add `ATLAS_QMD_CMD=qmd` to the config file. If the user reaches QMD another way (a wrapper, another machine over ssh), ask for that command and save it instead.
- If `obsidian version` prints a version, add `ATLAS_OBSIDIAN_CMD=obsidian`. On macOS the app binary also answers CLI commands: `/Applications/Obsidian.app/Contents/MacOS/Obsidian`.

With `ATLAS_QMD_CMD` set, the plugin also refreshes QMD's index in the background each time an agent writes a note in the brain. Skip this step silently when neither tool is present.

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
