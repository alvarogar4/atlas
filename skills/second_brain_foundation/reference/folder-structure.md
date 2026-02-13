# Knowledge Base Folder Structure

**This is the single source of truth** for the Atlas folder structure. All other skills reference this.

## Brain Root

```
{BRAIN_PATH}/
├── inbox/                      # Quick captures, unprocessed (default)
├── projects/                   # Active work with deadlines
│   └── {project-name}/         # See "Project Structure" below
├── areas/                      # Ongoing responsibilities (no deadline)
│   ├── {area-name}/            # Topic areas (health, finances, career, etc.)
│   │   ├── context.md
│   │   └── YYYY-MM-DD-{topic}.md
│   ├── decisions/              # Decision logs
│   │   └── YYYY-MM-DD-{topic}.md
│   └── reviews/                # Periodic reviews
│       ├── YYYY-WXX-weekly.md
│       ├── YYYY-MM-monthly.md
│       └── YYYY-QX-quarterly.md
├── resources/                  # Reference material, learnings
│   ├── market/                 # Market intelligence
│   │   └── YYYY-MM-DD-{topic}.md
│   └── strategy/               # Strategic analyses (non-project)
│       └── {topic}/
│           └── analysis.md
├── archives/                   # Completed/inactive items
└── .context/                   # Preferences, active project tracking
    └── active-project
```

## Project Structure

Each project under `projects/{project-name}/`:

```
{project-name}/
├── README.md                              # Project overview
├── context.md                             # Project context
├── strategy/                              # Business strategy
│   ├── strategy.md                        # Main strategy document
│   ├── [plans/]                           # Specific plans (on-demand)
│   └── [ideas/]                           # Ideas and explorations (on-demand)
├── competitors/                           # Competitor analysis
│   └── {competitor-slug}.md
└── marketing/
    ├── content/                           # Unified content workflow (topic-first)
    │   └── YYYY-MM-DD_{topic}/
    │       ├── 1_research.md              # Shared research
    │       ├── 2_plan.md                  # Shared content brief
    │       ├── 3_draft-{channel}.md       # Channel-specific draft
    │       ├── 4_review-{channel}.md      # Channel-specific review
    │       ├── 5_results-{channel}.md     # Channel-specific results
    │       └── resources/                 # Shared images, prompts
    ├── calendars/                         # Content calendars
    │   └── {year}-Q{n}.md
    ├── audiences/                         # Audience personas
    │   └── {persona-slug}.md
    ├── themes/                            # Content themes
    │   ├── {theme-slug}.md
    │   └── _archived/
    ├── brand-voice.md                     # Brand voice guidelines
    └── visual-identity.md                 # Visual identity
```

**Principle**: Business assets (context, strategy/, competitors/) at project root. Marketing assets inside `marketing/`.

## Directory Creation Commands

```bash
# Brain-level directories
mkdir -p {BRAIN_PATH}/{inbox,projects,areas,resources,archives,.context}
mkdir -p {BRAIN_PATH}/areas/{decisions,reviews}
mkdir -p {BRAIN_PATH}/resources/{market,strategy}

# Project-level directories (on-demand)
mkdir -p {PROJECT_PATH}/strategy
mkdir -p {PROJECT_PATH}/competitors
mkdir -p {PROJECT_PATH}/marketing
mkdir -p {PROJECT_PATH}/marketing/audiences
mkdir -p {PROJECT_PATH}/marketing/calendars
mkdir -p {PROJECT_PATH}/marketing/themes
mkdir -p {PROJECT_PATH}/marketing/themes/_archived
mkdir -p {PROJECT_PATH}/marketing/content
```

## File Naming Convention

```
YYYY-MM-DD-{kebab-case-topic}.md
```

## Frontmatter Template

```yaml
---
captured: 2024-12-16T14:30:00Z
type: {note|idea|decision|learning|reference|meeting|task|research}
tags: [tag1, tag2]
status: {inbox|active|someday|reference|archived}
project: {project-name if applicable}
area: {area-name if applicable}
related: [path/to/related-note.md]
---
```

## Categorization Guide

| If it has... | Put in... |
|-------------|----------|
| Deadline/deliverable | `projects/` |
| Ongoing responsibility | `areas/` |
| Reference value | `resources/` |
| Just captured | `inbox/` |
| Done/old | `archives/` |

## Operations

### Search Notes

```bash
# Content search
grep -ri "{query}" {BRAIN_PATH}/ --include="*.md" -l

# Tag search
grep -r "tags:.*{tag}" {BRAIN_PATH}/ --include="*.md" -l
```

### Recent Activity

```bash
# Modified this week
find {BRAIN_PATH}/ -name "*.md" -mtime -7
```

### Move/Organize

```bash
# Move from inbox to project
mv {BRAIN_PATH}/inbox/{file}.md {BRAIN_PATH}/projects/{project}/{file}.md

# Archive completed
mv {BRAIN_PATH}/projects/{project}/ {BRAIN_PATH}/archives/
```

## Tag Conventions

- Topics: `#architecture`, `#trading`, `#product`
- Types: `#idea`, `#decision`, `#learning`
- Status: `#urgent`, `#blocked`, `#review`
- Projects: `#project-name`
