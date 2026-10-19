# Atlas - Personal Assistant & Second Brain

A personal assistant with memory, marketing automation, and business strategy capabilities. Ships as a Claude Code plugin and as standard [Agent Skills](https://agentskills.io), so it also runs in Codex, Cursor, Gemini CLI, GitHub Copilot, OpenCode and any other agent that loads skills.

## Features

- **Knowledge Management** - PARA-based second brain with capture, recall, and search
- **Marketing Automation** - Campaign planning, content calendars, copywriting frameworks
- **Business Strategy** - SWOT, Porter's Five Forces, Business Model Canvas, OKRs, and more
- **Decision Support** - Structured decision logging with pre-mortems and prioritization
- **Content Humanization** - 43 anti-patterns plus a deterministic linter to detect and remove AI writing fingerprints
- **Translation** - Context-aware bilingual translation with 18 quality patterns

## Quick Start

### Claude Code

```bash
# 1. Install the plugin
/plugin marketplace add alvarogar4/atlas
/plugin install atlas@atlas-marketplace

# 2. Initialize your knowledge base
/atlas:second-brain setup
```

### Any other agent

```bash
# Install all six skills for every agent detected on this machine
npx skills add alvarogar4/atlas --all
```

Then ask the agent to "set up the Atlas second brain". The brain path is saved to `~/.config/atlas/.env`, so every agent shares the same knowledge base.

Subagents (`locate_knowledge`, `analyze_knowledge`, etc.) ship inside `skills/second-brain/agents/`. Agents that can spawn subagents use them as prompts; the rest run them inline. Atlas's persona lives in `CLAUDE.md` (symlinked as `AGENTS.md`); copy it into your agent's global instructions if you want the full Atlas behaviour outside this repo.

After setup, Atlas works conversationally:

- "Save this idea: build a habit tracker CLI"
- "Research content about AI trends"
- "Analyze our market position using SWOT"
- "Weekly review"

## Plugin Structure

```
atlas/
├── skills/                                 # 6 Agent Skills (spec-compliant, portable)
│   ├── second-brain/                       # Core knowledge + project management
│   │   ├── SKILL.md                        # Config, capabilities, agent orchestration, portability
│   │   ├── agents/                         # Subagents (registered in plugin.json for Claude Code)
│   │   │   ├── locate_knowledge.md         # Fast file discovery
│   │   │   ├── analyze_knowledge.md        # Deep analysis and synthesis
│   │   │   ├── content_reviewer.md         # Content QA
│   │   │   ├── market_researcher.md        # Market intelligence
│   │   │   └── strategist.md               # Framework-based analysis
│   │   ├── reference/                      # folder-structure.md
│   │   ├── templates/                      # Project asset templates (9 files)
│   │   ├── entities/                       # Entity definitions (project, theme, competitor, audience, calendar)
│   │   ├── foundations/                     # Project foundations (context, strategy, brand-voice, visual-identity)
│   │   └── workflows/                      # setup, capture, search
│   ├── business-strategy/                  # Strategy + decisions (3 actions)
│   │   ├── SKILL.md                        # Framework selection, capabilities
│   │   ├── frameworks/                     # 12 frameworks (SWOT, Porter's, etc.)
│   │   ├── templates/                      # analysis, decision, review
│   │   └── workflows/                      # analyze, decision, review
│   ├── marketing-content/                  # Content lifecycle
│   │   ├── SKILL.md                        # Content lifecycle, state detection
│   │   ├── channels/                       # blog, linkedin, twitter, email, hackernews, social
│   │   ├── reference/                      # metrics.md, review-checklist.md
│   │   ├── workflow/                       # research, plan, write, review, results, status
│   │   └── calendar/                       # plan, view
│   ├── marketing-visuals/                  # Visual content creation
│   │   ├── SKILL.md                        # Decision tree, workflow chaining
│   │   ├── tools/                          # processing, schema-generation, video-generation + assets
│   │   └── guides/                         # ai-prompting
│   ├── humanizer/                          # AI writing pattern detection (43 anti-patterns + linter)
│   │   └── SKILL.md                        # Zero-tolerance checklist, generation constraints
│   └── translator/                         # Context-aware bilingual translation (18 patterns)
│       └── SKILL.md                        # Translation quality patterns, voice preservation
├── hooks/
│   └── hooks.json                          # Event handlers
├── CLAUDE.md                               # Personality & behavior (AGENTS.md symlinks here)
└── README.md                               # This file
```

## Capabilities

### Knowledge Management (`second-brain`)

PARA-based personal knowledge base: capture ideas, search notes, deep recall with synthesis. Manage projects with foundations (context, strategy, brand voice, visual identity) and entities (themes, competitors, audiences, calendars).

### Content Creation (`marketing-content`)

Full content lifecycle: research, plan, write, review, results tracking, status overview, calendar planning. Supports 6 channels: blog, linkedin, twitter, email, hackernews, social.

Pipeline: research → plan → write → review → [publish] → results

### Business Strategy (`business-strategy`)

Strategic frameworks with 3 operations: analyze (12 frameworks), document decisions, periodic reviews (weekly/monthly/quarterly/annual).

### Visual Content (`marketing-visuals`)

Internal skill for image processing, schema diagrams, AI prompt composition, and short animations (Remotion → MP4 for LinkedIn, looping GIF for X; one composition per format, blind review of stills, optional sound).

### Content Humanization (`humanizer`)

AI writing pattern detection with 43 anti-patterns split across `reference/phrases.md`, `reference/structures.md`, and `reference/style.md`. Loaded as generation constraints during content writing and verified during review. Covers content patterns, language/grammar, style, communication tone, filler/hedging, structural uniformity, directness, precision, and agency.

`tools/lint.sh` catches the mechanically detectable patterns (em dashes, curly quotes, emoji, adverbs, jargon, throat-clearing openers, negative parallelism) with no model judgement involved. It runs on every draft during write and review. Passing the linter is necessary, not sufficient: it sees about a third of the patterns and none of the structural ones.

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

After running `/atlas:second-brain setup` (or asking any agent to set up Atlas), your brain path is stored in a config file shared by every agent:

- `~/.config/atlas/.env` (override the location with `ATLAS_CONFIG`)

Exported shell variables with the same names take precedence. A legacy `.env` at the plugin root is still read as a fallback.

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
