# Calendar: View

**Purpose**: View current quarter marketing calendar summary with theme balance.

## Setup

Execute **Config** from SKILL.md.

## Process

1. **Determine current quarter:**

```bash
MONTH=$(date +%m)
YEAR=$(date +%Y)
QUARTER=$((($MONTH - 1) / 3 + 1))
```

2. **Locate current quarter content:**

```
subagent_type: atlas:core:locate_knowledge
prompt: "Find all marketing content for Q{quarter} {year} in ${PROJECT_PATH}/marketing/

Search for:
- Campaign plans (status: active or planned)
- Published blog posts this quarter
- Scheduled content
- Content themes

Return:
- File paths organized by type (campaigns, blogs, themes)
- Dates and status for each item
- Brief summary of content type"
```

Wait for locator to complete.

3. **Create calendars directory if needed:**

```bash
mkdir -p ${PROJECT_PATH}/marketing/calendars
```

4. **Read themes:**

```bash
ls ${PROJECT_PATH}/marketing/themes/*.md 2>/dev/null | head -20
```

5. **Generate summary:**

```
Marketing Calendar: {Project} - Q{n} {Year}

## Overview
| Month | Campaigns | Blog Posts | Primary Theme |
|-------|-----------|------------|---------------|
| {Month 1} | {name} | {n} posts | {theme} |
| {Month 2} | - | {n} posts | {theme} |
| {Month 3} | {name} | {n} posts | {theme} |

## Theme Balance
{Theme 1}: ████████░░ 80% (target: 70%) ✓
{Theme 2}: ██░░░░░░░░ 20% (target: 30%) ⚠

## Upcoming (Next 30 Days)
- {date}: {type} - {title}
- {date}: {type} - {title}

## Gaps
- Week {n}: No content planned
- {Theme}: Below target this quarter
```
