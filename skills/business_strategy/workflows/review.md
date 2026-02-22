# Workflow: Review

Consolidates strategic reviews and periodic business reviews.

## Mode Selection

Determine the review period from the conversation:

- Weekly review, "this week" → Weekly
- Monthly review, "this month" → Monthly
- Quarterly review, "this quarter", strategic review → Quarterly
- Just "review" with no qualifier → Default to weekly

---

## Mode: Weekly

**Purpose**: Reflect on week, plan next week.

### Process

1. Get current week: `date '+%Y-W%V'`

2. **Find recent activity**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this week in {BRAIN_PATH}/

Time filter: Files modified in the last 7 days (-mtime -7)

Search all PARA categories:
- projects/ - Active work
- areas/ - Ongoing areas of responsibility
- resources/ - Reference material
- inbox/ - New captures

Return:
- File paths grouped by category
- Modification dates
- Content type (note, decision, idea, etc.)
- Brief summary of what changed"
```

3. Walk through review questions with user:

**Wins & Accomplishments**: What went well? What progress was made?

**Challenges & Learnings**: What didn't go as planned? What did you learn?

**Key Metrics** (if applicable): Any numbers to track?

**Open Loops**: What's unfinished? What needs follow-up?

**Next Week Focus**: Top 3 priorities? Important dates?

4. Create weekly review:

```yaml
---
captured: {timestamp}
type: review
period: {YYYY-WXX}
---

# Weekly Review: {Week of Date}

## Summary
{1-2 sentence summary of the week}

## Wins
1. {Accomplishment 1}
2. {Accomplishment 2}

## Challenges
1. {Challenge 1}
   - Learning: {what you learned}

## Key Metrics
| Metric | This Week | Last Week | Trend |
|--------|-----------|-----------|-------|
| {metric} | {value} | {value} | {trend} |

## Open Loops
- [ ] {Unfinished item 1}
- [ ] {Unfinished item 2}

## Next Week Focus
### Top 3 Priorities
1. {Priority 1}
2. {Priority 2}
3. {Priority 3}

### Key Dates
- {date}: {event/deadline}
```

5. Save to: `{BRAIN_PATH}/areas/reviews/YYYY-WXX-weekly.md`

---

## Mode: Monthly

**Purpose**: Reflect on month, assess progress, set direction.

### Process

1. Get current month: `date '+%Y-%m'`

2. **Gather monthly data**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this month in {BRAIN_PATH}/

Time filter: Files modified in the last 30 days (-mtime -30)

Search all PARA categories with emphasis on:
- projects/ - Project progress
- areas/decisions/ - Decisions made
- areas/reviews/ - Weekly reviews

Return:
- File paths grouped by category
- Summary of activity level per area
- Key changes identified"
```

3. Read weekly reviews to synthesize.

4. Walk through monthly questions:

**Accomplishments**: What did you complete? Goal progress?

**Learnings**: New knowledge or skills? Insights?

**Metrics**: How did key metrics perform?

**Projects**: Status updates? Completions or starts?

**Next Month**: Goals? Adjustments needed?

5. Create monthly review:

```yaml
---
captured: {timestamp}
type: review
period: {YYYY-MM}
---

# Monthly Review: {Month Year}

## Executive Summary
{3-4 sentence overview}

## Goals Review
| Goal | Status | Progress | Notes |
|------|--------|----------|-------|
| {goal} | {status} | {%} | {notes} |

## Key Accomplishments
1. {Major accomplishment 1}
2. {Major accomplishment 2}

## Metrics Dashboard
| Metric | Target | Actual | vs Last Month |
|--------|--------|--------|---------------|
| {metric} | {target} | {actual} | +/-% |

## Projects Update
| Project | Status | Progress | Next Milestone |
|---------|--------|----------|----------------|
| {project} | {status} | {%} | {milestone} |

## Learnings
1. **{Topic}**: {What you learned}

## Next Month
### Goals
1. {Goal 1}
2. {Goal 2}
```

6. Save to: `{BRAIN_PATH}/areas/reviews/YYYY-MM-monthly.md`

---

## Mode: Quarterly

**Purpose**: Strategic review, major course corrections.

### Process

1. Calculate quarter: `month=$(date '+%m'); year=$(date '+%Y'); quarter=$(( (month - 1) / 3 + 1 )); echo "${year}-Q${quarter}"`

2. **Gather quarterly data**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find all files modified this quarter in {BRAIN_PATH}/

Time filter: Files modified in the last 90 days (-mtime -90)

Search all PARA categories with emphasis on:
- projects/ - Project completions and progress
- resources/strategy/ - Strategic analyses
- areas/decisions/ - Major decisions
- areas/reviews/ - Monthly reviews

Return:
- File paths grouped by category
- Summary of quarter activity
- Major milestones and changes"
```

3. Read monthly reviews to synthesize.

4. Walk through quarterly questions:

**Goals Achievement**: Quarter goals met? What was achieved? What wasn't, and why?

**Strategic Progress**: Moving toward vision? Pivots needed?

**Major Wins**: Biggest accomplishments? What made them possible?

**Major Challenges**: Biggest obstacles? What would you do differently?

**Next Quarter**: Strategic priorities? Changes to approach?

5. Create quarterly review:

```yaml
---
captured: {timestamp}
type: review
period: {YYYY-QX}
---

# Quarterly Review: {Quarter Year}

## Executive Summary
{Strategic overview of the quarter}

## Quarter Goals Review

### Goals Achieved
| Goal | Result | Notes |
|------|--------|-------|
| {goal} | {achievement} | {context} |

### Goals Not Achieved
| Goal | Progress | Reason | Disposition |
|------|----------|--------|-------------|
| {goal} | {%} | {why} | {continue/drop/modify} |

## Strategic Assessment

### Progress Toward Vision
{How this quarter moved you toward long-term goals}

### Market/External Changes
{Relevant changes in environment}

## Quarterly Metrics
| Metric | Q Start | Q End | Change | Trend |
|--------|---------|-------|--------|-------|
| {metric} | {value} | {value} | +/-% | {trend} |

## Major Wins
1. **{Win 1}**: Impact and success factors

## Major Challenges
1. **{Challenge 1}**: Impact, response, learning

## Key Decisions Made
| Decision | Date | Outcome Assessment |
|----------|------|-------------------|
| {decision} | {date} | {good/okay/revisit} |

## Next Quarter

### Strategic Priorities
1. **{Priority 1}**: {why and what}
2. **{Priority 2}**: {why and what}

### Goals
| Goal | Metric | Target |
|------|--------|--------|
| {goal} | {how measured} | {target value} |

### Risks to Watch
1. {Risk}: {mitigation}
```

6. Save to: `{BRAIN_PATH}/areas/reviews/YYYY-QX-quarterly.md`
