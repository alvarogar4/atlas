# Obsidian Features Reference

**This is the reference** for Obsidian-specific features available in brain notes. All notes remain standard markdown-compatible; these features enhance the experience when viewing in Obsidian.

## Link Format

Atlas uses **standard relative markdown links** exclusively:

```markdown
[Display Text](../relative/path/to/file.md)
```

Obsidian also supports wikilinks (`[[Note]]`) but we only use them in one place: the frontmatter `related` property (`- "[[path/to/file.md]]"`). Obsidian's graph engine only creates edges from wikilinks, so plain paths in YAML are invisible to the graph. Everywhere else (body text, series navigation), standard markdown links are used for portability.

## Callouts

Callouts render as styled blockquotes in Obsidian and as regular blockquotes elsewhere. Use them to highlight key information in notes.

```markdown
> [!note]
> Basic informational callout.

> [!important] Key Deadline
> The first milestone is due on January 30th.

> [!warning]
> This constraint cannot be violated.

> [!tip]
> Practical advice or shortcut.

> [!example]
> Concrete illustration of a concept.

> [!question]
> Open question to revisit later.

> [!faq]- Collapsed by default
> Foldable callout (- collapsed, + expanded).
```

### Callout Types

| Type | Use in brain notes |
|------|-------------------|
| `note` | General context, background info |
| `important` | Key decisions, deadlines, constraints |
| `warning` | Risks, things to avoid, blockers |
| `tip` | Practical advice, shortcuts |
| `example` | Concrete illustrations |
| `question` | Open questions, things to revisit |
| `todo` | Action items |
| `success` | Wins, validated assumptions |
| `failure` | Failed experiments, lessons learned |
| `quote` | External quotes with attribution |
| `abstract` | Executive summaries, TLDRs |
| `bug` | Known issues, things to fix |

### Nesting Callouts

```markdown
> [!question] Should we expand to enterprise?
> Analysis needed.
>
> > [!tip] Prior art
> > See the 2025 Q2 strategy review for market sizing.
```

## Embeds

Embed content from other notes inline. Uses standard `![[]]` syntax:

```markdown
![[Note Name]]                         Embed full note
![[Note Name#Heading]]                 Embed specific section
![[image.png]]                         Embed image
![[image.png|300]]                     Embed image with width
![[document.pdf#page=3]]               Embed PDF page
```

Useful for:
- Embedding strategy summaries into project READMEs
- Showing competitor overviews in content research
- Inlining visual assets from `resources/` folders

## Highlights

Mark important text with highlight syntax:

```markdown
This is ==highlighted text== that stands out in Obsidian.
```

Use for key findings in research notes, critical constraints in context docs, or important metrics in strategy files.

## Comments

Hide internal notes that shouldn't appear in reading view:

```markdown
This is visible %%but this is hidden%% text.

%%
Internal note: revisit this after Q2 review.
This entire block is hidden in reading view.
%%
```

Use for: internal reminders, draft notes within published content, temporary annotations.

## Properties (Frontmatter)

Atlas already uses YAML frontmatter extensively. These Obsidian-specific properties enhance vault navigation:

```yaml
---
tags:
  - project
  - active
aliases:
  - Alternative Name
  - Short Name
cssclasses:
  - custom-class
---
```

| Property | Purpose |
|----------|---------|
| `tags` | Searchable labels (Atlas already uses these) |
| `aliases` | Alternative names for the note; Obsidian suggests these in link autocomplete |
| `cssclasses` | Apply custom CSS styling to specific notes |

### Tag Syntax

Tags support hierarchy via forward slashes:

```markdown
#project/obsessiondb          Nested tag
#status/active                Status hierarchy
#content/blog                 Content type hierarchy
```

Tags in frontmatter (array format) and inline (`#tag`) are both searchable.

## Obsidian CLI

Interact with Obsidian vaults via the `obsidian` command when Obsidian is running. Provides faster search and richer operations than raw file access.

### Prerequisites

- Obsidian must be open
- The `obsidian` CLI must be installed
- Falls back to standard file operations (grep, read) if unavailable

### Key Commands

```bash
# Read a note
obsidian read file="My Note"

# Search vault content (faster than grep, uses Obsidian's index)
obsidian search query="search term" limit=10

# Create a note
obsidian create name="New Note" content="# Hello" silent

# Append to a note
obsidian append file="My Note" content="New line"

# Daily notes
obsidian daily:read
obsidian daily:append content="- [ ] New task"

# Properties
obsidian property:set name="status" value="done" file="My Note"

# Tags and backlinks
obsidian tags sort=count counts
obsidian backlinks file="My Note"
```

### Vault Targeting

```bash
# Target a specific vault (defaults to most recently focused)
obsidian vault="My Vault" search query="test"
```

### CLI vs File Operations

| Operation | Obsidian CLI | File Fallback |
|-----------|-------------|---------------|
| Search | `obsidian search query="X"` | `grep -ri "X" {BRAIN_PATH}/ --include="*.md"` |
| Read | `obsidian read file="X"` | `cat {BRAIN_PATH}/path/to/X.md` |
| Append | `obsidian append file="X" content="Y"` | Append to file directly |
| Tags | `obsidian tags sort=count` | `grep -r "tags:.*" {BRAIN_PATH}/` |
| Backlinks | `obsidian backlinks file="X"` | `grep -r "X" {BRAIN_PATH}/ --include="*.md"` |
| Daily | `obsidian daily:read` | Find today's daily note file |

Try the CLI command first. If it fails (Obsidian not running, CLI not installed), fall back to file operations silently.

## Defuddle (Web Content Extraction)

Extract clean markdown from web pages, stripping navigation, ads, and clutter:

```bash
# Extract clean markdown from a URL
defuddle parse <url> --md

# Get JSON output with metadata
defuddle parse <url> --json

# Save to file
defuddle parse <url> --md -o output.md

# Extract specific metadata
defuddle parse <url> -p title,description,domain
```

Preferred over WebFetch for standard web pages (articles, docs, blog posts). Falls back to WebFetch for SPAs, auth-gated content, or pages defuddle can't parse.

## References

- [Obsidian Flavored Markdown](https://help.obsidian.md/obsidian-flavored-markdown)
- [Callouts](https://help.obsidian.md/callouts)
- [Embed files](https://help.obsidian.md/embeds)
- [Properties](https://help.obsidian.md/properties)
- [Obsidian CLI](https://help.obsidian.md/cli)
