# Calendar: View

**Purpose**: View current quarter marketing calendar summary with theme balance.

## Setup

Execute **Project** config from `atlas:second-brain`.

## Process

1. **Determine current quarter:**

```bash
MONTH=$(date +%m)
YEAR=$(date +%Y)
QUARTER=$((($MONTH - 1) / 3 + 1))
```

2. **Find current quarter content:**

```bash
# List content folders for this quarter
ls -d ${PROJECT_PATH}/marketing/content/${YEAR}-* 2>/dev/null
```

```bash
# Read calendar file if it exists
cat ${PROJECT_PATH}/marketing/calendars/${YEAR}-Q${QUARTER}.md 2>/dev/null
```

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
