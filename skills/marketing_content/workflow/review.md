# Workflow: Review

**Purpose**: Quality control — MANDATORY before publishing. Runs `atlas:content_reviewer` agent + humanizer pass.

## Humanizer Checks (CRITICAL)

Load the `atlas:humanizer` skill for the full pattern reference and zero-tolerance checklist. Verify the draft against every pattern listed there. The humanizer was applied during writing; this pass catches anything that slipped through. You have rights to fix any pattern detected, even if it requires deep edits or its one of the less relevant patterns.

## Checkpoint Enforcement (CRITICAL)

**STOP AND WAIT at every checkpoint.**

## Setup

Execute **Full** config from `atlas:second_brain`.

## Process

1. **Determine channel and topic**: Follow the Topic Determination pattern from SKILL.md. Channel from conversation.

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

4. **Apply humanizer verification pass:**

The writing pass applied humanizer rules during generation. This pass is a **verification scan**: it catches patterns that slipped through because the model was balancing content quality with pattern avoidance. Load the `atlas:humanizer` skill, verify the draft against every pattern, use the zero-tolerance checklist for a fast scan. Fix any patterns found and track changes.

This runs before QA so the reviewer evaluates the actual content that will be published.

5. **Spawn `atlas:content_reviewer` agent on the humanized draft:**

```
subagent_type: atlas:content_reviewer
prompt: "Review {channel} content for quality

IMPORTANT: Do NOT create any files or folders. Return your findings as text only. The main agent will handle it.

Draft file: ${CONTENT_FOLDER}/3_draft-${channel}.md
Research file: ${CONTENT_FOLDER}/1_research.md
Channel: {channel}

Use the review checklist from reference/review-checklist.md as your primary reference.

Review checklist:
1. Typos and grammar issues (with line numbers)
2. Factual accuracy (verify against research sources)
3. Legal issues (claims, trademark, copyright). Scan the draft for every third-party product, technology, or brand name mentioned. For each one:
  - Check `${PROJECT_PATH}/context.md` for project-specific trademark rules
  - If not covered there, check the product's official website for their trademark usage guidelines
  - Apply the correct symbol (®, ™) with the frequency and placement that brand requires
  - This is a **blocking** check: missing trademark symbols = BLOCKED status
4. Brand voice consistency
5. Channel-specific requirements:
   - Blog: SEO optimization (title, meta, headings)
   - LinkedIn: Hook effectiveness, closing style matches brand voice
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

6. **Apply reviewer fixes and append corrections log:**

For each issue found:

1. Read the specific line(s)
2. Apply the recommended fix
3. Track what was changed

Then append a combined corrections section at the bottom of `3_draft-${channel}.md`:

```markdown
---

## Corrections Applied

**Date**: {ISO date}

### Humanizer Fixes

{n} AI patterns fixed:

1. [Line X]: "{original}" → "{fixed}"

### Reviewer Fixes

{n} issues fixed:

1. [Line X]: {issue type} - "{original}" → "{fixed}"
```

Save the draft once with both the reviewer fixes and corrections log applied.

7. **Save reviewer findings as review file:** `${CONTENT_FOLDER}/4_review-${channel}.md`

Use the Review Output Format below.

8. **CHECKPOINT — STOP AND WAIT.** Present review results:

**If BLOCKED:**

```
Review: BLOCKED

{n} issues found and fixed, but {n} blockers remain:
1. [Line X]: {issue} → Fix: {recommendation}

Next: Edit draft manually, then re-run review.
```

**If NEEDS REVISION:**

```
Review: NEEDS REVISION

{n} warnings remain:
1. [Line X]: {issue}

Options:
1. Fix and re-review
2. Override and proceed
```

**STOP AND WAIT.**

**If PASS:**

```
Review: PASS

Content is ready for publication!
{n} suggestions for consideration (optional).
```

### Output

**If PASS:**

```
Content is ready! You can now:
- Copy content from 3_draft-${channel}.md to your publishing platform
- Create image prompts using `atlas:marketing_visuals` if needed

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

### Legal Risks (Trademarks, Copyright, etc.)

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
