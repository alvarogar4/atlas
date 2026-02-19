---
name: atlas:marketing:content
description: Content lifecycle management - research, planning, writing, review, and results tracking. Also manages content calendars and themes. Use when working with marketing content.
tools: Read, Write, Grep, Glob, Bash, AskUserQuestion, WebSearch, Task
user_invocable: true
---

# Marketing Content

Content lifecycle management with calendars and themes.

## Config

Follow the **Config Chain** from `second_brain_foundation/SKILL.md` (project-level config required).

Requires: `BRAIN_PATH`, `ACTIVE_PROJECT`, `PROJECT_PATH`

## Content Lifecycle

Content follows a strict pipeline. Each step produces a numbered file:

```
research (1_research.md) → plan (2_plan.md) → write (3_draft-{channel}.md) → review (4_review-{channel}.md) → [publish] → results (5_results-{channel}.md)
```

**Starting point detection**: When a user wants to create content, determine where to start:

- "I want to write about X" → Check if research exists. If not, start at research
- "Let's plan content for X" → Check if research exists. If not, start at research
- "Review my blog post about X" → Check if draft exists. If not, tell user to write first
- Always enforce: research before plan, plan before write, write before review

### Capabilities

| What the user wants                | Workflow                            |
| ---------------------------------- | ----------------------------------- |
| Research a content topic           | `workflow/research.md`              |
| Plan content structure             | `workflow/plan.md`                  |
| Write content for a channel        | `workflow/write.md`                 |
| Review content quality (mandatory) | `workflow/review.md`                |
| Document content performance       | `workflow/results.md`               |
| View content calendar              | `calendar/view.md`                  |
| Plan quarterly content             | `calendar/plan.md`                  |
| Create a content theme             | `themes/manage.md` → add section    |
| List themes                        | `themes/manage.md` → list section   |
| Edit a theme                       | `themes/manage.md` → edit section   |
| Archive a theme                    | `themes/manage.md` → remove section |

### State Detection

Before starting any content workflow, check for existing work:

```bash
TOPIC_SLUG=$(echo "{topic}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${TOPIC_SLUG}* 2>/dev/null | head -1)
```

If folder found, check which files exist to determine current state:

- Has `1_research.md` → research done
- Has `2_plan.md` → planning done
- Has `3_draft-{channel}.md` → draft exists for that channel
- Has `4_review-{channel}.md` → review done for that channel
- Has `5_results-{channel}.md` → results recorded

Report state to user: "I found existing work on this topic: [research done, blog draft in progress]. Where would you like to continue?"

## Content Folder Structure

Content is organized topic-first with shared research/plan and channel-suffixed drafts:

```
${PROJECT_PATH}/marketing/content/
└── {date}_{topic}/
    ├── 1_research.md               # Research findings (research)
    ├── 2_plan.md                   # Content brief (plan)
    ├── 3_draft-{channel}.md        # Written content (write)
    ├── 4_review-{channel}.md       # Review results (review)
    ├── 5_results-{channel}.md      # Performance metrics (results)
    └── resources/                  # Image prompts and generated assets
```

## Shared Patterns

### Content Folder Discovery

```bash
TOPIC_SLUG=$(echo "{topic}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${TOPIC_SLUG}* 2>/dev/null | head -1)
```

### Channel Validation

Valid channels: `blog`, `linkedin`, `twitter`, `email`, `hackernews`, `social`

If invalid channel provided → "Invalid channel '{channel}'. Valid: blog, linkedin, twitter, email, hackernews, social"

### Channel Writing Guidelines

When writing or reviewing, read the channel-specific guidelines:

| Channel    | File                     |
| ---------- | ------------------------ |
| blog       | `channels/blog.md`       |
| linkedin   | `channels/linkedin.md`   |
| twitter    | `channels/twitter.md`    |
| email      | `channels/email.md`      |
| hackernews | `channels/hackernews.md` |
| social     | `channels/social.md`     |

### Shared Writing Patterns

These apply across all channels:

**Hook Techniques:**

| Technique      | Description                   | Example                                 |
| -------------- | ----------------------------- | --------------------------------------- |
| Contrarian     | Challenge conventional wisdom | "Everything you know about X is wrong." |
| Question       | Create curiosity gap          | "Why do 90% of startups fail?"          |
| Story          | Personal narrative opener     | "Last Tuesday, I almost quit."          |
| Stat/Number    | Lead with data                | "67% of blog posts get zero shares."    |
| Bold claim     | Make a strong assertion       | "Cold email is dead."                   |
| Direct address | Speak to the reader           | "If you're struggling with X..."        |
| Achievement    | Share a result                | "I went from $0 to $1M ARR."            |

**CTA Best Practices:**

- **One primary CTA per piece** — Multiple CTAs dilute action
- **Action-oriented language** — "Get", "Start", "Download" beats "Click here", "Submit"
- **Benefit-focused** — "Get my free checklist" beats "Download"
- **Personalized CTAs** perform 202% better than generic
- **Place above the fold** for primary, repeat at end

**Formatting Rules:**

- Short paragraphs: 1-3 sentences max for digital content
- Line breaks: Create visual breathing room
- One idea per section: Don't bundle multiple concepts
- Scannable structure: Subheadings, bullets, numbered lists
- Read aloud test: If it sounds unnatural, rewrite it

**Pre-Write Quality Checks:**

- [ ] Hook grabs attention in the first line
- [ ] Single primary CTA is clear
- [ ] Tone matches the channel and brand voice
- [ ] No filler or padding content
- [ ] Reads naturally (read aloud test passed)
- [ ] Frontmatter is complete with all required fields

**Post-Write Humanization (MANDATORY cross-load):**

Whenever you write or edit marketing content, you MUST load the `atlas:humanizer` skill BEFORE writing or presenting any text to the user. This includes:

- Full draft creation via `workflow/write.md`
- Rewriting paragraphs or sections in existing drafts
- Any content edit the user requests

Load the skill, apply its 29 anti-patterns as generation-time constraints (not post-processing). Never show the user AI-patterned text and ask them to humanize it separately. The humanizer pass is automatic and non-negotiable.

**Visual Assets (MANDATORY):**

Whenever content involves visual assets, you MUST load the `atlas:marketing_visuals` skill BEFORE proceeding with any visual work. This includes:

- Composing AI image generation prompts (hero images, cover images, OG cards)
- Processing or editing images (crop, resize, optimize, background removal)
- Creating diagrams, schemas, or flowchart visualizations
- Any task involving the `resources/` folder for visual content

Do not attempt image work with ad-hoc approaches (raw Python/Pillow, manual prompt composition). The skill contains structured prompt templates, dedicated CLI tools (`bun crop`, `bun polish`, `bun optimize`), and brand-consistent visual guidelines from `visual-identity.md`. Load the skill, follow its decision tree.

## Error Handling

- **Missing prerequisite**: Tell user which step is needed first and offer to start it. Example: "This topic needs research before we can plan. Want me to start researching?"
- **Content folder not found**: "I don't see any work on this topic yet. Want to start with research?"
- **Agent failure**: Log error, present partial results, offer to retry
- **Checkpoint timeout**: Save progress, allow resume
