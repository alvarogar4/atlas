# Entity: Content Theme

## Purpose

Content themes organize marketing content into topic areas. Each theme defines a content category with its target audience, channels, objectives, and content guidelines. Themes are the foundation for calendar planning and content strategy.

## Storage

- **Path**: `{PROJECT_PATH}/marketing/themes/{slug}.md` — one file per theme
- **Archive**: `{PROJECT_PATH}/marketing/themes/_archived/{slug}.md`
- **Type**: Collection (multiple per project)
- **Slug rule**: Lowercase, spaces to hyphens, strip non-alphanumeric except hyphens

## Template

Use the Content Theme template from `templates/theme.md`.

**Required fields when creating**:

- Overview (1-2 sentence description)
- Target audience
- Channels (mark primary)
- Objective (awareness | leads | conversions | retention)
- Content guidelines: tone, key messages (3), frequency target

## Management

- **Create**: Gather required fields interactively. Check if slug already exists (offer overwrite or cancel). Create `marketing/themes/` directory if needed. Write using template.
- **List**: Read all `.md` files in themes directory, excluding `_archived/`. Display table: name, objective, frequency, channels.
- **Edit**: Find theme by name or slug (fuzzy match). Show current values. Ask which sections to update. Preserve unchanged sections. Update `updated` timestamp in frontmatter.
- **Archive**: Confirm before moving. Move file to `_archived/` subdirectory. File is preserved, just hidden from active lists.
- **Restore**: Move back from `_archived/` to themes directory.

## Integration

- **Content research** (`marketing_content/workflow/research.md`): Reads themes to match topics against theme guidelines and keywords
- **Calendar planning** (`marketing_content/calendar/plan.md`): Reads themes for coverage analysis and balance visualization
- **Content writing**: References theme tone and key messages for voice consistency
