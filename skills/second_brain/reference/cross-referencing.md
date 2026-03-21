# Cross-Referencing Rules

**This is the single source of truth** for how brain files link to each other. All skills that create or update files must follow these rules.

## Why Cross-References Matter

1. **Agent discovery**: `locate_knowledge` and `analyze_knowledge` follow the `related` property to find connected files
2. **Graph navigation**: Obsidian renders `related` paths as edges in the graph view, forming navigable clusters

## The `related` Property

Every brain file should include a `related` property in frontmatter listing paths to connected files. Paths are **relative to the vault root** (the brain root).

```yaml
---
related:
  - /projects/personal-brand/marketing/brand-voice.md
  - /projects/personal-brand/marketing/audiences/technical-tim.md
  - /projects/personal-brand/marketing/calendars/2026-Q1.md
---
```

### What to link

Add paths to files that are **directly related** to the current file:

| File type                                         | Link to                                                    |
| ------------------------------------------------- | ---------------------------------------------------------- |
| Content pipeline files                            | Siblings in the same content folder, calendar entry, theme |
| Entity files (themes, audiences, competitors)     | Related entities, brand-voice, strategy                    |
| Foundation files (context, strategy, brand-voice) | Themes, audiences they reference                           |
| Calendar files                                    | Brand voice, content folders for scheduled entries         |
| Inbox captures                                    | Project context or area files if clearly related           |
| Results files                                     | Calendar, quarterly review, series siblings                |

### Rules

- Use vault-root paths starting with `/` (e.g., `/projects/personal-brand/context.md`)
- Always link to files, never to directories
- No bidirectional maintenance needed -- Obsidian shows incoming links in the backlinks panel automatically
- When creating a new file, populate `related` with known connections. No need to update other files to link back.
- When a file is renamed or moved, grep for its old path across the brain and update any `related` entries that reference it

## Tags

Simple, broad categories in frontmatter. No namespaces, no detailed hierarchies.

```yaml
tags: [marketing, strategy, decision, content]
```

Good tags: `marketing`, `strategy`, `decision`, `idea`, `learning`, `reference`, `content`, `competitor`, `audience`, `review`

Tags are for filtering and browsing, not for expressing relationships between files. Use `related` for that.

## Series Navigation (results files only)

Content series need explicit prev/next ordering, which `related` and tags can't express.

If content belongs to a named series, add a series line at the end of the results file:

```markdown
**Series**: {Series Name} | prev: [#N: Title](../YYYY-MM-DD_slug/5_results.md) | next: [#N: Title](../YYYY-MM-DD_slug/5_results.md)
```

Rules:

- Only in `5_results.md` (or `5_results-{channel}.md`)
- First entry has `next` only; last entry has `prev` only
- When adding a new series entry, update the previous entry's `next` link
