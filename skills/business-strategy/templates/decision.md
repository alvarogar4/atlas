# Decision Log Templates

Templates and tools for documenting business decisions.

## Storage

Resolve scope via `SKILL.md` routing → paths from `atlas:second-brain` → `reference/folder-structure.md`.

## Full Decision Log Template

For major decisions requiring thorough analysis:

```yaml
---
captured: {timestamp}
updated: {timestamp}
type: decision-log
topic: {topic}
status: {pending|decided|implemented|reviewed}
decided_date: {date if decided}
decision_maker: {who made the call}
stakeholders: [{who was involved}]
reversibility: {easily|with effort|irreversible}
impact: {high|medium|low}
---

# Decision: {Clear Decision Title}

## Status
**Current**: {Pending/Decided/Implemented/Reviewed}
**Last updated**: {date}

## Context

### Background
{What situation or opportunity prompted this decision?}

### Constraints
- **Time**: {deadline or urgency}
- **Budget**: {financial constraints}
- **Resources**: {people, tools, dependencies}
- **Technical**: {technical limitations}

### Success Criteria
{How will we know this decision was correct?}

## Options Considered

### Option A: {Name}

**Description**: {What this option involves}

**Pros**:
- {Benefit 1}
- {Benefit 2}
- {Benefit 3}

**Cons**:
- {Drawback 1}
- {Drawback 2}

**Effort/Cost**: {Estimate}
**Risk Level**: {High/Medium/Low}
**Reversibility**: {Easy/Moderate/Difficult}

### Option B: {Name}

**Description**: {What this option involves}

**Pros**:
- {Benefit 1}
- {Benefit 2}

**Cons**:
- {Drawback 1}
- {Drawback 2}

**Effort/Cost**: {Estimate}
**Risk Level**: {High/Medium/Low}
**Reversibility**: {Easy/Moderate/Difficult}

### Option C: Do Nothing

**Description**: Maintain status quo

**Pros**:
- No immediate effort required
- No risk of change

**Cons**:
- {What problem continues}
- {What opportunity is missed}

## Decision Matrix (Optional)

| Criteria | Weight | Option A | Option B | Option C |
|----------|--------|----------|----------|----------|
| {Criteria 1} | {1-5} | {1-5} | {1-5} | {1-5} |
| {Criteria 2} | {1-5} | {1-5} | {1-5} | {1-5} |
| {Criteria 3} | {1-5} | {1-5} | {1-5} | {1-5} |
| **Weighted Total** | | {sum} | {sum} | {sum} |

## Decision

**Chosen Option**: {Option name}

**Rationale**:
{Clear explanation of why this option was selected}

**Key Factors**:
1. {Most important reason}
2. {Second reason}
3. {Third reason}

**Trade-offs Accepted**:
{What we're giving up or accepting by choosing this option}

## Implementation Plan

### Immediate Actions
- [ ] {Action 1} - {owner} - {date}
- [ ] {Action 2} - {owner} - {date}

### Follow-up Actions
- [ ] {Action 3} - {owner} - {date}
- [ ] {Action 4} - {owner} - {date}

### Communication
- {Who needs to be informed}
- {How and when}

## Review

**Review Date**: {When to assess this decision}

**Review Criteria**:
- {Metric or observation to check}
- {Another criterion}

### Post-Implementation Notes
{Add notes after implementation}

**Outcome**: {What actually happened}
**Lessons Learned**: {What we'd do differently}

## Related Documents
- [{Related decision}](path/to/decision.md)
- [{Supporting analysis}](path/to/analysis.md)
```

## Quick Decision Template

For smaller decisions that don't need full analysis:

```yaml
---
captured: {timestamp}
type: decision
topic: {topic}
status: decided
---

# Decision: {Topic}

**Context**: {Brief situation}

**Options**:
1. {Option A}
2. {Option B}

**Decision**: {What we decided}

**Rationale**: {Why}

**Next step**: {Immediate action}
```

## Decision Quality Checklist

