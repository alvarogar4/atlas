# Themes Management

Consolidated theme CRUD operations.

---

## Action: theme-add

### Setup
Execute **Setup** from SKILL.md.

### Process

1. **CHECKPOINT**: Gather theme details:

```
Adding theme: {name}

Please provide:
- Overview (1-2 sentences about this topic area):
- Target Audience (who is this content for):
- Channels (e.g., LinkedIn, Blog, Twitter):
- Objective (awareness|leads|conversions):
- Target Frequency (posts per month):
```

2. **CHECKPOINT**: Gather content guidelines:

```
Content Guidelines for: {name}

- Tone (e.g., practical, authoritative, conversational):
- Key Messages (3 bullet points):
- Do's (3-4 behaviors to encourage):
- Don'ts (3-4 behaviors to avoid):
```

3. Create themes directory if needed:

```bash
mkdir -p ${PROJECT_PATH}/marketing/themes
```

4. Generate slug:

```bash
SLUG=$(echo "{name}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
```

5. Check if theme exists → ask to overwrite or cancel.

6. Write theme file using template from `atlas:second_brain:foundation` → `reference/project-templates.md`.

### Output

```
Theme created: {name}
Path: marketing/themes/{slug}.md

Next steps:
- Plan quarterly content with this theme
- Start researching content for this theme

Want to do either of these now?
```

---

## Action: theme-list

### Setup
Execute **Setup** from SKILL.md.

### Process

1. Find all theme files:

```bash
ls ${PROJECT_PATH}/marketing/themes/*.md 2>/dev/null | grep -v '_archived'
```

2. Read each theme file and extract key fields.

3. Display summary:

```
Content Themes: {Project}

## Active Themes
| Theme | Objective | Frequency | Channels |
|-------|-----------|-----------|----------|
| {name} | {objective} | {n}/mo | {channels} |

## Theme Details

### {Theme 1}
- Overview: {overview}
- Target Audience: {audience}
- Frequency: {n}/month

## Archived
Run `ls ${PROJECT_PATH}/marketing/themes/_archived/` to see archived themes.
```

---

## Action: theme-edit

### Setup
Execute **Setup** from SKILL.md.

### Process

1. Find theme file by name or slug:

```bash
ls ${PROJECT_PATH}/marketing/themes/*{name}*.md 2>/dev/null
```

2. If not found, show available themes.

3. Read existing theme file and present current values.

4. **CHECKPOINT**: Ask which sections to update:

```
Which sections would you like to update?
1. Overview & Audience
2. Channels & Frequency
3. Content Guidelines (Tone, Messages, Do's/Don'ts)
4. Metrics
5. All sections
```

5. Gather new values for selected sections.

6. Update theme file, preserving unchanged sections.

7. Update the `updated` timestamp in frontmatter.

---

## Action: theme-remove

### Setup
Execute **Setup** from SKILL.md.

### Process

1. Find theme file by name or slug.

2. If not found, show available themes.

3. **CHECKPOINT**: Confirm archival:

```
Archive theme: {name}?

This will move the theme to marketing/themes/_archived/
The theme will be preserved but won't appear in active lists.

Confirm? (y/n)
```

4. Create archived directory and move:

```bash
mkdir -p ${PROJECT_PATH}/marketing/themes/_archived
mv ${PROJECT_PATH}/marketing/themes/{slug}.md ${PROJECT_PATH}/marketing/themes/_archived/{slug}.md
```

### Output

```
Theme archived: {name}
Location: marketing/themes/_archived/{slug}.md

To restore, move the file back to marketing/themes/
```
