# Project File Templates

All templates for project-related files. Referenced by project definition workflows.

## Slugification

Convert names to slugs for file paths:

```bash
SLUG=$(echo "{name}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
```

---

## README Template

**Path:** `{PROJECT_PATH}/README.md`

```yaml
---
created: {ISO timestamp}
type: project
status: active
---

# Project: {Name}

## Overview
{Project description - populated by project-context}

## Content Themes
1. {Theme 1}
2. {Theme 2}
3. {Theme 3}

## Target Audience
{Audience description}

## Stats
- Content pieces: 0
- Last activity: {date}
```

## Context Template

**Path:** `{PROJECT_PATH}/context.md`

```yaml
---
project: {project_name}
created: {ISO timestamp}
updated: {ISO timestamp}
type: project-context
---

# Project Context: {Project Name}

## What It Is
{Brief description of the project/business}

## Problem It Solves
{Pain point or problem addressed}

## Core Offering
{Product or service description}

## Target Customer
{Brief customer description}

## Unique Value Proposition
{What makes it different/better}

## Stage
{Current stage: idea | MVP | growth | established}

## Marketing Goals
{Primary objectives: awareness | leads | conversions | retention}

## Summary
{2-3 sentence elevator pitch based on above}
```

## Strategy Template

**Path:** `{PROJECT_PATH}/strategy/strategy.md`

```yaml
---
project: {project_name}
created: {ISO timestamp}
updated: {ISO timestamp}
type: project-strategy
---

# Strategy: {Project Name}

## Vision
{Where we want to be in 2-3 years}

## Mission
{How we create value for our target customer}

## Strategic Objectives

### Primary Goal
{The #1 thing we're trying to achieve}

### Supporting Goals
1. {Goal 1}
2. {Goal 2}
3. {Goal 3}

## Target Market

### Primary Segment
{Who we serve first}

### Expansion Segments
{Future segments to pursue}

## Competitive Positioning

### Our Differentiation
{What makes us different/better}

### Key Advantages
1. {Advantage 1}
2. {Advantage 2}

## Key Initiatives

### Current Quarter
1. {Initiative 1}
2. {Initiative 2}

## Success Metrics

| Metric | Current | Target | Timeline |
|--------|---------|--------|----------|
| {metric} | {value} | {target} | {date} |

## Review Schedule
- Weekly: {what to review}
- Monthly: {what to review}
- Quarterly: {what to review}
```

## Brand Voice Template

**Path:** `{PROJECT_PATH}/marketing/brand-voice.md`

```yaml
---
project: {project_name}
created: {ISO timestamp}
updated: {ISO timestamp}
type: brand-voice
---

# Brand Voice: {Project Name}

## Personality
{Core brand personality}

## Tone
{Content tone}

## Key Messages
1. {Message 1}
2. {Message 2}
3. {Message 3}

## Language Guidelines

### Words to Use
- {Word/phrase that fits the brand}

### Words to Avoid
- {Word/phrase to avoid}

## Target Audience
{Brief audience description}

## Examples

### Good Example
> {Example text demonstrating the brand voice}

### Bad Example
> {Counter-example showing what NOT to do}
```

## Visual Identity Template

**Path:** `{PROJECT_PATH}/marketing/visual-identity.md`

```yaml
---
project: {project_name}
created: {ISO timestamp}
updated: {ISO timestamp}
type: visual-identity
---

# Visual Identity: {Project Name}

## Color Palette

### Primary Colors
| Name | Hex | Usage |
|------|-----|-------|
| Primary | {hex} | Main brand color, CTAs, headers |
| Secondary | {hex} | Supporting elements, accents |

### Extended Palette
| Name | Hex | Usage |
|------|-----|-------|
| Tertiary | {derived} | Highlights, decorative |
| Accent | {derived} | Interactive states |
| Surface | #FFFFFF | Backgrounds, cards |
| Muted | {derived} | Subtle elements |
| Border | {derived} | Dividers, outlines |

### Semantic Colors
| Name | Hex | Usage |
|------|-----|-------|
| Success | #10B981 | Positive states |
| Warning | #F59E0B | Caution states |
| Error | #EF4444 | Error states |
| Info | #3B82F6 | Informational |

## Visual Style

- **Aesthetic**: {style}
- **Mood**: {mood}
- **Rendering**: {style}
```

## Audience Persona Template

**Path:** `{PROJECT_PATH}/marketing/audiences/{persona-slug}.md`

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

## Competitor Profile Template

**Path:** `{PROJECT_PATH}/competitors/{competitor-slug}.md`

```yaml
---
project: {project_name}
captured: {ISO timestamp}
type: competitor
competitor: {competitor-name}
status: active
---

# Competitor: {Competitor Name}

## Overview
- **Website**: {URL}
- **Core Offering**: {Product/service}
- **Target Market**: {Who they serve}

## Positioning
{How they position themselves}

## Strengths
1. {Strength 1}
2. {Strength 2}
3. {Strength 3}

## Weaknesses
1. {Weakness 1}
2. {Weakness 2}
3. {Weakness 3}

## Our Differentiation
{How we differentiate from them}

## Notes
{Additional observations}
```

## Content Calendar Template

**Path:** `{PROJECT_PATH}/marketing/calendars/{year}-Q{n}.md`

```yaml
---
project: {project_name}
period: Q{n} {year}
created: {ISO timestamp}
updated: {ISO timestamp}
type: content-calendar
---

# Content Calendar: Q{n} {Year}

## Phase Objective

**Goal**: {high-level goal}

**Success Criteria**:
- [ ] {measurable target 1}
- [ ] {measurable target 2}

## Scheduled Content

| Week | Date | Content | Type | Theme | Objective | Status |
|------|------|---------|------|-------|-----------|--------|
| W1 | {date} | {title} | Blog | {theme} | {objective} | Planned |
```

## Theme File Template

**Path:** `{PROJECT_PATH}/marketing/themes/{theme-slug}.md`

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
