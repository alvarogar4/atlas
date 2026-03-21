# Cross-Referencing Rules

**This is the single source of truth** for how brain files link to each other. All skills that create or update files must follow these rules.

## Why Cross-References Matter

Cross-references serve two purposes:

1. **Agent discovery**: `locate_knowledge` and `analyze_knowledge` can follow links to find related context without relying solely on grep/glob
2. **Graph navigation**: Tools like Obsidian render connected files as navigable clusters; unlinked files appear as isolated dots

## Core Principle

**Every file must link to all related files it knows about.** Links are bidirectional: if A links to B, B should link back to A. When creating or updating any file, scan for related files and establish connections in both directions.

## Link Syntax

All links use relative markdown paths:

```markdown
[Display Text](../relative/path/to/file.md)
```

Multiple links on one line use pipe separators:

```markdown
**See also**: [research](1_research.md) | [plan](2_plan.md) | [draft blog](3_draft-blog.md)
```

## Patterns by File Type

### Content Pipeline Files (within a content folder)

Every pipeline file (`0_context.md`, `1_research.md`, `2_plan.md`, `3_draft-*.md`, `4_review-*.md`, `5_results-*.md`) gets a footer linking to all sibling files:

```markdown
---
**See also**: [context](0_context.md) | [research](1_research.md) | [plan](2_plan.md) | [draft linkedin](3_draft-linkedin.md) | [results](5_results.md) | [resources](resources/index.md)
```

Rules:
- Each file lists all siblings **except itself**
- Use human-readable display names: `[draft linkedin]`, `[review blog]`, `[results twitter]`
- Always include `[resources](resources/index.md)` as the last entry
- `5_results*.md` files additionally link upward to the calendar and quarterly review:

```markdown
**See also**: [research](1_research.md) | ... | [calendar](../../calendars/2026-Q1.md) | [Q1 review](../../../strategy/reviews/2026-Q1-quarterly.md) | [resources](resources/index.md)
```

**When to add**: After saving any pipeline file, append the footer. When saving a new file to an existing folder, also update the "See also" lines in all existing siblings to include the new file.

### Series Navigation (results files only)

If content belongs to a named series (e.g., "ClickHouse Deep Dive"), add a series line before the "See also" footer:

```markdown
- **Series**: {Series Name} | prev: [#N: Title](../YYYY-MM-DD_slug/5_results.md) | next: [#N: Title](../YYYY-MM-DD_slug/5_results.md)
```

Rules:
- Only in `5_results.md` (or `5_results-{channel}.md`)
- Links point to sibling content folders' results files
- First entry has `next` only; last entry has `prev` only
- When adding a new series entry, update the previous entry's `next` link

### Calendar Files

Each week block in a calendar should end with a `**Content**:` line linking to the content folders scheduled for that week:

```markdown
**Content**: [Topic display](../content/YYYY-MM-DD_slug/) | [Another topic](../content/YYYY-MM-DD_slug/)
```

Rules:
- Link to the content folder (directory), not to a specific file inside it
- Use the topic as display text
- Add links when content folders exist; for planned-but-not-started entries, add the link once the content folder is created
- Also add header-level references to foundation docs:

```markdown
**Brand voice**: [brand-voice.md](../brand-voice.md)
```

### Entity Files (themes, audiences, competitors)

Each entity file gets a `## Related` section at the bottom linking to related entities and foundation docs:

**Themes** link to:
- Target audience personas: `[Persona Name](../audiences/slug.md)`
- Brand voice: `[brand-voice.md](../brand-voice.md)`
- Related strategy docs (if applicable)

**Audiences** link to:
- Themes that target them: `[Theme Name](../themes/slug.md)`
- Other related personas: `[Persona Name](slug.md)`
- Brand voice: `[brand-voice.md](../brand-voice.md)`

**Competitors** link to:
- Strategy docs that reference them
- Content that covers them

Format:

```markdown
## Related

- **Theme**: [Data Engineering](../themes/data-engineering.md)
- **Brand voice**: [brand-voice.md](../brand-voice.md)
```

**When to add**: During Create and Edit operations. When creating a new entity, also update the `## Related` sections of any files that should link back to it.

### Foundation Files (context, strategy, brand-voice, visual-identity)

Foundation files link to themes and audiences inline where they reference them, and maintain a reference section linking to all related config files:

**Brand voice** links to themes inline where it describes content pillars:

```markdown
1. **Data Engineering** — Description... [Link](./themes/data-engineering.md)
```

### Resource Index Files

Each content folder's `resources/` directory must have an `index.md` listing all resource files:

```markdown
# Resources

- [filename.png](filename.png)
- [prompt-hero.md](prompt-hero.md)
```

**When to create**: When creating the content folder (during the context step). Update whenever new resources are added.

## The Bidirectional Rule

When adding a link from A to B, always check if B already links back to A. If not, add the reverse link. This applies to:

- Theme ↔ Audience
- Theme ↔ Brand voice
- Audience ↔ Brand voice
- Calendar ↔ Content folder
- Results ↔ Calendar
- Results ↔ Quarterly review
- Content ↔ Series siblings

## Updating Cross-References

When renaming, moving, or deleting a file:

1. Find all files that link to the old path (grep for the filename)
2. Update or remove those links
3. This prevents stale references

## Unpublished Content

Content folders without a results file yet still need an outward connection. The calendar's `**Content**:` link to their folder serves this purpose. If no calendar entry exists either, add a link from `0_context.md` to the calendar where the content is scheduled.
