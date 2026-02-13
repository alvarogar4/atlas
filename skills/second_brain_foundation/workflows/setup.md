# Workflow: Setup

**Purpose**: Initialize the brain directory and configure Atlas.

## Process

### 1. Check if Already Configured

Follow the Config Chain from SKILL.md. If `ATLAS_BRAIN_PATH` is found in any source, tell user it's already configured, show the path, ask if they want to reconfigure.

If not found: Proceed to step 2.

### 2. Ask for Brain Path (REQUIRED)

**DO NOT SKIP. DO NOT ASSUME A DEFAULT.**

Use AskUserQuestion:

```
Where should I store your knowledge base?

Examples:
- ~/brain
- ~/Documents/second-brain
- ~/Dropbox/brain
```

Wait for user's response before proceeding.

### 3. Save Configuration

Ask the user where to store the config:

Options:
1. `.env` file in current directory (portable, works with any tool)
2. `~/.claude/CLAUDE.md` (Claude Code-specific)

**If `.env`**: Create or update `.env`:
```
ATLAS_BRAIN_PATH={USER_PROVIDED_PATH}
```

**If `~/.claude/CLAUDE.md`**: Append Atlas configuration section:

```markdown

# Atlas Configuration

ATLAS_BRAIN_PATH={USER_PROVIDED_PATH}
```

Use Edit tool — do not overwrite existing content.

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

### 7. Confirm

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
