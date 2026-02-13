# Atlas - Personal Assistant & Second Brain

A Claude Code plugin that transforms Claude into a personal assistant with memory, marketing automation, and business strategy capabilities.

## Features

- **Knowledge Management** - PARA-based second brain with capture, recall, and search
- **Marketing Automation** - Campaign planning, content calendars, copywriting frameworks
- **Business Strategy** - SWOT, Porter's Five Forces, Business Model Canvas, OKRs, and more
- **Decision Support** - Structured decision logging with pre-mortems and prioritization

## Quick Start

```bash
# 1. Install the plugin
/install atlas

# 2. Initialize your knowledge base
/atlas:second_brain:foundation setup
```

After setup, Atlas works conversationally:
- "Save this idea: build a habit tracker CLI"
- "Research content about AI trends"
- "Analyze our market position using SWOT"
- "Weekly review"

## Plugin Structure

```
atlas/
├── agents/                                 # Flat structure with domain prefixes
│   ├── core_locate_knowledge.md            # Fast file discovery
│   ├── core_analyze_knowledge.md           # Deep analysis and synthesis
│   ├── marketing_content_reviewer.md       # Content QA
│   ├── marketing_market_researcher.md      # Market intelligence
│   └── business_strategist.md              # Framework-based analysis
├── skills/                                 # 4 consolidated skills
│   ├── second_brain_foundation/            # Core knowledge + project management (16 actions)
│   │   ├── SKILL.md                        # Config, capabilities, agent orchestration
│   │   ├── reference/                      # folder-structure.md, project-templates.md
│   │   ├── workflows/                      # setup, capture, search
│   │   └── project/                        # manage (CRUD), define (wizards)
│   ├── business_strategy/                  # Strategy + decisions (3 actions)
│   │   ├── SKILL.md                        # Framework selection, capabilities
│   │   ├── frameworks/                     # 12 frameworks (SWOT, Porter's, etc.)
│   │   ├── templates/                      # decision-log.md
│   │   └── workflows/                      # analyze, decision, review
│   ├── marketing_content/                  # Content lifecycle (11 actions)
│   │   ├── SKILL.md                        # Content lifecycle, state detection
│   │   ├── channels/                       # blog, linkedin, twitter, email, hackernews, social
│   │   ├── reference/                      # metrics.md, review-checklist.md
│   │   ├── workflow/                       # research, plan, write, review, results
│   │   ├── calendar/                       # plan, view
│   │   └── themes/                         # manage (add/list/edit/remove)
│   └── marketing_visuals/                  # Visual content creation
│       ├── SKILL.md                        # Decision tree, workflow chaining
│       ├── tools/                          # processing, schema-generation + assets
│       └── guides/                         # ai-prompting
├── hooks/
│   └── hooks.json                          # Event handlers
├── CLAUDE.md                               # Personality & behavior
└── README.md                               # This file
```

## Capabilities

### Knowledge Management (`second_brain_foundation`)
PARA-based personal knowledge base with 16 operations: capture ideas, search notes, deep recall with synthesis, create and manage projects, define project context/strategy/brand/visuals/audience/competitors.

### Content Creation (`marketing_content`)
Full content lifecycle with 11 operations: research, plan, write, review, results tracking, calendar planning, theme management. Supports 6 channels: blog, linkedin, twitter, email, hackernews, social.

Pipeline: research → plan → write → review → [publish] → results

### Business Strategy (`business_strategy`)
Strategic frameworks with 3 operations: analyze (12 frameworks), document decisions, periodic reviews (weekly/monthly/quarterly).

### Visual Content (`marketing_visuals`)
Internal skill for image processing, schema diagrams, and AI prompt composition.

## Strategic Frameworks Available

| Framework                 | Best For                  |
| ------------------------- | ------------------------- |
| **SWOT**                  | Current position analysis |
| **Porter's Five Forces**  | Industry dynamics         |
| **PESTEL**                | Macro environment         |
| **Value Chain**           | Internal operations       |
| **Business Model Canvas** | Business model design     |
| **Lean Canvas**           | Startup validation        |
| **Blue Ocean**            | Differentiation strategy  |
| **Jobs-to-be-Done**       | Customer needs            |
| **OKRs**                  | Goal setting and tracking |
| **Competitive Analysis**  | Competitor intelligence   |
| **Eisenhower Matrix**     | Task prioritization       |
| **ICE/RICE Scoring**      | Initiative prioritization |

## Knowledge Base Structure (PARA Method)

```
~/brain/
├── inbox/              # Quick captures, unsorted
├── projects/           # Active work with deadlines
│   └── {project-name}/ # Project silos
│       ├── README.md
│       ├── context.md
│       ├── strategy/
│       ├── competitors/
│       └── marketing/
│           ├── content/        # Topic-first content workflow
│           │   └── YYYY-MM-DD_{topic}/
│           ├── calendars/
│           ├── audiences/
│           ├── themes/
│           ├── brand-voice.md
│           └── visual-identity.md
├── areas/              # Ongoing responsibilities
│   ├── decisions/      # Decision logs
│   ├── reviews/        # Periodic reviews
│   └── strategy/       # Business strategy analysis
├── resources/          # Reference material
│   └── market/         # Market research
├── archives/           # Completed/inactive
└── .context/           # Preferences, patterns
```

## Agents

| Domain        | Agent               | Purpose                          |
| ------------- | ------------------- | -------------------------------- |
| **Core**      | `locate_knowledge`  | Fast file discovery (paths only) |
| **Core**      | `analyze_knowledge` | Deep analysis and synthesis      |
| **Marketing** | `market_researcher` | External market intelligence     |
| **Marketing** | `content_reviewer`  | Content quality assurance        |
| **Business**  | `strategist`        | Apply strategic frameworks       |

## Configuration

After running `/atlas:second_brain:foundation setup`, your brain path is stored in one of:
- `.env` file in your project (portable)
- `~/.claude/CLAUDE.md` (Claude Code-specific)

```
ATLAS_BRAIN_PATH=~/brain
ATLAS_ACTIVE_PROJECT=my-project
```

## Architecture (v2.0)

| Metric             | v1.9.1 (Jarvis) | v2.0.0 (Atlas) |
| ------------------ | ---------------- | --------------- |
| Commands           | 28               | 0               |
| Skills             | 21               | 4               |
| Agents             | 5                | 5               |
| Total components   | 54               | 9               |
| Indirection layers | 3                | 1               |

## Personality

Atlas is configured (in CLAUDE.md) to be:

- **Direct** - No fluff, get to the point
- **Future-focused** - Emphasize scalable solutions
- **Bilingual** - English default, Spanish (Spain) when you write in Spanish
- **Critical** - Prioritizes truth over agreement
- **Proactive** - Checks knowledge base, offers to capture learnings
