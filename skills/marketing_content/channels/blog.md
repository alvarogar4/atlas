# Blog Writing Guidelines

## Blog Structure

### Standard Blog Post

```
1. Hero image (schema or diagram)

2. Answer capsule (40-80 words)
   - Answers the article's core question completely, on its own
   - No "TL;DR:" label, this is just the opening paragraph

3. Table of contents

4. Introduction (150-200 words)
   - Hook: Grab attention immediately
   - Context: Why this matters to the reader
   - Promise: What they'll learn/gain
   - Transition: Lead into first section

5. Main Sections (3-5 sections, 300-500 words each)
   - One main idea per section
   - Opens by answering that section's own question, then expands
   - Subheadings for scannability
   - Examples and data to support claims
   - Citations with inline links

6. Conclusion (150-200 words)
   - Summary of key takeaways
   - Clear call-to-action
   - Secondary CTA (optional)

7. FAQ (4-8 real questions, one H3 each, 40-60 word answers)

8. Sources
```

The answer capsule, per-section leads, and FAQ are GEO requirements. See `reference/geo.md` for the rules behind each and the mandatory humanizer reconciliation.

### Word Count Targets

| Content Type   | Word Count  | Reading Time |
| -------------- | ----------- | ------------ |
| Short post     | 800-1,200   | 3-5 min      |
| Standard post  | 1,500-2,000 | 6-8 min      |
| Pillar content | 2,500-4,000 | 10-15 min    |
| Ultimate guide | 5,000+      | 20+ min      |

## SEO Requirements

### Title Optimization

- Include primary keyword
- Keep under 60 characters (Google truncates after 60)
- Front-load the keyword when possible
- Use power words: "Ultimate", "Complete", "Essential", numbers

### Meta Description

- 150-160 characters
- Include primary keyword naturally
- Include a call-to-action or benefit
- Make it compelling to click

### Heading Structure

```
H1: Title (only one per post)
  H2: Main section heading
    H3: Subsection heading
      H4: Detail heading (rare)
```

**Rules:**

- Never skip levels (H2 -> H4 is wrong)
- Primary keyword in at least one H2
- Use descriptive headings (not "Part 1", "Section A")

### Keyword Placement

| Location         | Requirement                |
| ---------------- | -------------------------- |
| Title (H1)       | Required - primary keyword |
| First 100 words  | Required - primary keyword |
| URL/slug         | Required - primary keyword |
| Meta description | Required - primary keyword |
| H2 headings      | At least one with primary  |
| Image alt text   | Where relevant             |
| Throughout body  | Natural usage, no stuffing |

## GEO Requirements

SEO targets ranked pages. GEO targets cited passages. Answer engines split a page into chunks, score each chunk independently, and quote the strongest ones, so a section that only makes sense in sequence never gets cited.

**Read `reference/geo.md` before writing or planning any blog post.** The rules below are the summary, that file has the reasoning, the evidence, and the failure modes.

### Required elements

| Element              | Rule                                                                     |
| -------------------- | ------------------------------------------------------------------------ |
| Answer capsule       | 40-80 words, first paragraph, self-contained, holds a concrete number    |
| Table of contents    | After the capsule                                                        |
| Section leads        | Every H2 answers its own question first, then expands                    |
| Self-containment     | No pronoun in a section opener reaching back across an H2 boundary       |
| FAQ                  | 4-8 real questions as H3, answers 40-60 words                            |
| `Article` JSON-LD    | Includes `dateModified`, synced with a visible "Last updated" date       |
| `FAQPage` JSON-LD    | Mirrors the visible FAQ exactly, never questions absent from the page    |
| Inline citations     | Every statistic and quote carries its source                             |

### Section leads collide with the humanizer

Answer-first governs **information order**, not paragraph shape. Writing "every section opens with a summary paragraph" as a template triggers humanizer patterns 6, 25, and 27 (formulaic sections, uniform paragraph lengths, parallel section structures).

Vary the lead across sections: a direct claim, a number, a definition, a verdict, a contrast, a concession. Never repeat a lead form in consecutive sections, never label a section `TL;DR:`, never run one summary template with the nouns swapped. The full table of lead forms is in `reference/geo.md`.

### GEO-native formats

Comparison pages, ranked listicles, and original-data posts are the formats answer engines cite most. Listicles carry the volume (21.9% of all citations), comparison pages carry the rate (64% per page). When the topic supports it, pick the format deliberately rather than defaulting to a standard article. Format specs are in `reference/geo.md`.

### Refresh cadence

Content under 30 days old draws roughly 3.2x the AI citations. Publish complete, then schedule three substantive refresh passes (+2 weeks, +4-6 weeks, +8-12 weeks) on the content calendar. Each pass updates `dateModified` and the visible date.

Do not publish a deliberately incomplete post to manufacture freshness events. The first crawl indexes the weak version.

## Hook Techniques (Blog-Specific)

