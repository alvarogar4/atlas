# Workflow: Write

**Purpose**: Generate channel-specific content from approved content brief.

## Channel-Specific Guidelines (CRITICAL)

**You MUST read the appropriate channel guidelines before writing.** See the channel table in SKILL.md.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Config** from SKILL.md.

## Process

1. **Determine channel and topic**: Use the channel and topic from conversation.

2. **Find content folder** (follow Content Folder Discovery from SKILL.md):

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${topic}* 2>/dev/null | head -1)
```

3. **Verify content brief exists:**

```bash
test -f "${CONTENT_FOLDER}/2_plan.md"
```

If missing → "The content brief isn't ready yet. Want to create one?"

4. **Read channel-specific writing guidelines** from `channels/{channel}.md`.

5. **Read content brief and research into context:**

```bash
cat "${CONTENT_FOLDER}/2_plan.md"
cat "${CONTENT_FOLDER}/1_research.md"
```

6. **Read brand voice** (if available):

```bash
cat ${PROJECT_PATH}/marketing/brand-voice.md 2>/dev/null
```

7. **Load the `atlas:humanizer` skill.** These are **generation constraints**, not post-processing. Internalize all 29 patterns BEFORE writing a single word, and make sure to apply them to the draft.

8. **Write content following the channel guidelines and humanizer rules:**

| Channel    | Key Requirements                                                          |
| ---------- | ------------------------------------------------------------------------- |
| blog       | Follow outline structure exactly, hit word count, cite sources inline     |
| linkedin   | Hook in first 140 chars, use line breaks, 3-5 hashtags, personal stories  |
| twitter    | First tweet must hook alone, 280 char limit per tweet, close threads      |
| email      | Subject 30-50 chars, one clear CTA, conversational tone, plain text ready |
| hackernews | Show HN title format, first comment structure, NO marketing language      |
| social     | Platform-appropriate length, engagement-focused, clear CTA                |

Content guidelines:

- Follow the approved content brief exactly (use the channel-specific section)
- Maintain consistent brand voice
- Include proper citations/links where applicable
- Match format requirements for the channel
- Include clear call-to-action
- Do NOT carry over formatting patterns from research documents (em dashes, list styles, etc.)
- Apply ALL humanizer rules from the `atlas:humanizer` skill during writing, not after

9. **Save draft immediately:** `${CONTENT_FOLDER}/3_draft-${channel}.md`

The user will review via `git diff`. Do NOT ask for acknowledgment before saving.

### Output

Present a brief summary after saving:

```
Draft saved: ${CONTENT_FOLDER}/3_draft-${channel}.md

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
