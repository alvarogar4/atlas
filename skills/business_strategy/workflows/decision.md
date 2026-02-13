# Workflow: Decision

**Purpose**: Document a major business decision with context and rationale.

## Process

1. **Understand the decision**:
   - What decision needs to be made?
   - What options are being considered?
   - What's the deadline?
   - Who needs to be involved?

2. **Check for relevant analysis**:

Read `{BRAIN_PATH}/resources/strategy/{topic}/analysis.md` if it exists.

3. If no analysis exists, offer to create one first.

4. **Document the decision** using the template from `templates/decision-log.md`:

```yaml
---
captured: {timestamp}
type: decision-log
topic: {topic}
status: {pending|decided|implemented}
decided_date: {date if decided}
---

# Decision: {Topic}

## Context
{What situation requires this decision}

## Decision Statement
{Clear statement of what needs to be decided}

## Options Considered

### Option A: {Name}
- **Description**: {what this involves}
- **Pros**:
  - {benefit 1}
  - {benefit 2}
- **Cons**:
  - {drawback 1}
  - {drawback 2}
- **Cost/Effort**: {estimate}
- **Risk**: {high/medium/low}

### Option B: {Name}
...

## Decision
**Chosen**: {Option name}
**Rationale**: {Why this option}
**Trade-offs accepted**: {What we're giving up}

## Implementation
- [ ] {Step 1}
- [ ] {Step 2}
- [ ] {Step 3}

## Success Criteria
{How we'll know this was the right decision}

## Review Date
{When to revisit this decision}

## Related
- {Link to analysis if exists}
- {Link to related decisions}
```

5. **Save to**: `{BRAIN_PATH}/areas/decisions/YYYY-MM-DD-{topic}.md`

6. **Output summary**:

```
Decision documented: {path}

Decision: {chosen option}
Key trade-off: {main trade-off}

Implementation steps identified: {count}
Review date set: {date}
```
