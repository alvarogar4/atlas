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

2. **Load project knowledge:**

Read these files to inform planning:

- `{PROJECT_PATH}/strategy/strategy.md` — Vision, goals, priorities, success metrics
- `{PROJECT_PATH}/marketing/themes/*.md` — Available content themes (topics, keywords, frequency targets)
- `{PROJECT_PATH}/marketing/audiences/*.md` — Target audience personas (goals, pain points, preferred channels)

Skip any that don't exist yet, but note them as gaps to the user and propose creating them first.

3. **Survey existing content:**

```bash
# List all content folders with their pipeline state
ls ${PROJECT_PATH}/marketing/content/*/1_research.md 2>/dev/null
ls ${PROJECT_PATH}/marketing/content/*/2_plan.md 2>/dev/null
ls ${PROJECT_PATH}/marketing/content/*/3_draft-*.md 2>/dev/null
```

```bash
# Read existing calendar if present
cat ${PROJECT_PATH}/marketing/calendars/${YEAR}-Q${QUARTER}.md 2>/dev/null
```

4. **Analyze content state:**

From the loaded knowledge and content survey, build:

- Content pieces with dates and pipeline status
- Theme coverage (which themes have content, which are underserved)
- Audience coverage (which personas are being addressed)
- Gaps (weeks with no content)
- Scheduling conflicts

5. **Present analysis and gather phase objectives:**

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

6. **CHECKPOINT — STOP AND WAIT.**

```
Save quarterly plan? (y/n)
This will create: marketing/calendars/{year}-Q{n}.md
```

7. **Assign per-entry references:**

For each scheduled entry, ask: "Which competitor or audience files should be loaded when working on this piece?"

List available files:

- Competitors: `ls {PROJECT_PATH}/competitors/*.md`
- Audiences: `ls {PROJECT_PATH}/marketing/audiences/*.md`

Populate the References column accordingly. Leave empty for entries that don't need specific context.

8. **If confirmed**, save the calendar using the Content Calendar template from `second_brain/templates/calendar.md` at path `{PROJECT_PATH}/marketing/calendars/{year}-Q{n}.md`.
