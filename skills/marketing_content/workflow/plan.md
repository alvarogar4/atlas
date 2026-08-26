# Workflow: Plan

**Purpose**: Create a shared content brief covering all target channels from research.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine topic**: Follow the Topic Determination pattern from SKILL.md.

2. **Find content folder** (follow Content Folder Discovery from SKILL.md):

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${topic}* 2>/dev/null | head -1)
```

If not found → "I don't see a content folder for this topic. Want to start with context?"

3. **Verify context and research exist:**

```bash
test -f "${CONTENT_FOLDER}/0_context.md"
test -f "${CONTENT_FOLDER}/1_research.md"
```

If context missing → "Context hasn't been defined yet for this topic. Let's start there to align on angle and constraints."
If research missing → "Research hasn't been done yet for this topic. Want to start there?"

4. **Read context into planning scope:**

```bash
cat "${CONTENT_FOLDER}/0_context.md"
```

The context file defines the angle, constraints, tone, and framing decisions for this piece. The content brief must serve these — don't propose outlines that conflict with the context.

5. **Load calendar references for this topic:**

Read the current calendar. Find the entry matching this topic. If the entry references audience files:

- Read referenced audience personas from `{PROJECT_PATH}/marketing/audiences/{name}.md`
- Use persona data to inform channel selection (where they hang out) and messaging alignment (tone, pain points, goals)

Present audience-informed channel recommendations:

- {Persona} hangs out on {platforms} -> recommend {channels}

6. **Determine target channels** — ask user:

```
Which channels do you want to target?
Options: blog, linkedin, twitter, email, hackernews, social
```

**CHECKPOINT — STOP AND WAIT.**

Read the corresponding writing guidelines from the channel files listed in SKILL.md. **Channel guidelines are hard constraints, not suggestions.** Every measurable requirement (character limits, keyword placement, word count targets, structure rules) must be satisfied in the outline. Do not propose options that violate the channel's own rules.

7. **Read research into context:**

```bash
cat "${CONTENT_FOLDER}/1_research.md"
```

8. **Create unified content brief** with per-channel outlines:

### Blog Outline Structure

Read the GEO section of `channels/blog.md` before outlining a blog post. GEO decisions belong in the brief, not in the draft, because format and FAQ questions change the outline itself.

```
- Title options (3)
- GEO format (standard | comparison | listicle | original-data) with rationale
- SEO Strategy (primary/secondary keywords, meta description)
- Answer capsule draft (40-80 words, the question the article answers)
- Introduction (~150-200 words) with hook type
- 3-5 main sections with briefs (~300-500 words each)
  - Per section: the question it answers, and the lead form (claim/number/
    definition/verdict/contrast/concession). Lead forms must differ between
    consecutive sections
- Conclusion with CTA (~150-200 words)
- FAQ: 4-8 real questions sourced from search suggestions, sales calls,
  support tickets, or forums. Flag any that are invented
- Internal/external links
- Word count target
- Refresh passes: proposed dates for +2 weeks, +4-6 weeks, +8-12 weeks
```

**Format selection**: if the topic is a head-to-head, an "alternatives to X" query, or a tool selection question, propose a comparison page or ranked listicle instead of a standard article. If the project holds proprietary data on the topic (benchmarks, usage stats, survey results), propose an original-data post. Format specs and the citation evidence are in the GEO section of `channels/blog.md`.

### LinkedIn Outline Structure

```
- Hook (first 140 characters - before "see more")
- Main message (3-5 key points)
- Story/example element
- Closing thought or CTA (per brand voice)
- Carousel slides (if applicable)
```

### Twitter Outline Structure

```
- Thread hook (first tweet - must stand alone)
- Thread structure (5-15 tweets)
- Key points per tweet
- Media requirements (images, videos)
- Final tweet CTA
```

### Email Outline Structure

```
- Subject line options (3)
- Preheader text
- Email type (newsletter, nurture, promotional, transactional)
- Opening hook
- Body sections
- CTA placement and copy
- P.S. line (optional)
```

9. **CHECKPOINT — STOP AND WAIT.** Present content brief:

```
Based on research, I propose this content brief:

## Core Angle
{shared thesis}

## Per-Channel Outlines
{Show structure for each selected channel}

Does this structure work? Any sections to add/remove/adjust?
```

10. If user requests changes, adjust and re-present.

11. **Only after user approves**, save: `${CONTENT_FOLDER}/2_plan.md`

12. **Populate `related` in frontmatter** (see `second_brain/reference/cross-referencing.md`): Add vault-root paths to siblings in the content folder, calendar entry, and any referenced theme/audience files.

### Confirmation

```
Content brief approved and saved: ${CONTENT_FOLDER}/2_plan.md

Ready to write? Which channel should we start with?
```

## Output Format

```yaml
---
topic: "{topic}"
channels: [{selected channels}]
project: {project}
status: approved
created: {ISO timestamp}
approved: {ISO timestamp}
---

# Content Brief: {Title}

## Core Angle
{shared thesis and key messages}

## Target Audience
{audience description}

## Channel: Blog
{Blog-specific outline if selected}

## Channel: LinkedIn
{LinkedIn-specific outline if selected}

---

**Status**: Brief approved. Ready for writing.
```
