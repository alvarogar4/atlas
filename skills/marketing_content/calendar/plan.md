# Calendar: Plan

**Purpose**: Plan quarterly content calendar with phase objectives.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Setup** from SKILL.md.

## Process

1. **Determine target quarter:**
   - If current quarter has <30 days remaining, plan next quarter
   - Otherwise, plan current quarter

2. **Locate existing content for context:**

```
subagent_type: atlas:core:locate_knowledge
prompt: "Find all marketing content in ${PROJECT_PATH}/marketing/ for quarterly planning

Search for:
- Campaign plans (status: active, planned, completed)
- Published blog posts
- Blog drafts in progress
- Content themes

Return:
- File paths grouped by type
- Status and dates for each item
- Theme distribution across content"
```

3. **Analyze calendar with findings:**

```
subagent_type: atlas:core:analyze_knowledge
prompt: "Analyze marketing content for Q{n} {year} planning

Files to analyze:
{paste file paths from locate_knowledge}

Target quarter: Q{n} {year}

Extract calendar-specific data:
- Content pieces with their dates (published or scheduled)
- Theme/topic for each piece
- Content type (blog, campaign, social)
- Status (published, draft, planned)

Analyze:
- Content already scheduled for this quarter
- Theme coverage and gaps (which themes have few posts)
- Posting frequency patterns
- Weeks with no content scheduled
- Conflicts (multiple pieces on same day, theme overload)

Return:
- Current state summary
- Gaps identified (weeks with no content)
- Theme balance assessment
- Conflicts or scheduling issues"
```

**Wait for BOTH agents to complete.**

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
