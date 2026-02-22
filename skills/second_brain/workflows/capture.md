# Workflow: Capture

**Purpose**: Quick capture an idea to inbox with minimal friction.

**Prerequisite**: The user provides or implies an idea to save. If nothing to capture is clear from the conversation, ask "What would you like me to save?"

## Setup

Execute **Basic** config from SKILL.md.

## Process

1. Get timestamp: `date '+%Y-%m-%d-%H-%M'`

2. Generate a short kebab-case topic from the idea (max 5 words)

3. Create file at `{BRAIN_PATH}/inbox/{timestamp}-{topic}.md`:

```markdown
---
captured: {ISO timestamp}
tags: []
type: idea
status: inbox
---

# {Title from idea}

{Full idea text}

---
*Captured via Atlas*
```

4. Confirm:

```
Captured: {BRAIN_PATH}/inbox/{filename}
```