Before finalizing a decision, verify:

### Analysis Quality

- [ ] Problem is clearly defined
- [ ] At least 2-3 options considered
- [ ] "Do nothing" option evaluated
- [ ] Pros and cons for each option
- [ ] Key assumptions identified

### Decision Quality

- [ ] Rationale is documented
- [ ] Trade-offs are explicit
- [ ] Decision maker is clear
- [ ] Stakeholders are identified

### Implementation Quality

- [ ] Next steps are defined
- [ ] Owners are assigned
- [ ] Timeline is set
- [ ] Review date is scheduled

## Pre-Mortem Analysis

Before finalizing major decisions, imagine failure:

```markdown
## Pre-Mortem: {Decision}

**Scenario**: It's 6 months from now. This decision has failed spectacularly.

### What Went Wrong?

1. {Possible failure mode 1}
2. {Possible failure mode 2}
3. {Possible failure mode 3}

### Warning Signs We Ignored

- {Signal we should have noticed}
- {Assumption that was wrong}

### What Could We Have Done?

- {Prevention for failure 1}
- {Prevention for failure 2}

### Mitigations to Add Now

Based on this pre-mortem:

- {Safeguard to implement}
- {Checkpoint to add}
- {Alternative to prepare}
```

## Second-Order Thinking

For high-impact decisions, think beyond immediate effects:

```markdown
## Second-Order Consequences: {Decision}

### First-Order Effects (Immediate)

What happens directly as a result:

- {Effect 1}
- {Effect 2}

### Second-Order Effects (Reactions)

What happens because of the first-order effects:

- {Consequence of Effect 1}
- {How others will respond}
- {Unintended consequences}

### Third-Order Effects (Ripples)

Longer-term systemic impacts:

- {Market/competitive response}
- {Cultural/organizational shift}
- {New problems or opportunities created}

### Net Assessment

Considering all orders of effects:

- **Benefits outweigh costs?** {Yes/No/Uncertain}
- **Acceptable risks?** {Yes/No}
- **Proceed?** {Yes/No/Need more info}
```

## Reversibility Assessment

```markdown
## Reversibility: {Decision}

### Type Assessment

- [ ] **Type 1 (Irreversible)**: Like walking through a one-way door
- [ ] **Type 2 (Reversible)**: Like walking through a two-way door

### If Type 1 (Irreversible)

- Take more time
- Get more data
- Involve more stakeholders
- Consider pilots or phased approach

### If Type 2 (Reversible)

- Move faster
- Learn by doing
- Course correct as needed
- Don't over-analyze

### Reversal Cost

If we need to undo this decision:

- **Time**: {how long}
- **Money**: {cost}
- **Reputation**: {impact}
- **Relationships**: {impact}

### Recommendation

{Based on reversibility, how much analysis is appropriate}
```

## Decision Review Template

For quarterly reviews of past decisions:

```markdown
## Decision Review: {Quarter/Year}

### Decisions Reviewed

#### {Decision 1}

- **Made**: {date}
- **Expected outcome**: {what we thought}
- **Actual outcome**: {what happened}
- **Assessment**: {Good/Okay/Poor}
- **Learning**: {what to do differently}

### Pattern Analysis

- **Decisions that worked well**: {common factors}
- **Decisions that didn't work**: {common factors}
- **Blind spots identified**: {recurring issues}

### Process Improvements

Based on this review:

1. {Improvement to decision process}
2. {New criterion to consider}
3. {Stakeholder to involve earlier}
```

## Common Decision Types

| Type            | Key Criteria                                                       |
| --------------- | ------------------------------------------------------------------ |
| **Hiring**      | Skills, culture fit, growth potential, team dynamics               |
| **Technology**  | Scalability, maintainability, team expertise, cost, vendor risk    |
| **Pricing**     | Value delivered, competitive position, costs, customer willingness |
| **Partnership** | Strategic fit, capability complement, cultural alignment, terms    |
| **Investment**  | ROI, strategic value, opportunity cost, risk/reward                |
