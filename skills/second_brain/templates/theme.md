# Theme Template

Template for content theme definitions.

## Slugification

```bash
SLUG=$(echo "{name}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
```

## Content Theme Template

**Path**: `{PROJECT_PATH}/marketing/themes/{theme-slug}.md`

```yaml
---
project: {project_name}
created: {ISO timestamp}
updated: {ISO timestamp}
type: content-theme
theme: {theme-name}
status: active
---

# Theme: {Theme Name}

## Overview
{1-2 sentence description}

## Target Audience
{Who is this content for}

## Channels
- {Primary channel} (primary)
- {Secondary channel}

## Objective
{awareness | leads | conversions | retention}

## Content Guidelines

**Tone**: {Practical, authoritative, conversational, etc.}

**Key Messages**:
1. {Core message 1}
2. {Core message 2}
3. {Core message 3}

## Metrics

| Metric | Target |
|--------|--------|
| Frequency | {n}/month |
| Avg impressions | {n}+ |
| Engagement rate | {n}%+ |
```
