# Calendar Template

Template for quarterly content calendars.

## Content Calendar Template

**Path**: `{PROJECT_PATH}/marketing/calendars/{year}-Q{n}.md`

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

**Goal**: {high-level goal}

**Success Criteria**:
- [ ] {measurable target 1}
- [ ] {measurable target 2}

## Scheduled Content

| Week | Date | Content | Type | Theme | Objective | References | Status |
|------|------|---------|------|-------|-----------|------------|--------|
| W1 | {date} | {title} | Blog | {theme} | {objective} | competitors/acme.md | Planned |
| W2 | {date} | {title} | LinkedIn | {theme} | {objective} | audiences/technical-tim.md | Planned |
| W3 | {date} | {title} | Blog | {theme} | {objective} | | Planned |
```
