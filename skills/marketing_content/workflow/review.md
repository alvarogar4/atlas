# Workflow: Review

**Purpose**: Quality control — MANDATORY before publishing. Runs content_reviewer agent + humanizer pass.

## Humanizer Checks (CRITICAL)

Load the `atlas:humanizer` skill for the full pattern reference and zero-tolerance checklist. Scan the draft against every pattern listed there. You have rights to fix any pattern detected, even if it requires deep edits or its one of the less relevant patterns.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Setup** from SKILL.md.

## Process

1. **Determine channel and topic**: Use the channel and topic from conversation.

2. **Find content folder and verify draft exists:**

```bash
CONTENT_FOLDER=$(ls -d ${PROJECT_PATH}/marketing/content/*${topic}* 2>/dev/null | head -1)
test -f "${CONTENT_FOLDER}/3_draft-${channel}.md"
```

If missing → "I don't see a draft for this channel yet. Want to write it?"

3. **Read draft and research into context:**

```bash
cat "${CONTENT_FOLDER}/3_draft-${channel}.md"
cat "${CONTENT_FOLDER}/1_research.md"
```

4. **Spawn content_reviewer agent:**

```
subagent_type: atlas:marketing:content_reviewer
prompt: "Review {channel} content for quality

Draft file: ${CONTENT_FOLDER}/3_draft-${channel}.md
Research file: ${CONTENT_FOLDER}/1_research.md
Channel: {channel}

Review checklist:
1. Typos and grammar issues (with line numbers)
2. Factual accuracy (verify against research sources)
3. Legal issues (claims, trademark, copyright)
4. Brand voice consistency
5. Channel-specific requirements:
   - Blog: SEO optimization (title, meta, headings)
   - LinkedIn: Hook effectiveness, hashtag count
   - Twitter: Character limits, thread coherence
   - Email: Subject line, CTA placement
   - Hacker News: NO marketing language, Show HN title format, first comment structure
6. CTA effectiveness
7. Flow & structure: ideas introduced in one section are resolved in corresponding sections, logical linear progression, no orphaned concepts

Return:
- Overall status: PASS / NEEDS_REVISION / BLOCKED
- Issues found with severity (critical/warning/suggestion)
- Specific line numbers for each issue
- Recommended fixes
- Strengths noted"
```

5. **Apply reviewer fixes directly to draft:**

For each issue found:

1. Read the specific line(s)
2. Apply the recommended fix
3. Track what was changed

Update the draft file. Output:

```
Content Review Complete

{n} issues found and fixed:
1. [Line X]: {issue type} - "{original}" → "{fixed}"
2. [Line Y]: {issue type} - "{original}" → "{fixed}"

Draft updated: ${CONTENT_FOLDER}/3_draft-${channel}.md
```

6. **Apply humanizer as final polish pass:**

Load the `atlas:humanizer` skill and scan the updated draft against every pattern. Use the zero-tolerance checklist for a fast scan. Apply ALL fixes directly to the draft.

Output:

```
Humanizer Applied

{n} AI writing patterns fixed:
1. [Line X]: "{original}" → "{fixed}"

Draft updated: ${CONTENT_FOLDER}/3_draft-${channel}.md
```

If no patterns found: "No AI writing patterns detected. Draft unchanged."

7. **CHECKPOINT — STOP AND WAIT.** Present review results:

**If BLOCKED:**

```
Review: BLOCKED

{n} issues must be fixed before publishing:
1. [Line X]: {issue} → Fix: {recommendation}

Next: Edit draft manually, then let me re-review.
```

Save review file and STOP.

**If NEEDS REVISION:**

```
Review: NEEDS REVISION

{n} warnings found:
1. [Line X]: {issue}

Options:
1. Fix and re-review
2. Proceed to images anyway (not recommended)
```

**STOP AND WAIT.**

**If PASS:**

```
Review: PASS

Content is ready for publication!
{n} suggestions for consideration (optional).
```

8. **Save review file:** `${CONTENT_FOLDER}/4_review-${channel}.md`

9. **Recommend images** (only if PASS or user chose to proceed):

| Channel  | Recommendation                                                         |
| -------- | ---------------------------------------------------------------------- |
| blog     | "Blog posts need a hero image and OG card for social sharing."         |
| linkedin | "LinkedIn posts with images get 2x engagement. You need an image."     |
| twitter  | "Visual tweets perform better. Consider adding an image."              |
| email    | "Plain text emails often have better deliverability. Images optional." |

```
Create image prompts? (y/n)
```

**CHECKPOINT — STOP AND WAIT.**

10. **If images requested** — generate prompts using `atlas:marketing:visuals` → `guides/ai-prompting.md`:

- Create: `mkdir -p ${CONTENT_FOLDER}/resources/`
- For each image: ask subject, purpose/size, colors, style, mood
- Check `visual-identity.md` for brand defaults
- Save to: `${CONTENT_FOLDER}/resources/prompt-{image-name}.md`

### Output

```
Content is ready! You can now:
- Copy content from 3_draft-${channel}.md to your publishing platform
- Use image prompts in resources/ to generate visuals

After publishing, I can help track performance results.
```

## Review Output Format

```markdown
# Content Review: {Title}

**File**: `{path}`
**Channel**: {channel}
**Date**: {ISO date}

## Review Status: {PASS | NEEDS REVISION | BLOCKED}

## Humanizer Check

**Status**: {PASS | FIXED}
**Patterns fixed**: {count}

## Checks

### Typos & Grammar

**Status**: {PASS | ISSUES FOUND}

### Legal Risks

**Status**: {PASS | ISSUES FOUND}

### Factual Accuracy

**Status**: {PASS | ISSUES FOUND}

### Channel-Specific ({channel})

**Status**: {PASS | ISSUES FOUND}

### Flow & Structure

**Status**: {PASS | ISSUES FOUND}

## Summary

- Total issues: {count}
- Blocking issues: {count}
- AI patterns fixed: {count}
- Recommendations: {count}
```
