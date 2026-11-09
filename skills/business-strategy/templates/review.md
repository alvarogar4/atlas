# Review Templates

Templates for periodic business reviews at all cadences.

## Storage

Resolve scope via `SKILL.md` routing → paths from `atlas:second-brain` → `reference/folder-structure.md`.

## Daily Review Template

**Path**: `{BRAIN_PATH}/areas/reviews/YYYY-WXX/YYYY-MM-DD.md` (ISO week of the day)

Drop sections that don't apply to the user (no task system → no blocks table). Add per-topic sections (one per client, project or area that moved that day) between Blocks and Open.

```yaml
---
created: {timestamp}
updated: {timestamp}
type: review
period: {YYYY-MM-DD}
related:
  - "{previous day's review}"
---

# {Day} {YYYY-MM-DD}

{2-4 sentences: what the day was about, what got done, what moved and why.}

## Blocks

| When | Block | Planned | Actual |
| --- | --- | --- | --- |
| {time} | {block} | {planned} | {actual, or why it didn't happen} |

{Short note on what changed against the plan.}

## {Topic}

{What happened, results, numbers, decisions.}

## Open
- {Unfinished item}: {next step and date}

## Tomorrow
- {time}: {block or event}

## Read on the day
{Atlas's conclusions after the user corrected them: what moved, what slipped and why, patterns, risks for tomorrow.}

## To-do delta
- **Done:** {items}
- **Added:** {items}
```

## Weekly Review Template

**Path**: `{BRAIN_PATH}/areas/reviews/YYYY-WXX/YYYY-WXX-weekly.md` (next to the week's daily reviews)

In the prep version, fill every data-backed section and mark the user's parts with `> [!todo] {user}: ...` callouts; the session replaces them. The prep also drafts **Atlas's read and recommendations**; the session turns it into the agreed table.

```yaml
---
captured: {timestamp}
type: review
period: {YYYY-WXX}
status: prep | final
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
| Planned vs actual time | {value} | {value} | {trend} |
| Unplanned (extra) work share | {value} | {value} | {trend} |
| {metric} | {value} | {value} | {trend} |

## What Slipped
| Item | Times moved | Why |
|------|-------------|-----|
| {item} | {n} | {reason} |

## Content Results
| Post | Channel | Result |
|------|---------|--------|
| {post} | {channel} | {numbers} |

## How the Week Felt
{The user's words: energy, focus, what shaped the week.}

## Atlas's Read and Recommendations
{Prep: 3-6 recommendations, each tied to a number or pattern from this week, ordered by expected impact. Skip anything the user already rejected in earlier weeks unless its reason changed.}

| Recommendation | {User} | Outcome |
|---|---|---|
| {recommendation and the evidence behind it} | {the user's answer, in their words} | {adopted / adopted with changes / not now, revisit when X / dropped} |

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

## Monthly Review Template

**Path**: `{BRAIN_PATH}/areas/reviews/YYYY-MM-monthly.md`

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

## Quarterly Review Template

**Path**: Resolve via `atlas:second-brain` routing (project or personal scope)

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

## Annual Review Template

**Path**: Resolve via `atlas:second-brain` routing (project or personal scope)

```yaml
---
captured: {timestamp}
type: review
period: {YYYY}
---

# Annual Review: {Year}

## Executive Summary
{Strategic overview of the year in 4-6 sentences}

## Vision Assessment

### Original Vision
{What you set out to achieve this year}

### Where You Ended Up
{Honest assessment of current position}

### Gap Analysis
{What's still missing and why}

## Annual Goals Review

### Goals Achieved
| Goal | Result | Impact |
|------|--------|--------|
| {goal} | {achievement} | {what it enabled} |

### Goals Not Achieved
| Goal | Progress | Root Cause | Disposition |
|------|----------|------------|-------------|
| {goal} | {%} | {why it didn't happen} | {carry forward/drop/redesign} |

## Year in Numbers
| Metric | Year Start | Year End | Change |
|--------|-----------|----------|--------|
| {metric} | {value} | {value} | +/-% |

## Top Wins
1. **{Win 1}**: What happened, why it matters, what made it possible
2. **{Win 2}**: ...
3. **{Win 3}**: ...

## Top Misses
1. **{Miss 1}**: What didn't happen, root cause, lesson learned
2. **{Miss 2}**: ...

## Strategic Pivots
| Pivot | When | Why | Assessment |
|-------|------|-----|------------|
| {what changed} | {quarter} | {trigger} | {right call/wrong call/too early to tell} |

## Competitive Landscape Evolution
{How the market and competitors changed. Are you better or worse positioned than 12 months ago?}

## Key Decisions Made
| Decision | Date | Outcome |
|----------|------|---------|
| {decision} | {date} | {impact assessment} |

## Lessons Learned
1. **{Lesson 1}**: {insight and how to apply it going forward}
2. **{Lesson 2}**: ...

## Next Year

### Vision
{Where you want to be in 12 months}

### Strategic Priorities
1. **{Priority 1}**: {why and what success looks like}
2. **{Priority 2}**: ...
3. **{Priority 3}**: ...

### Goals
| Goal | Metric | Target | Quarter |
|------|--------|--------|---------|
| {goal} | {how measured} | {target value} | {target quarter} |

### Risks & Mitigation
1. **{Risk}**: {mitigation strategy}

### What Needs to Change
{Processes, habits, tools, or approaches to start/stop/continue}
```
