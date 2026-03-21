# Entity: Audience Persona

## Purpose

Audience personas define target user segments with their demographics, goals, pain points, and behavior. Personas inform content channel selection, messaging, and tone.

## Storage

- **Path**: `{PROJECT_PATH}/marketing/audiences/{slug}.md` — one file per persona
- **Type**: Collection (multiple per project)
- **Slug rule**: Lowercase, spaces to hyphens, strip non-alphanumeric except hyphens

## Template

Use the Audience Persona template from `templates/audience.md`.

**Required fields when creating**:

- Persona name (e.g., "Technical Tim")
- Demographics (role, company size/industry)
- Goals (3+)
- Pain points (3+)
- Where they hang out online
- Buying triggers
- Messaging that works (topics, tone)

## Context

Read `{PROJECT_PATH}/context.md` before creating a persona. This informs who the target audience is.

## Management

- **Create**: Read project context first. Gather required fields interactively. Check if slug exists (offer overwrite or cancel). Create `marketing/audiences/` directory if needed. Write using template. Populate `related` in frontmatter with paths to themes targeting this persona, other related personas, and brand-voice.md.
- **List**: Read all `.md` files in audiences directory. Display table: persona name, role, key goal, primary pain point.
- **Edit**: Find by name or slug. Show current values. Ask which sections to update. Preserve unchanged sections. Update `modified` date. Update `related` if related themes or personas changed.
- **Delete**: Confirm before deleting.

## Integration

- **Content planning** (`marketing_content/workflow/plan.md`): Audience personas inform channel selection and messaging alignment
- **Brand voice** (`marketing/brand-voice.md`): Personas reference brand voice for tone consistency
- **Calendar planning**: Personas help validate content relevance to target segments
