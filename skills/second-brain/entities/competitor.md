# Entity: Competitor Profile

## Purpose

Competitor profiles document companies that compete in the same space. Each profile captures positioning, strengths, weaknesses, and differentiation. Competitor data feeds into strategic analysis and content differentiation.

## Storage

- **Path**: `{PROJECT_PATH}/competitors/{slug}.md` — one file per competitor
- **Type**: Collection (multiple per project)
- **Slug rule**: Lowercase, spaces to hyphens, strip non-alphanumeric except hyphens

## Template

Use the Competitor Profile template from `templates/competitor.md`.

**Required fields when creating**:

- Competitor name
- Website
- Core offering
- Target market
- Positioning
- Strengths (3+)
- Weaknesses (3+)
- Our differentiation

## Context

Read `{PROJECT_PATH}/context.md` before creating a competitor profile. This provides comparison context for the differentiation section.

## Research Enrichment

When creating a competitor, spawn `atlas:market_researcher` to gather real data before writing the profile:

```
subagent_type: atlas:market_researcher
prompt: "Research competitor: {competitor name}

Website: {url}

Find:
- What they offer (products, services, pricing if public)
- How they position themselves (tagline, messaging, target audience)
- Recent news or announcements
- Strengths and weaknesses based on reviews, press, community sentiment
- Market position and notable customers

Do NOT create any files or folders. Return your findings as text."
```

Merge the researcher's findings with what the user provided. Present the combined profile to the user for confirmation before saving — the user may disagree with or want to adjust the researcher's findings.

## Management

- **Create**: Read project context first. Ask for competitor name and website. Spawn `atlas:market_researcher` to enrich. Merge user input with research findings. Present for confirmation. Check if slug exists (offer overwrite or cancel). Create `competitors/` directory if needed. Write using template.
- **List**: Read all `.md` files in competitors directory. Display table: name, core offering, positioning, our differentiation.
- **Edit**: Find by name or slug. Show current values. Ask which sections to update. Preserve unchanged sections. Update `updated` timestamp.
- **Delete**: Confirm before deleting. Unlike themes, competitors are hard-deleted (no archive).

## Integration

- **Strategic analysis** (`business-strategy/workflows/analyze.md`): Competitor files are loaded explicitly and passed to the strategist agent
- **Content research** (`marketing-content/workflow/research.md`): Competitor positioning informs differentiation angles
- **Competitive framework** (`business-strategy/frameworks/competitive.md`): Analysis should pull from existing competitor profiles rather than asking from scratch
