# Obsidian Bases Reference

**This is the reference** for creating Obsidian Bases (`.base` files) that provide database-like views of brain notes. Bases use YAML and sit alongside regular notes without modifying them.

## What Bases Are

A `.base` file creates filtered, sorted, computed views over your notes. Think of them as saved queries with a visual table/card/list UI in Obsidian. They read note properties (frontmatter) and file metadata to build dynamic views.

## When to Use

| Scenario | Base provides |
|----------|--------------|
| Project dashboard | Content pipeline status, recent activity, task overview |
| Content tracking | Drafts by channel, review status, publication dates |
| Competitor overview | All competitors with positioning and status |
| Inbox triage | Recent captures sorted by date, filterable by type |

## Schema

```yaml
filters:                    # Which notes to include
  and: []                   # All conditions must match
  or: []                    # Any condition can match
  not: []                   # Exclude matching notes

formulas:                   # Computed properties
  name: 'expression'

properties:                 # Display customization
  property_name:
    displayName: "Label"

views:                      # One or more visual layouts
  - type: table | cards | list
    name: "View Name"
    limit: 10               # Optional: cap results
    order:                   # Properties to show
      - file.name
      - property_name
      - formula.name
    groupBy:                 # Optional: group by property
      property: status
      direction: ASC
    summaries:               # Optional: aggregate values
      property: Average
```

## Filter Syntax

```yaml
# Single condition
filters: 'status == "active"'

# AND — all must be true
filters:
  and:
    - file.hasTag("project")
    - 'status != "archived"'

# OR — any can be true
filters:
  or:
    - file.hasTag("blog")
    - file.hasTag("linkedin")

# NOT — exclude
filters:
  not:
    - file.hasTag("archived")

# Nested
filters:
  and:
    - file.hasTag("content")
    - or:
        - 'type == "draft"'
        - 'type == "review"'
```

### Filter Functions

| Function | Example |
|----------|---------|
| `file.hasTag("x")` | Note has tag #x |
| `file.hasLink("x")` | Note links to "x" |
| `file.inFolder("x")` | Note is in folder x |

### Operators

`==`, `!=`, `>`, `<`, `>=`, `<=`, `&&`, `||`, `!`

## Properties

### Note Properties (from frontmatter)

Reference directly by name: `status`, `type`, `tags`, `project`, `captured`

### File Properties

| Property | Type | Description |
|----------|------|-------------|
| `file.name` | String | File name |
| `file.basename` | String | Name without extension |
| `file.path` | String | Full path |
| `file.folder` | String | Parent folder |
| `file.ext` | String | Extension |
| `file.size` | Number | Size in bytes |
| `file.ctime` | Date | Created time |
| `file.mtime` | Date | Modified time |
| `file.tags` | List | All tags |
| `file.backlinks` | List | Files linking to this |

## Formulas

```yaml
formulas:
  # Days since captured
  age: '(now() - file.ctime).days'

  # Status with icon
  status_icon: 'if(status == "active", "🟢", if(status == "draft", "🟡", "⚪"))'

  # Date formatting
  created: 'file.ctime.format("YYYY-MM-DD")'

  # Days until deadline
  days_left: 'if(deadline, (date(deadline) - today()).days, "")'

  # Word estimate
  words: '(file.size / 5).round(0)'
```

### Key Functions

| Function | Description |
|----------|-------------|
| `date(string)` | Parse string to date |
| `now()` | Current date and time |
| `today()` | Current date (00:00) |
| `if(cond, true, false?)` | Conditional |
| `duration(string)` | Parse duration |

### Duration Handling

Date subtraction returns a Duration, not a number. Access fields first:

```yaml
# CORRECT
"(now() - file.ctime).days"
"(date(due) - today()).days.round(0)"

# WRONG — Duration doesn't support direct math
"(now() - file.ctime).round(0)"
```

## Summary Functions

| Name | Input | Description |
|------|-------|-------------|
| `Average` | Number | Mean |
| `Sum` | Number | Total |
| `Min` / `Max` | Number | Extremes |
| `Median` | Number | Middle value |
| `Earliest` / `Latest` | Date | Date extremes |
| `Filled` / `Empty` | Any | Count non-empty / empty |
| `Unique` | Any | Count distinct values |

## Default Project Dashboard Template

Auto-generated when creating a project. Placed at `{PROJECT_PATH}/dashboard.base`.

```yaml
filters:
  and:
    - 'file.ext == "md"'

formulas:
  age: '(now() - file.mtime).days'
  status_label: 'if(status == "active", "🟢 Active", if(status == "draft", "🟡 Draft", if(status == "inbox", "📥 Inbox", if(status == "archived", "📦 Archived", "⚪ Other"))))'
  words: '(file.size / 5).round(0)'

properties:
  formula.status_label:
    displayName: "Status"
  formula.age:
    displayName: "Days Ago"
  formula.words:
    displayName: "~Words"

views:
  - type: table
    name: "Recent Activity"
    limit: 20
    order:
      - file.name
      - type
      - formula.status_label
      - formula.age
      - formula.words
    filters:
      not:
        - file.inFolder("archives")

  - type: table
    name: "Content Pipeline"
    filters:
      and:
        - file.inFolder("marketing/content")
    order:
      - file.folder
      - file.name
      - type
      - file.mtime

  - type: table
    name: "Strategy & Competitors"
    filters:
      or:
        - file.inFolder("strategy")
        - file.inFolder("competitors")
    order:
      - file.name
      - type
      - formula.status_label
      - file.mtime
```

## On-Demand Base Examples

### Inbox Triage

```yaml
filters:
  and:
    - file.inFolder("inbox")

formulas:
  age: '(now() - file.ctime).days'

views:
  - type: table
    name: "Inbox"
    order:
      - file.name
      - type
      - tags
      - formula.age
```

### Content by Channel

```yaml
filters:
  and:
    - file.inFolder("marketing/content")
    - '/^3_draft/.matches(file.basename)'

formulas:
  channel: 'file.basename.replace("3_draft-", "")'

views:
  - type: cards
    name: "Drafts"
    order:
      - file.folder
      - formula.channel
      - file.mtime
```

## Embedding Bases

Embed a base view inside a regular note:

```markdown
![[dashboard.base]]

<!-- Specific view -->
![[dashboard.base#Content Pipeline]]
```

## YAML Quoting Rules

- Single quotes for formulas containing double quotes: `'if(done, "Yes", "No")'`
- Double quotes for simple strings: `"My View"`
- Escape nested quotes properly

## Troubleshooting

- **YAML syntax error**: Check for unquoted special characters (`:`, `#`, `[`, `]`)
- **Duration math error**: Access `.days`/`.hours` before calling `.round()`
- **Missing formula**: Every `formula.X` in `order` needs a matching `formulas:` entry
- **Null property crash**: Guard with `if()`: `'if(due, (date(due) - today()).days, "")'`

## References

- [Bases Syntax](https://help.obsidian.md/bases/syntax)
- [Functions](https://help.obsidian.md/bases/functions)
- [Views](https://help.obsidian.md/bases/views)
