# Workflow: Write

**Purpose**: Generate channel-specific content from approved content brief.

## Channel-Specific Guidelines (CRITICAL)

**You MUST read the appropriate channel guidelines before writing.** See the channel table in SKILL.md.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine channel and topic**: Follow the Topic Determination pattern from SKILL.md. Channel from conversation.

2. **Find content folder** (follow Content Folder Discovery from SKILL.md):

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${topic}* 2>/dev/null | head -1)
```

3. **Verify content brief exists:**

```bash
test -f "${CONTENT_FOLDER}/2_plan.md"
```

If missing → "The content brief isn't ready yet. Want to create one?"

4. **Read channel-specific writing guidelines** from `channels/{channel}.md`. **These are hard constraints.** Every measurable requirement (character limits, keyword placement, word counts, structure rules, quality checklist items) must be satisfied in the draft. Do not produce content that violates the channel's own rules.

5. **Read context, content brief, and research into context:**

```bash
cat "${CONTENT_FOLDER}/0_context.md"
cat "${CONTENT_FOLDER}/2_plan.md"
cat "${CONTENT_FOLDER}/1_research.md"
```

The `0_context.md` file contains the framing decisions, constraints, and tone for this piece. These are **hard constraints** during writing — every sentence must respect the angle, use the approved terminology, and avoid anything the constraints rule out.

6. **Load the `atlas:humanizer` skill.** These are **generation constraints**, not post-processing. Read the zero-tolerance checklist and every pattern description. Before writing a single word, you must know all 29 patterns well enough to avoid them during generation, including variant forms. The checklist exists because "internalizing" rules isn't enough. Treat each pattern as a hard constraint: if a sentence would trigger any pattern, rewrite it before moving on.

7. **Write content following the channel guidelines and humanizer rules:**

| Channel    | Key Requirements                                                                  |
| ---------- | --------------------------------------------------------------------------------- |
| blog       | Follow outline structure exactly, hit word count, cite sources inline             |
| linkedin   | Hook in first 140 chars, use line breaks, personal stories, close per brand voice |
| twitter    | First tweet must hook alone, 280 char limit per tweet, close threads              |
| email      | Subject 30-50 chars, one clear CTA, conversational tone, plain text ready         |
| hackernews | Show HN title format, first comment structure, NO marketing language              |
| social     | Platform-appropriate length, engagement-focused, clear CTA                        |

Content guidelines:

- Follow the approved content brief exactly (use the channel-specific section)
- Maintain consistent brand voice
- Include proper citations/links where applicable
- Match format requirements for the channel
- Include clear call-to-action
- Do NOT carry over formatting patterns from research documents (em dashes, list styles, etc.)
- Every sentence and pargrpah must satisfy all 29 humanizer patterns as it is written. If you catch yourself generating a pattern, stop and rewrite that sentence before continuing. Do not plan to "fix it later."
- Apply trademark symbols (®, ™) on first mention of third-party products per project context rules or check the product's official website for their trademark usage guidelines

8. **Save draft immediately:** `${CONTENT_FOLDER}/3_draft-${channel}.md`

The user will review via `git diff`. Do NOT ask for acknowledgment before saving.

9. **Image assessment and generation (COMPULSORY):**

After saving the draft, check the channel guidelines (`channels/{channel}.md`) for **Image Requirements**. Every channel defines how many images are needed and when to skip.

**Process:**

- Read the channel's image requirements section
- Determine how many images are needed and their purpose (hero/social card, diagram, illustration, etc.)
- Load `atlas:marketing_visuals` skill
- Generate AI image prompts or schemas for each required image
- Save prompts and any generated assets to `${CONTENT_FOLDER}/resources/`
- If the channel guidelines say no images are needed, skip and note "No images required for this channel" in the output
- **Reuse across channels**: Images in `resources/` are shared. When writing for a second channel on the same topic, check existing assets before generating new ones — if they fit for the use case, you can reuse or adapt across channels if they serve the purpose.

10. **Apply cross-referencing** (see `second_brain/reference/cross-referencing.md`):

- Append a `**See also**` footer to `3_draft-${channel}.md` linking to all existing siblings (context, research, plan, other drafts, resources/index.md)
- Update the `**See also**` footers in all existing siblings to include `[draft ${channel}](3_draft-${channel}.md)`
- Update `resources/index.md` to list any new resources created during image generation

### Output

Present the article in the chat too

```
Draft saved: ${CONTENT_FOLDER}/3_draft-${channel}.md
Images: {N} resource(s) saved to ${CONTENT_FOLDER}/resources/

Ready for quality review?
```

## Output Format

```yaml
---
channel: "{channel}"
topic: "{topic}"
project: { project }
status: draft
created: { ISO timestamp }
---
```

Channel-specific body format defined in the writing guidelines.
