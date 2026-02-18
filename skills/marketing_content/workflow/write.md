# Workflow: Write

**Purpose**: Generate channel-specific content from approved content brief.

## Channel-Specific Guidelines (CRITICAL)

**You MUST read the appropriate channel guidelines before writing.** See the channel table in SKILL.md.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Setup** from SKILL.md.

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

7. **Write content following the channel guidelines AND anti-AI-detection rules:**

Load the `humanizer` skill BEFORE writing. Apply all humanizer patterns as **generation constraints** (not post-processing). The content must be written human-first from the start.

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

Anti-AI-detection rules (MANDATORY during writing, not after):

**Word and phrase level (from humanizer):**
- Zero em dashes. Replace all `—` with commas, periods, or colons. No exceptions.
- No AI vocabulary: "delve", "crucial", "landscape", "tapestry", "multifaceted", "pivotal", "showcase", "underscore", "foster", "garner", "interplay", "intricate", "vibrant", "testament", "enduring", "enhance"
- No inflated symbolism: "beacon of hope", "testament to", "tapestry of"
- No promotional language: "game-changing", "revolutionary", "groundbreaking", "breathtaking"
- No superficial -ing phrases: "highlighting the need", "underscoring the importance", "showcasing how"
- No vague attributions: "critics argue", "some say", "experts believe", "industry observers"
- No negative parallelisms: "not just X but Y", "it's not about X, it's about Y"
- No excessive conjunctions: limit "However", "Moreover", "Furthermore", "Additionally" to max 1 per piece
- No rule of three unless it occurs naturally: avoid forcing ideas into "X, Y, and Z" groups
- No filler phrases: "in order to", "at the end of the day", "it is important to note"
- No sycophantic openings: "Great question!", "Absolutely!", "That's a great point!"
- Use simple copulas ("is", "are", "has") instead of "serves as", "stands as", "functions as"

**Structural level (AI detectors catch these):**
- Vary paragraph lengths: mix 1-sentence paragraphs with 3-5 sentence ones. Never have 4+ consecutive paragraphs of similar length.
- Vary sentence lengths: alternate short punchy sentences with longer flowing ones. Avoid uniform 15-20 word sentences.
- No parallel section structures: each section should have its own shape. If one section uses a list, the next should use prose. If one opens with a question, the next should open differently.
- Allow controlled imperfection: tangents, asides, half-formed thoughts, self-corrections. Real humans meander.
- Vary information density: some paragraphs should be dense with specifics, others should breathe with opinion or reflection.
- Use first-person voice where brand voice calls for it: "I", "we", "I've seen", "in my experience"

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
