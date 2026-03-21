# Workflow: Context

**Purpose**: Conversational intake step where user and agent align on angle, constraints, tone, narrative structure, and framing decisions before any research or planning begins. This is step 0 — the foundation that all downstream workflows reference.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.** This workflow is conversational, not a form to fill out.

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine topic**: Follow the Topic Determination pattern from SKILL.md.

2. **Check for existing content folder** (follow Content Folder Discovery from SKILL.md):

```bash
DATE=$(date +%Y-%m-%d)
TOPIC_SLUG=$(echo "{topic}" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')
EXISTING_FOLDERS=$(ls -d ${PROJECT_PATH}/marketing/content/*${TOPIC_SLUG}* 2>/dev/null)
```

**If existing folder(s) found:**

```
Found existing campaign folder(s) for this topic:
{list each folder with date}

Options:
1. Use existing folder: {folder path}
2. Create new folder for this topic

Your choice?
```

**CHECKPOINT — STOP AND WAIT.**

3. **Create content folder** (only if no existing folder chosen):

```bash
CONTENT_FOLDER="${PROJECT_PATH}/marketing/content/${DATE}_${TOPIC_SLUG}"
mkdir -p "${CONTENT_FOLDER}"
mkdir -p "${CONTENT_FOLDER}/resources"
```

4. **Load project context for grounding:**

```bash
cat "${PROJECT_PATH}/context.md" 2>/dev/null
cat "${PROJECT_PATH}/marketing/brand-voice.md" 2>/dev/null
```

This gives you the project's identity, rules, and voice. Use it to ground the conversation — don't repeat what's already defined there.

5. **Start the conversation.** First, ask for a bulk dump of the context. Then, if necessary, ask the user ONE question at a time to build the context. Don't present a form or checklist. Have a natural back-and-forth to uncover:

- **Core angle**: What's the main thesis or point of view?
- **Constraints**: What must NOT be said? What must be said exactly?
- **Tone and register**: How should this piece feel? (beyond brand voice defaults)
- **Narrative structure**: Story arc, logical progression, comparison, etc.
- **Framing decisions**: Specific terminology choices, positioning, emphasis
- **Source material**: Any existing docs, conversations, or references to draw from
- **Target outcome**: What should the reader think/feel/do after reading?

Not every piece needs all of these. Let the conversation flow naturally. The user may provide several of these upfront, or may need prompting.

**CHECKPOINT — STOP AND WAIT after each exchange.** This is a dialogue, not a monologue.

6. **When the user signals alignment** (or you've covered enough ground), synthesize the context into a summary and present it:

```
Here's what I've captured for this piece:

## Angle
{core thesis}

## Constraints
{what must/must not be included}

## Tone
{specific tone notes beyond brand voice}

## Narrative Structure
{how the piece should flow}

## Framing Decisions
{terminology, positioning, emphasis choices}

## Source Material
{references to use}

## Target Outcome
{what the reader should take away}

Does this capture everything? Anything to add or change?
```

**CHECKPOINT — STOP AND WAIT.**

7. If user has adjustments, iterate. Remove sections that don't apply — the context file should only contain what's relevant to this specific piece.

8. **Only after user confirms**, save: `${CONTENT_FOLDER}/0_context.md`

9. **Populate `related` in frontmatter** (see `second_brain/reference/cross-referencing.md`): Add vault-root paths to the calendar entry for this topic (if one exists) and any referenced theme/audience files.

### Output

```
Context saved: ${CONTENT_FOLDER}/0_context.md

Ready to start researching this topic?
```

## Output Format

```yaml
---
topic: "{topic}"
project: {project}
status: approved
created: {ISO timestamp}
approved: {ISO timestamp}
---

# Content Context: {Title}

## Angle
{core thesis}

## Constraints

> [!warning] Hard Constraints
> {rules and boundaries that cannot be violated}

## Tone
{tone notes}

## Narrative Structure
{flow and arc}

## Framing Decisions
{terminology and positioning}

## Source Material
{references}

## Target Outcome
{reader takeaway}
```

Only include sections that are relevant. Don't pad with empty sections.
