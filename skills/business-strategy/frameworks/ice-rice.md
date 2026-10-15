# ICE & RICE Scoring

Prioritization frameworks for initiatives, features, and product decisions.

## ICE Scoring

For prioritizing initiatives and features.

**Formula**: ICE Score = (Impact + Confidence + Ease) / 3

### Scoring Criteria

| Score | Impact | Confidence | Ease |
|-------|--------|------------|------|
| 10 | Massive impact on goal | Certain it will work | Can do in hours |
| 7-9 | High impact | Very confident | Can do in days |
| 4-6 | Medium impact | Somewhat confident | Can do in weeks |
| 1-3 | Low impact | Low confidence | Takes months |

### Template

```markdown
## ICE Scoring: {Project/Sprint}

| Initiative | Impact | Confidence | Ease | ICE Score | Priority |
|------------|--------|------------|------|-----------|----------|
| {Initiative 1} | {1-10} | {1-10} | {1-10} | {avg} | {rank} |
| {Initiative 2} | ... | ... | ... | ... | ... |

### Top Priorities (Sorted by ICE)
1. **{Highest ICE}**: Score {X} - {Brief rationale}
2. **{Second}**: Score {X}
3. **{Third}**: Score {X}

### Notes
- Items with ICE > 7: Do immediately
- Items with ICE 5-7: Plan for this quarter
- Items with ICE < 5: Reconsider or backlog
```

## RICE Scoring

For product prioritization with reach consideration.

**Formula**: RICE Score = (Reach x Impact x Confidence) / Effort

### Criteria

| Factor | Definition | Scale |
|--------|------------|-------|
| **Reach** | How many users/customers affected per quarter | Actual number |
| **Impact** | Effect on individual user | 3=Massive, 2=High, 1=Medium, 0.5=Low, 0.25=Minimal |
| **Confidence** | How sure are you | 100%=High, 80%=Medium, 50%=Low |
| **Effort** | Person-months required | Actual estimate |

### Template

```markdown
## RICE Scoring: {Product/Quarter}

| Initiative | Reach | Impact | Confidence | Effort | RICE Score |
|------------|-------|--------|------------|--------|------------|
| {Feature 1} | {users} | {0.25-3} | {50-100%} | {person-months} | {calculated} |
| {Feature 2} | ... | ... | ... | ... | ... |

### Prioritized Roadmap
1. **{Highest RICE}**: {Score} - {one-liner}
2. **{Second}**: {Score}
3. **{Third}**: {Score}

### Low Confidence Items (Need Research)
- {Item requiring validation before committing}
```

## When to Use Which

- **ICE**: Quick prioritization, smaller teams, internal initiatives
- **RICE**: Product roadmaps, larger teams, customer-facing features where reach matters
