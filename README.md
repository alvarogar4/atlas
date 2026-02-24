# Atlas - Personal Assistant & Second Brain

A Claude Code plugin that transforms Claude into a personal assistant with memory, marketing automation, and business strategy capabilities.

## Features

- **Knowledge Management** - PARA-based second brain with capture, recall, and search
- **Marketing Automation** - Campaign planning, content calendars, copywriting frameworks
- **Business Strategy** - SWOT, Porter's Five Forces, Business Model Canvas, OKRs, and more
- **Decision Support** - Structured decision logging with pre-mortems and prioritization
- **Content Humanization** - 29 anti-patterns to detect and remove AI writing fingerprints
- **Translation** - Context-aware bilingual translation with 18 quality patterns

## Quick Start

```bash
# 1. Install the plugin
/install atlas

# 2. Initialize your knowledge base
/atlas:second_brain setup
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
│   ├── locate_knowledge.md                 # Fast file discovery
│   ├── analyze_knowledge.md                # Deep analysis and synthesis
│   ├── marketing_content_reviewer.md       # Content QA
│   ├── marketing_market_researcher.md      # Market intelligence
│   └── business_strategist.md              # Framework-based analysis
├── skills/                                 # 6 skills
│   ├── second_brain/                       # Core knowledge + project management
│   │   ├── SKILL.md                        # Config, capabilities, agent orchestration
│   │   ├── reference/                      # folder-structure.md
│   │   ├── templates/                      # Project asset templates (9 files)
│   │   ├── entities/                       # Entity definitions (project, theme, competitor, audience, calendar)
│   │   ├── foundations/                     # Project foundations (context, strategy, brand-voice, visual-identity)
│   │   └── workflows/                      # setup, capture, search
│   ├── business_strategy/                  # Strategy + decisions (3 actions)
│   │   ├── SKILL.md                        # Framework selection, capabilities
│   │   ├── frameworks/                     # 12 frameworks (SWOT, Porter's, etc.)
│   │   ├── templates/                      # analysis, decision, review
│   │   └── workflows/                      # analyze, decision, review
│   ├── marketing_content/                  # Content lifecycle
│   │   ├── SKILL.md                        # Content lifecycle, state detection
│   │   ├── channels/                       # blog, linkedin, twitter, email, hackernews, social
│   │   ├── reference/                      # metrics.md, review-checklist.md
│   │   ├── workflow/                       # research, plan, write, review, results, status
│   │   └── calendar/                       # plan, view
│   ├── marketing_visuals/                  # Visual content creation
│   │   ├── SKILL.md                        # Decision tree, workflow chaining
│   │   ├── tools/                          # processing, schema-generation + assets
│   │   └── guides/                         # ai-prompting
│   ├── humanizer/                          # AI writing pattern detection (29 anti-patterns)
│   │   └── SKILL.md                        # Zero-tolerance checklist, generation constraints
│   └── translator/                         # Context-aware bilingual translation (18 patterns)
│       └── SKILL.md                        # Translation quality patterns, voice preservation
├── hooks/
│   └── hooks.json                          # Event handlers
├── CLAUDE.md                               # Personality & behavior
└── README.md                               # This file
```

## Capabilities

### Knowledge Management (`second_brain`)

PARA-based personal knowledge base: capture ideas, search notes, deep recall with synthesis. Manage projects with foundations (context, strategy, brand voice, visual identity) and entities (themes, competitors, audiences, calendars).

### Content Creation (`marketing_content`)

Full content lifecycle: research, plan, write, review, results tracking, status overview, calendar planning. Supports 6 channels: blog, linkedin, twitter, email, hackernews, social.

Pipeline: research → plan → write → review → [publish] → results

### Business Strategy (`business_strategy`)

Strategic frameworks with 3 operations: analyze (12 frameworks), document decisions, periodic reviews (weekly/monthly/quarterly/annual).

### Visual Content (`marketing_visuals`)

Internal skill for image processing, schema diagrams, and AI prompt composition.

### Content Humanization (`humanizer`)

AI writing pattern detection with 29 anti-patterns. Loaded as generation constraints during content writing and verified during review. Covers content patterns, language/grammar, style, communication tone, filler/hedging, and structural uniformity.

### Translation (`translator`)

Context-aware bilingual translation with 18 quality patterns. Prevents literal translation, false friends, calques, and other common translation errors. Default pair: English <> Spanish (Spain).

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
│   └── reviews/        # Periodic reviews
├── resources/          # Reference material
│   ├── market/         # Market research
│   └── strategy/       # Business strategy analysis
├── archives/           # Completed/inactive
└── .context/           # Preferences, patterns
```

## Agents

| Domain        | Agent                     | Purpose                          |
| ------------- | ------------------------- | -------------------------------- |
| **Core**      | `atlas:locate_knowledge`  | Fast file discovery (paths only) |
| **Core**      | `atlas:analyze_knowledge` | Deep analysis and synthesis      |
| **Marketing** | `atlas:market_researcher` | External market intelligence     |
| **Marketing** | `atlas:content_reviewer`  | Content quality assurance        |
| **Business**  | `atlas:strategist`        | Apply strategic frameworks       |

## Configuration

After running `/atlas:second_brain setup`, your brain path is stored in:

- `.env` file in your project

```
ATLAS_BRAIN_PATH=~/brain
ATLAS_ACTIVE_PROJECT=my-project
```

## Personality

Atlas is configured (in CLAUDE.md) to be:

- **Direct** - No fluff, get to the point
- **Future-focused** - Emphasize scalable solutions
- **Bilingual** - English default, Spanish (Spain) when you write in Spanish
- **Critical** - Prioritizes truth over agreement
- **Proactive** - Checks knowledge base, offers to capture learnings
