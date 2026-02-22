# Calendar: Plan

**Purpose**: Plan quarterly content calendar with phase objectives.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine target quarter:**
   - If current quarter has <30 days remaining, plan next quarter
   - Otherwise, plan current quarter

2. **Survey existing content:**

```bash
# List all content folders with their pipeline state
ls ${PROJECT_PATH}/marketing/content/*/1_research.md 2>/dev/null
ls ${PROJECT_PATH}/marketing/content/*/2_plan.md 2>/dev/null
ls ${PROJECT_PATH}/marketing/content/*/3_draft-*.md 2>/dev/null
```

```bash
# Read themes for coverage analysis
cat ${PROJECT_PATH}/marketing/themes/*.md 2>/dev/null
```

```bash
# Read existing calendar if present
cat ${PROJECT_PATH}/marketing/calendars/${YEAR}-Q${QUARTER}.md 2>/dev/null
```

3. **Analyze content state:**

From the file listing above, build:

- Content pieces with dates and pipeline status
- Theme coverage (which themes have content, which don't)
- Gaps (weeks with no content)
- Scheduling conflicts

4. **Present analysis and gather phase objectives:**

```
Quarterly Planning: {Project} - Q{n} {Year}

## Phase Context
**Period**: {start date} - {end date}
**Phase Objective**: {ask user for high-level goal}
**Success Criteria**:
- {ask user for measurable targets}

## Current State
- Campaigns planned: {n}
- Blog posts scheduled: {n}
- Theme coverage: {breakdown}

## Gaps Identified
1. Week {n}: No content → Recommend: Blog on {theme}
2. {Theme}: Underrepresented → Recommend: Add {n} posts

## Conflicts
1. {Date}: {description} → Recommend: {action}
```

5. **CHECKPOINT — STOP AND WAIT.**

```
Save quarterly plan? (y/n)
This will create: marketing/calendars/{year}-Q{n}.md
```

6. **If yes**, save plan file:

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
**Goal**: {user-provided high-level goal}

**Success Criteria**:
- [ ] {measurable target 1}
- [ ] {measurable target 2}
- [ ] {measurable target 3}

## Scheduled Content
| Week | Date | Content | Type | Theme | Objective | Status |
|------|------|---------|------|-------|-----------|--------|
| W1 | Jan 6 | {title} | Blog | {theme} | Position as expert | Planned |
| W2 | Jan 13 | {title} | LinkedIn | {theme} | Build awareness | Planned |

## Notes
{Any special considerations, holidays, events}
```
