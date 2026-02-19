# Workflow: Research

**Purpose**: Investigate topic, find sources, check calendar alignment. Research is shared across all channels.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.** This workflow is iterative, not a pipeline.

## Setup

Execute **Config** from SKILL.md.

## Process

1. **Determine topic**: Use the topic from conversation. Slugify for folder naming.

2. **Read calendar files for phase objectives:**

```bash
cat ${PROJECT_PATH}/marketing/calendars/*.md 2>/dev/null
```

Extract from active calendar:
- Phase Objective (what this period aims to achieve)
- Success Criteria (how to measure success)
- Per-post objectives relevant to this topic

3. **Read themes for topic context:**

```bash
ls ${PROJECT_PATH}/marketing/themes/*.md 2>/dev/null && cat ${PROJECT_PATH}/marketing/themes/*.md
```

Match topic against themes to understand keywords, target frequency, subtopics.

4. **Read brand voice:**

```bash
cat ${PROJECT_PATH}/marketing/brand-voice.md 2>/dev/null
```

5. **Check for existing content folder** (follow Content Folder Discovery from SKILL.md):

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

6. **Create content folder** (only if no existing folder chosen):

```bash
CONTENT_FOLDER="${PROJECT_PATH}/marketing/content/${DATE}_${TOPIC_SLUG}"
mkdir -p "${CONTENT_FOLDER}"
mkdir -p "${CONTENT_FOLDER}/resources"
```

7. **Locate similar past content** (PARALLEL with step 8):

```
subagent_type: atlas:core:locate_knowledge
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

8. **Analyze past content patterns** (if content found):

```
subagent_type: atlas:core:analyze_knowledge
prompt: "Analyze these existing content pieces for patterns:

Files to analyze:
{paste file paths from locate_knowledge}

Extract content-specific patterns:
- Structural patterns: How are pieces organized?
- Hook techniques: What opening styles are used?
- CTA patterns: What calls-to-action appear?
- Tone and style: Voice, formality, personality
- Engagement patterns: What performed well?
- Gaps in coverage that new content could fill

Return patterns that should inform the new content research."
```

**Wait for BOTH agents to complete before checkpoint.**

9. **Read key files into main context**: After agents complete, read top 2-3 most relevant existing pieces to verify overlap assessment.

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

11. **Only after user confirms**, spawn market_researcher:

```
subagent_type: atlas:marketing:market_researcher
prompt: "Research content topic: '{topic}'

IMPORTANT: Do NOT create any files or folders. Return your findings as text only. The main agent will handle saving.

Context from project:
- Phase Objective: {from calendar}
- Target themes: {from themes}
- Brand voice: {key points from brand-voice.md}

Existing related content to avoid overlap:
{file paths from locate_knowledge}

Pattern analysis from existing content:
{summary from analyze_knowledge}

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

### Output

```
Research saved: ${CONTENT_FOLDER}/1_research.md

Review the research file. Ready to plan the content structure?
```
