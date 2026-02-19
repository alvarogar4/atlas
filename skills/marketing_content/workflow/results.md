# Workflow: Results

**Purpose**: Document content performance metrics and learnings after publishing. Closes the feedback loop.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Config** from SKILL.md.

## Process

1. **Determine channel and topic**: Use the channel and topic from conversation.

2. **Find content folder:**

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${topic}* 2>/dev/null | head -1)
```
If not found → "Content folder not found."

3. **Read draft to understand what was published:**

```bash
cat "${CONTENT_FOLDER}/3_draft-${channel}.md"
```

4. **CHECKPOINT — STOP AND WAIT.** Gather metrics by channel:

**Blog:**
```
Recording results for: {title}

Please provide metrics (leave blank if not available):
- Page views:
- Unique visitors:
- Avg. time on page:
- Bounce rate:
- Social shares:
- Comments:
- Backlinks gained:
- Search ranking for target keyword:
- Conversions (if applicable):
```

**LinkedIn:**
```
- Impressions:
- Reactions:
- Comments:
- Reposts:
- Click-through rate:
- Profile visits from post:
- New followers:
- Engagement rate:
```

**Twitter:**
```
- Impressions:
- Likes:
- Retweets:
- Replies:
- Quote tweets:
- Link clicks:
- Profile visits:
- New followers:
```

**Email:**
```
- Emails sent:
- Delivered:
- Open rate:
- Click rate:
- Unsubscribes:
- Replies:
- Conversions:
- Revenue (if applicable):
```

5. **CHECKPOINT — STOP AND WAIT.** Gather learnings:

```
What worked well?
What didn't work?
What would you do differently?
Key insight for future content:

Should this content be:
[ ] Repurposed to other formats
[ ] Updated/refreshed later
[ ] Used as a template for similar content
[ ] Promoted further
```

6. **Save:** `${CONTENT_FOLDER}/5_results-${channel}.md`

### Output

```
Results documented: ${CONTENT_FOLDER}/5_results-${channel}.md

Performance: {ABOVE_BENCHMARK / MEETS_BENCHMARK / BELOW_BENCHMARK}
Key learning: {one-sentence summary}
Suggested next action: {based on results}
```

## Output Format

```yaml
---
channel: "{channel}"
topic: "{topic}"
project: {project}
published: {date}
recorded: {ISO timestamp}
performance: {above_benchmark|meets_benchmark|below_benchmark}
---

# Content Results: {Title}

## Content Summary
- **Channel**: {channel}
- **Topic**: {topic}
- **Published**: {date}
- **URL**: {if applicable}

## Performance Metrics
{Channel-specific metrics table}

### Benchmark Comparison
| Metric | Result | Benchmark | Status |
|--------|--------|-----------|--------|
| {metric} | {value} | {benchmark} | {above/meets/below} |

## Analysis

### What Worked
1. {insight}

### What Didn't Work
1. {insight}

### Key Learning
{One paragraph summary}

## Recommendations

### For This Content
- [ ] {action item}

### For Future Content
- [ ] {pattern to repeat}
- [ ] {pattern to avoid}

## Repurposing Opportunities
| Format | Status | Notes |
|--------|--------|-------|
| LinkedIn post | {done/planned/skip} | |
| Twitter thread | {done/planned/skip} | |
| Email newsletter | {done/planned/skip} | |
```

## Benchmarks by Channel

### Blog
| Metric | Good | Great |
|--------|------|-------|
| Page views (first week) | 100+ | 500+ |
| Avg. time on page | 2+ min | 4+ min |
| Bounce rate | <70% | <50% |
| Social shares | 10+ | 50+ |

### LinkedIn
| Metric | Good | Great |
|--------|------|-------|
| Impressions | 1,000+ | 5,000+ |
| Engagement rate | 2%+ | 5%+ |
| Comments | 10+ | 50+ |

### Twitter
| Metric | Good | Great |
|--------|------|-------|
| Impressions | 1,000+ | 10,000+ |
| Engagement rate | 1%+ | 3%+ |
| Retweets | 5+ | 25+ |

### Email
| Metric | Good | Great |
|--------|------|-------|
| Open rate | 20%+ | 35%+ |
| Click rate | 2%+ | 5%+ |
| Unsubscribe rate | <0.5% | <0.2% |
