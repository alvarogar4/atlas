# Entity: Content Calendar

## Purpose

Content calendars define publishing plans with phase objectives, scheduled content, and theme balance. Each entry can reference specific project files (competitors, audiences) that should be loaded when working on that content piece.

## Storage

- **Path**: `{PROJECT_PATH}/marketing/calendars/{year}-Q{n}.md` — one file per period
- **Type**: Collection (keyed by year-period)
- **Default cadence**: Quarterly (recommended). The user can change to monthly (`{year}-{MM}.md`) or annual (`{year}.md`) based on their publishing volume.

## Template

Use the Content Calendar template from `templates/calendar.md`.

**Required fields when creating**:

- Period (auto-detect current or next quarter by default; ask user if they prefer a different cadence)
- Phase objective (high-level goal for the period)
- Success criteria (2-3 measurable targets)
- Scheduled content entries (week, date, title, type, theme, objective, references)

**The `References` column** specifies project files to load when working on that content entry:

- Competitor files: `competitors/{name}.md` -- load when the post involves differentiation or competitive positioning
- Audience files: `audiences/{name}.md` -- load to understand the ideal reader for this piece
- Strategy file: `strategy/strategy.md` -- loaded automatically during calendar planning, not per-entry
- Leave empty when no specific context is needed beyond defaults

Examples:

- A post comparing your approach vs a competitor: `competitors/acme.md`
- A post targeting a specific persona: `audiences/technical-tim.md`
- A post targeting a persona with competitor context: `competitors/acme.md, audiences/technical-tim.md`

## Calendar Planning Flow

Calendar planning is more than CRUD. The planning process:

1. **Period determination**: Default to quarterly. If current quarter has <30 days remaining, target next quarter. Ask user if they prefer a different cadence (monthly, annual).
2. **Load strategy**: Read `{PROJECT_PATH}/strategy/strategy.md` to align calendar objectives with strategic goals.
3. **Survey existing content**: List all content folders and their pipeline status (research/plan/draft/review/results).
4. **Read themes**: Load all active themes for coverage analysis.
5. **Check existing calendar**: Read calendar file for target quarter if it exists.
6. **Analyze gaps**: Identify weeks without planned content, themes below target frequency, and scheduling conflicts.
7. **Gather objectives**: Ask user for phase objective and success criteria.
8. **For each entry, ask about references**: Which competitor or audience files are relevant to this piece? List available files from `competitors/` and `audiences/` directories.
9. **Write calendar**: Save using template with References column populated.

See `marketing_content/calendar/plan.md` for the full planning flow.

## Calendar Viewing

Read the current quarter's calendar and themes. Display:

- Monthly overview (campaigns, posts, primary theme per month)
- Theme balance visualization (actual vs target frequency)
- Upcoming content (next 30 days)
- Gaps (weeks without content, themes below target)

See `marketing_content/calendar/view.md` for the view flow.

## Management

- **Create/Update**: Use the planning flow above. Overwrites existing calendar for the same quarter.
- **View**: Use the viewing flow above.
- **List**: Show all calendar files across quarters with a summary line per quarter (content count, phase objective).

## Integration

- **Content research** (`marketing_content/workflow/research.md`): Reads calendar for phase objectives, per-post objectives, AND referenced files (competitors/audiences for this specific entry)
- **Content planning** (`marketing_content/workflow/plan.md`): Reads referenced audience files to inform channel selection and messaging
- **Theme management**: Calendars reference themes for content categorization and balance tracking
