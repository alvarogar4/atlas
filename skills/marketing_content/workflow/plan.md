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

If not found → "I don't see a content folder for this topic. Want to start with research?"

3. **Verify research exists:**

```bash
test -f "${CONTENT_FOLDER}/1_research.md"
```

If missing → "Research hasn't been done yet for this topic. Want to start there?"

4. **Load calendar references for this topic:**

Read the current calendar. Find the entry matching this topic. If the entry references audience files:

- Read referenced audience personas from `{PROJECT_PATH}/marketing/audiences/{name}.md`
- Use persona data to inform channel selection (where they hang out) and messaging alignment (tone, pain points, goals)

Present audience-informed channel recommendations:

- {Persona} hangs out on {platforms} -> recommend {channels}

5. **Determine target channels** — ask user:

```
Which channels do you want to target?
Options: blog, linkedin, twitter, email, hackernews, social
```

**CHECKPOINT — STOP AND WAIT.**

Read the corresponding writing guidelines from the channel files listed in SKILL.md.

6. **Read research into context:**

```bash
cat "${CONTENT_FOLDER}/1_research.md"
```

7. **Create unified content brief** with per-channel outlines:

### Blog Outline Structure

```
- Title options (3)
- SEO Strategy (primary/secondary keywords, meta description)
- Introduction (~150-200 words) with hook type
- 3-5 main sections with briefs (~300-500 words each)
- Conclusion with CTA (~150-200 words)
- Internal/external links
- Word count target
```

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

8. **CHECKPOINT — STOP AND WAIT.** Present content brief:

```
Based on research, I propose this content brief:

## Core Angle
{shared thesis}

## Per-Channel Outlines
{Show structure for each selected channel}

Does this structure work? Any sections to add/remove/adjust?
```

9. If user requests changes, adjust and re-present.

10. **Only after user approves**, save: `${CONTENT_FOLDER}/2_plan.md`

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
