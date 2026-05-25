# Knowledge Base Folder Structure

**This is the default Atlas folder structure** — the fallback used when a project does not pin its own. All other skills reference this.

> [!important] A project's `STRUCTURE.md` overrides this document.
> If the active project has a `STRUCTURE.md` at its root (`{PROJECT_PATH}/STRUCTURE.md`), that file is **authoritative** for that project's folder layout, file naming, frontmatter, and cross-link style. Use this document only as the fallback for whatever the project's `STRUCTURE.md` does not specify. See `SKILL.md` → Config → [Project Structure Spec](../SKILL.md#project-structure-spec).

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

## Git Isolation

Projects that need their own git history (e.g., client projects, open-source work) can have a separate git repo inside their `projects/{name}/` folder. Add the project folder to the brain's `.gitignore`:

```gitignore
# In {BRAIN_PATH}/.gitignore
projects/obsessiondb/
projects/client-project/
```

These projects are managed identically to any other project — the only difference is git tracking.

**Brain-level PARA** (inbox, areas, resources, archives) always uses `ATLAS_BRAIN_PATH`, regardless of which project is active.

## Project Structure

Each project under `projects/{project-name}/`:

```
{project-name}/
├── README.md                              # Project overview
├── dashboard.base                         # Obsidian Bases project dashboard
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
    │       ├── 0_context.md               # Angle, constraints, framing
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
created: 2024-12-16
modified: 2024-12-16
tags: [marketing, idea]
project: project-name
related:
  - /projects/project-name/context.md
  - /projects/project-name/marketing/brand-voice.md
---
```

Content pipeline files add `topic` to group files for the same piece:

```yaml
---
created: 2024-12-16
modified: 2024-12-16
tags: [marketing, content]
project: project-name
topic: clickhouse-deep-dive
related:
  - /projects/project-name/marketing/content/2024-12-16_clickhouse-deep-dive/0_context.md
  - /projects/project-name/marketing/calendars/2024-Q4.md
---
```

See `reference/cross-referencing.md` for what to link in `related` and tag guidelines.

## Categorization Guide

| If it has...           | Put in...    |
| ---------------------- | ------------ |
| Deadline/deliverable   | `projects/`  |
| Ongoing responsibility | `areas/`     |
| Reference value        | `resources/` |
| Just captured          | `inbox/`     |
| Done/old               | `archives/`  |

## Operations

Try Obsidian CLI first (faster, uses vault index). Fall back to file operations if Obsidian isn't running. See `reference/obsidian.md` for full CLI reference.

### Search Notes

```bash
# Obsidian CLI (preferred)
obsidian search query="{query}" limit=10
obsidian tags sort=count counts
obsidian backlinks file="{note}"

# File fallback
grep -ri "{query}" {BRAIN_PATH}/ --include="*.md" -l
grep -r "tags:.*{tag}" {BRAIN_PATH}/ --include="*.md" -l
```

### Read & Append Notes

```bash
# Obsidian CLI (preferred)
obsidian read file="{note}"
obsidian append file="{note}" content="{content}"

# File fallback
cat {BRAIN_PATH}/path/to/{note}.md
```

### Daily Notes

```bash
obsidian daily:read
obsidian daily:append content="- [ ] {task}"
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

Broad categories. Hierarchical tags via `/` are supported for sub-categorization:

- Topics: `#marketing`, `#strategy`, `#architecture`, `#trading`
- Types: `#idea`, `#decision`, `#learning`, `#reference`
- Status: `#urgent`, `#blocked`, `#review`
- Projects: `#project/obsessiondb`, `#project/gymbros`
- Content: `#content/blog`, `#content/linkedin`
- `architecture`, `trading`, `product`
