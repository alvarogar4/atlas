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
│   │   ├── YYYY-MM-DD-{topic}.md
│   │   └── [decisions/]        # Area-scoped decisions (on-demand)
│   │       └── YYYY-MM-DD-{topic}.md
│   ├── decisions/              # General decision logs (not area-specific)
│   │   └── YYYY-MM-DD-{topic}.md
│   └── reviews/                # Personal periodic reviews
│       ├── YYYY-WXX-weekly.md
│       ├── YYYY-MM-monthly.md
│       ├── YYYY-QX-quarterly.md
│       └── YYYY-annual.md
├── resources/                  # Reference material, learnings
│   ├── market/                 # Market intelligence
│   │   └── YYYY-MM-DD-{topic}.md
│   └── strategy/               # Strategic analyses (non-project)
│       └── {topic}/
│           └── YYYY-MM-DD-analysis.md
├── .context/                   # Preferences, patterns
└── archives/                   # Completed/inactive items
```

## External Projects

Projects can also live outside the brain via per-project path variables:

```env
# In .env
ATLAS_PATH_OBSESSIONDB=/path/to/obsessiondb
ATLAS_PATH_GYMBROS=/path/to/gymbros
```

External project directories follow the same structure as `projects/{project-name}/`:

```
/path/to/external-project/
├── README.md
├── context.md
├── strategy/
├── competitors/
└── marketing/
    ├── content/
    ├── calendars/
    ├── audiences/
    ├── themes/
    ├── brand-voice.md
    └── visual-identity.md
```

**Brain-level PARA** (inbox, areas, resources, archives) always uses `ATLAS_BRAIN_PATH`, regardless of which project is active.

## Project Structure

Each project under `projects/{project-name}/`:

```
{project-name}/
├── README.md                              # Project overview
├── context.md                             # Project context
├── strategy/                              # Business strategy
│   ├── strategy.md                        # Main strategy document
│   ├── [plans/]                           # Specific plans (on-demand)
│   ├── [ideas/]                           # Ideas and explorations (on-demand)
│   ├── [{topic}/]                         # Topic folders (on-demand, from strategy workflows)
│   │   ├── YYYY-MM-DD-analysis.md         # Strategic analysis
│   │   └── YYYY-MM-DD-decision.md         # Decision about this topic
│   └── [reviews/]                         # Project-scoped reviews (on-demand)
│       ├── YYYY-QX-quarterly.md
│       └── YYYY-annual.md
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
type: { note|idea|decision|learning|reference|meeting|task|research }
tags: [tag1, tag2]
status: { inbox|active|someday|reference|archived }
project: { project-name if applicable }
area: { area-name if applicable }
related: [path/to/related-note.md]
---
```

## Categorization Guide

| If it has...           | Put in...    |
| ---------------------- | ------------ |
| Deadline/deliverable   | `projects/`  |
| Ongoing responsibility | `areas/`     |
| Reference value        | `resources/` |
| Just captured          | `inbox/`     |
| Done/old               | `archives/`  |

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

## Plugin-Level: Templates

Project asset templates live in the plugin source (not the brain):

```
skills/second_brain/templates/
├── readme.md           # Project README
├── context.md          # Project context
├── strategy.md         # Project strategy
├── brand-voice.md      # Brand voice guidelines
├── visual-identity.md  # Visual identity guidelines
├── audience.md         # Audience persona
├── competitor.md       # Competitor profile
├── calendar.md         # Content calendar
└── theme.md            # Content theme
```

## Plugin-Level: Foundation Definitions

Foundation definitions live in the plugin source (not the brain). They define how project-level foundational documents (context, strategy, brand voice, visual identity) are created and managed:

```
skills/second_brain/foundations/
├── context.md          # Project context definition
├── strategy.md         # Project strategy definition
├── brand-voice.md      # Brand voice definition
└── visual-identity.md  # Visual identity definition
```

## Plugin-Level: Entity Definitions

Entity definitions live in the plugin source (not the brain). They define how collection entities (themes, competitors, audiences, calendars) are managed:

```
skills/second_brain/entities/
├── project.md      # Project CRUD + link/unlink
├── theme.md        # Content theme CRUD
├── competitor.md   # Competitor profile CRUD
├── audience.md     # Audience persona CRUD
└── calendar.md     # Content calendar planning/viewing
```

These files define purpose, storage paths, templates, and management behavior. The AI handles operations from these definitions.

## Tag Conventions

- Topics: `#architecture`, `#trading`, `#product`
- Types: `#idea`, `#decision`, `#learning`
- Status: `#urgent`, `#blocked`, `#review`
- Projects: `#project-name`
