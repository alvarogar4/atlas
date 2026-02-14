# Content Review Checklist

Patterns and checklists for content quality control. Used by the `atlas:marketing:content_reviewer` agent.

## Review Categories

### 1. Typos & Grammar

**Check for:**

- Spelling errors
- Grammar mistakes
- Inconsistent capitalization (headers, proper nouns)
- Broken markdown formatting (unclosed tags, bad links)
- Placeholder text ({TODO}, [REPLACE], TBD, etc.)
- Repeated words/phrases ("the the", "and and")
- Missing punctuation at end of sentences

**Severity:**

- BLOCKER: Wrong names, numbers, dates, company names
- WARNING: Typos in body text
- SUGGESTION: Style improvements, word choice

### 2. Legal Risks

**HIGH RISK - Mark as BLOCKER:**

| Issue                              | Example                         | Fix                                     |
| ---------------------------------- | ------------------------------- | --------------------------------------- |
| Competitor claims without citation | "X is slower than us"           | Add benchmark source or remove          |
| Medical advice                     | "This cures headaches"          | Add "Consult a healthcare professional" |
| Financial advice                   | "Invest in X"                   | Add "Not financial advice" disclaimer   |
| Defamatory statements              | "Company X is fraudulent"       | Remove or cite legal proceedings        |
| Copyright                          | Long quotes without attribution | Add source or shorten quote             |
| Privacy/PII                        | Email addresses, phone numbers  | Remove or redact                        |

**MEDIUM RISK - Mark as WARNING:**

| Issue        | Example                         | Fix                    |
| ------------ | ------------------------------- | ---------------------- |
| Superlatives | "best", "only", "#1"            | Add evidence or soften |
| Comparatives | "better than", "faster than"    | Add data source        |
| Guarantees   | "will definitely", "guaranteed" | Soften language        |

### 3. Factual Accuracy

**Process:**

1. Extract all factual claims (statistics, dates, quotes, company info)
2. For each claim:
   - Is source cited? If yes, verify claim matches source
   - If no source, search web to verify
   - Flag unverifiable claims

**Common claims to verify:**

- Statistics and percentages ("40% faster", "10x improvement")
- Historical facts and dates
- Technical specifications
- Company information (founding date, employee count)
- Quotes attributed to people

### 4. SEO Compliance (Blog only)

**Checklist:**

- [ ] Target keyword in title
- [ ] Target keyword in first 100 words
- [ ] Target keyword in at least one H2
- [ ] Meta description present (150-160 chars)
- [ ] Meta description includes keyword
- [ ] Headers properly structured (H1 > H2 > H3, no skipping)
- [ ] Internal links to related content
- [ ] External links to authoritative sources
- [ ] Images have alt text (if applicable)

## Review Output Template

```yaml
---
reviewed: {ISO timestamp}
content_file: {relative path}
content_type: {blog|email|linkedin|landing-page}
status: {pass|needs_revision|blocked}
reviewer: content_reviewer
---

# Content Review: {Title}

## Summary

| Category | Blockers | Warnings | Suggestions |
|----------|----------|----------|-------------|
| Typos/Grammar | {n} | {n} | {n} |
| Legal | {n} | {n} | {n} |
| Factual | {n} | {n} | {n} |
| SEO | {n} | {n} | {n} |
| **Total** | **{n}** | **{n}** | **{n}** |

**Status**: {PASS / NEEDS REVISION / BLOCKED}

## Blockers (MUST FIX before publishing)

### 1. {Issue title}
- **Location**: Line {X}, "{exact text}"
- **Category**: {legal|factual|typo|seo}
- **Issue**: {description of the problem}
- **Risk**: {potential consequence if not fixed}
- **Fix**: {specific recommendation}

## Warnings (SHOULD FIX)

### 1. {Issue title}
- **Location**: Line {X}
- **Category**: {category}
- **Issue**: {description}
- **Fix**: {recommendation}

## Suggestions (CONSIDER for quality)

### 1. {Suggestion}
- **Location**: Line {X}
- **Suggestion**: {improvement idea}

## Legal Checklist

- [ ] No unverified claims about competitors
- [ ] No medical/financial advice without disclaimers
- [ ] All statistics have sources cited
- [ ] No potentially defamatory statements
- [ ] Copyright compliance (quotes attributed, images licensed)
- [ ] No PII exposure

## Factual Verification Log

| Claim | Line | Source Cited | Verified | Notes |
|-------|------|--------------|----------|-------|
| "{claim text}" | {n} | {yes/no} | {yes/no/unable} | {verification details} |

---
*Reviewed: {timestamp} by content_reviewer agent*
```

### 5. Flow & Structure

**Check for:**

- Ideas introduced in one section that are never resolved or addressed in a later section (orphaned concepts)
- Problems listed in one section that aren't matched by solutions in a corresponding section
- Non-linear jumps between unrelated ideas without transitions
- Sections that don't build on each other logically
- Repetitive back-and-forth between the same ideas

**Process:**

1. List all concepts, problems, or promises introduced in each section
2. Verify each is resolved, addressed, or intentionally left open by the end
3. Check that sections follow a logical progression (setup → development → resolution)
4. Flag any structural gaps where the reader would be left wondering "what happened to X?"

**Severity:**

- BLOCKER: Key promises or problems introduced but never resolved (e.g., 4 problems listed, only 2 addressed)
- WARNING: Minor structural jumps that may confuse the reader
- SUGGESTION: Reordering that would improve readability

## Severity Definitions

**BLOCKER** - Content CANNOT be published:

- Legal liability risk
- Factual errors that damage credibility
- Critical typos (wrong numbers, names, dates, company names)

**WARNING** - Content SHOULD be fixed:

- Minor inaccuracies that don't affect core message
- Style inconsistencies
- Non-critical typos in body text

**SUGGESTION** - Optional improvements:

- Better word choices
- Structural improvements
- Enhanced clarity
- SEO optimizations