1. **Speak directly**: "You're about to make a mistake..."
2. **Shocking stat**: "67% of blog posts get zero shares."
3. **Yes-trigger question**: "Ever felt like you're shouting into the void?"
4. **Personal story**: "Last Tuesday, I almost quit..."
5. **Analogy**: "Writing without structure is like driving without GPS"
6. **Contrarian**: "Everything you've heard about SEO is wrong."
7. **Newsjack**: "After Google's latest update..."
8. **Paint a picture**: "Imagine waking up to 10,000 new subscribers..."

### Open Loops

Create "mental gaps" that compel continued reading:

- "In a moment, I'll show you the exact formula..."
- "But first, you need to understand why this matters..."

**Close every loop.** Unresolved open loops = clickbait that destroys trust.

## Bucket Brigades

Short phrases that keep readers scrolling:

- "Here's the thing:"
- "But wait..."
- "Truth is:"
- "You might be wondering:"
- "Let me explain:"

**Usage:** 1-2 per 500 words.

## Internal Linking

- Link to 2-5 related posts per article
- Use descriptive anchor text (not "click here")
- Link early in the post for important pages
- Create content clusters around pillar topics

## External Linking

- Link to authoritative sources (research, stats, expert quotes)
- 2-5 external links per 1000 words
- Verify links work before publishing

## Formatting for Readability

- Max 3-4 sentences per paragraph
- One idea per paragraph
- Use single-sentence paragraphs for emphasis
- Visual break every 300-400 words (subheading, image, blockquote, bullet list)

### Image Requirements

Blog posts require visual assets as part of the draft. Prefer schemas and technical diagrams over AI-generated images — they carry more value, especially in technical articles where architecture diagrams, flowcharts, and data flows are essential.

- **Social card**: Always 1 (schema or diagram that captures the article's core concept)
- **In-content images**: Schemas and diagrams as needed. If the plan doesn't specify images, evaluate where architecture diagrams, flowcharts, comparison charts, or process flows would strengthen the piece
- **AI-generated images**: Use sparingly — only when no schema/diagram fits (e.g., non-tech articles, abstract concepts, mood/tone pieces)

All image prompts and assets go in `${CONTENT_FOLDER}/resources/`.

### Images and Diagrams

| Image Type                         | Tool                                          |
| ---------------------------------- | --------------------------------------------- |
| Architecture diagrams              | `atlas:marketing_visuals` (schema-generation) |
| Flowcharts, process flows          | `atlas:marketing_visuals` (schema-generation) |
| Comparison charts                  | `atlas:marketing_visuals` (schema-generation) |
| Conceptual/artistic illustrations  | `atlas:marketing_visuals` (ai-prompting)      |
| Photo cropping, background removal | `atlas:marketing_visuals` (processing)        |

All images go in `${CONTENT_FOLDER}/resources/` and are referenced as `./resources/{image}.png`.

## Blog Post Frontmatter

```yaml
---
channel: "blog"
title: "{Title from outline}"
slug: { url-slug }
meta_description: "{150-160 chars, includes primary keyword}"
keywords: [{ primary }, { secondary keywords }]
author: { from project context or "Author" }
status: draft
created: { ISO timestamp }
updated: { ISO date, maps to dateModified in schema }
project: { project }
word_count: { actual count }
target_word_count: { from outline }
geo_format: { standard | comparison | listicle | original-data }
refresh_passes: { scheduled dates for passes 1-3, or "unscheduled" }
---
```

## Blog Quality Checklist

- [ ] Hook grabs attention in first 2 sentences
- [ ] Primary keyword in title, first 100 words, and at least one H2
- [ ] Meta description is 150-160 chars with keyword
- [ ] Word count hits target (within 10%)
- [ ] All sections from outline are included
- [ ] Sources are cited with inline links
- [ ] Internal links to 2-5 related posts
- [ ] Images have alt text
- [ ] No orphan headings (single H3 under H2)
- [ ] Conclusion has clear CTA
- [ ] Read out loud - flows naturally

### GEO

- [ ] Answer capsule present, 40-80 words, self-contained, unlabeled
- [ ] Capsule answers the core question rather than teasing it
- [ ] Table of contents after the capsule
- [ ] Every H2 leads with that section's answer
- [ ] Lead forms vary across sections (humanizer 6, 25, 27 verified)
- [ ] No section opener depends on a pronoun from the previous section
- [ ] FAQ with 4-8 real questions, 40-60 word self-contained answers
- [ ] `Article` and `FAQPage` JSON-LD specified, `dateModified` set
- [ ] Visible "Last updated" date matches `dateModified`
- [ ] Refresh passes scheduled on the calendar

## Content Upgrades (Optional)

| Content Type   | Best Upgrade           |
| -------------- | ---------------------- |
| How-to guide   | Checklist/Cheatsheet   |
| Listicle       | Downloadable list      |
| Strategy guide | Template/Workbook      |
| Data post      | Spreadsheet/Calculator |

**Placement:** After the most valuable section, not at the end.
