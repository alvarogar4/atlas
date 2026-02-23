# Audience Template

Template for audience persona definitions.

## Slugification

```bash
SLUG=$(echo "{name}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
```

## Audience Persona Template

**Path**: `{PROJECT_PATH}/marketing/audiences/{persona-slug}.md`

```yaml
---
project: {project_name}
captured: {ISO timestamp}
type: audience
tags: [audience, {persona-slug}]
status: active
---

# Persona: {Persona Name}

## Demographics
- **Role**: {Job title, function}
- **Company**: {Size, industry}

## Goals
1. {Goal 1}
2. {Goal 2}
3. {Goal 3}

## Pain Points
1. {Pain point 1}
2. {Pain point 2}
3. {Pain point 3}

## Where They Hang Out
- Online: {Platforms, communities}
- Publications: {What they read}

## Buying Triggers
- {What prompts action}

## Messaging That Works
- Topics: {Derived from goals/pain points}
- Tone: {Reference brand voice if exists}
```
