# Workflow: Research

**Purpose**: Investigate topic, find sources, check calendar alignment. Research is shared across all channels.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.** This workflow is iterative, not a pipeline.

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine topic**: Follow the Topic Determination pattern from SKILL.md.

2. **Verify context exists:**

```bash
test -f "${CONTENT_FOLDER}/0_context.md"
```

If missing → "Context hasn't been defined yet for this topic. Let's start there to align on angle, constraints, and framing." Then run `workflow/context.md`.

If found, read it into context:

```bash
cat "${CONTENT_FOLDER}/0_context.md"
```

The context file is the source of truth for this piece. All research should serve the angle, respect the constraints, and align with the framing decisions defined there.

3. **Read calendar files for phase objectives:**

```bash
cat ${PROJECT_PATH}/marketing/calendars/*.md 2>/dev/null
```

Extract from active calendar:

- Phase Objective (what this period aims to achieve)
- Success Criteria (how to measure success)
- Per-post objectives relevant to this topic

4. **Read themes for topic context:**

```bash
ls ${PROJECT_PATH}/marketing/themes/*.md 2>/dev/null && cat ${PROJECT_PATH}/marketing/themes/*.md
```

Match topic against themes to understand keywords, target frequency, subtopics.

5. **Load calendar references for this topic:**

Find the calendar entry matching the current topic. If the entry has a `References` column:

- Read each referenced file from `{PROJECT_PATH}/` (e.g., `competitors/acme.md`, `audiences/technical-tim.md`)
- Pass competitor data to the `atlas:market_researcher` subagent for differentiation context
- Pass audience data to inform research angle and reader perspective

6. **Find content folder** (follow Content Folder Discovery from SKILL.md):

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${TOPIC_SLUG}* 2>/dev/null | head -1)
```

The content folder should already exist from the context step. If not found → "I don't see a content folder for this topic. Let's start with context to define the angle and constraints."

7. **Read context constraints into research scope:**

The `0_context.md` defines what this piece is about, what angles to pursue, and what to avoid. Use these as filters during research:

- Only pursue sources that serve the defined angle
- Skip research directions that conflict with the constraints
- Weight findings by relevance to the framing decisions

8. **Locate similar past content**:

```
subagent_type: atlas:locate_knowledge
prompt: "Find existing content that might overlap with '{topic}' in ${PROJECT_PATH}/marketing/content/

Search for:
- Files containing '{topic}' keywords
- Files with similar themes or tags
- Published content in the same content pillar
- Content on similar topics across all channels

Return:
- File paths with dates
- Brief title/summary of each piece
- Overlap assessment (high/medium/low)
- Suggested differentiation angles"
```

9. **Analyze past content patterns** (if content found):

```
subagent_type: atlas:analyze_knowledge
prompt: "Analyze these existing content pieces for patterns:

Files to analyze:
{paste file paths from atlas:locate_knowledge}

Extract content-specific patterns:
- Structural patterns: How are pieces organized?
- Hook techniques: What opening styles are used?
- CTA patterns: What calls-to-action appear?
- Tone and style: Voice, formality, personality
- Engagement patterns: What performed well?
- Gaps in coverage that new content could fill

Return patterns that should inform the new content research."
```

**Wait for analysis to complete before checkpoint.**

10. **CHECKPOINT — STOP AND WAIT.** If overlapping content found:

```
Found {n} related pieces:
- {piece 1 title} ({type})
- {piece 2 title} ({type})

Options:
1. Proceed with differentiated angle
2. Pivot to different topic
3. Cancel

Your choice?
```

11. **Only after user confirms**, spawn `atlas:market_researcher`:

```
subagent_type: atlas:market_researcher
prompt: "Research content topic: '{topic}'

IMPORTANT: Do NOT create any files or folders. Return your findings as text only. The main agent will handle saving.

Content context (from 0_context.md — these are hard constraints):
{paste relevant sections from 0_context.md: angle, constraints, framing decisions}

Context from project:
- Phase Objective: {from calendar}
- Target themes: {from themes}

Calendar references: {data from referenced competitor/audience files, if any}
- If competitor referenced: Check what they've published on this topic. Identify differentiation angles.
- If audience referenced: Research with this reader persona in mind.

Existing related content to avoid overlap:
{file paths from atlas:locate_knowledge}

Pattern analysis from existing content:
{summary from atlas:analyze_knowledge}

Research objectives:
1. Find authoritative sources for the topic
2. Identify unique angle that differentiates from existing content
3. Gather supporting data, examples, and quotes
4. Note potential expert voices to cite
5. Consider what works best across multiple content channels

Return:
- Sources found with URLs/citations
- Recommended angle with rationale
- Key data points and examples
- Channel-agnostic recommendations
- Open questions requiring user input"
```

12. **CHECKPOINT — STOP AND WAIT.** Present research findings:

```
Research complete!

Sources found: {n}
Recommended angle: {angle}

Open questions:
- {question 1}
- {question 2}

Proceed with this angle? (y/n/adjust)
```

13. If user has questions or adjustments, iterate.

14. **Only after user confirms**, save: `${CONTENT_FOLDER}/1_research.md`

15. **Apply cross-referencing** (see `second_brain/reference/cross-referencing.md`):

- Append a `**See also**` footer to `1_research.md` linking to all existing siblings in the folder (e.g., `[context](0_context.md) | [resources](resources/index.md)`)
- Update the `**See also**` footer in `0_context.md` to include `[research](1_research.md)`

### Output

```
Research saved: ${CONTENT_FOLDER}/1_research.md

Review the research file. Ready to plan the content structure?
```
