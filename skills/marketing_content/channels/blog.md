# Blog Writing Guidelines

## Blog Structure

### Standard Blog Post

```
1. Introduction (150-200 words)
   - Hook: Grab attention immediately
   - Context: Why this matters to the reader
   - Promise: What they'll learn/gain
   - Transition: Lead into first section

2. Main Sections (3-5 sections, 300-500 words each)
   - One main idea per section
   - Subheadings for scannability
   - Examples and data to support claims
   - Citations with inline links

3. Conclusion (150-200 words)
   - Summary of key takeaways
   - Clear call-to-action
   - Secondary CTA (optional)
```

### Word Count Targets

| Content Type | Word Count | Reading Time |
|--------------|-----------|--------------|
| Short post | 800-1,200 | 3-5 min |
| Standard post | 1,500-2,000 | 6-8 min |
| Pillar content | 2,500-4,000 | 10-15 min |
| Ultimate guide | 5,000+ | 20+ min |

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

| Location | Requirement |
|----------|-------------|
| Title (H1) | Required - primary keyword |
| First 100 words | Required - primary keyword |
| URL/slug | Required - primary keyword |
| Meta description | Required - primary keyword |
| H2 headings | At least one with primary |
| Image alt text | Where relevant |
| Throughout body | Natural usage, no stuffing |

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

### Images and Diagrams

| Image Type | Tool |
|-----------|------|
| Architecture diagrams | `atlas:marketing:visuals` (schema-generation) |
| Flowcharts, process flows | `atlas:marketing:visuals` (schema-generation) |
| Comparison charts | `atlas:marketing:visuals` (schema-generation) |
| Conceptual/artistic illustrations | `atlas:marketing:visuals` (ai-prompting) |
| Photo cropping, background removal | `atlas:marketing:visuals` (processing) |

All images go in `${CONTENT_FOLDER}/resources/` and are referenced as `./resources/{image}.png`.

## Blog Post Frontmatter

```yaml
---
title: "{Title from outline}"
slug: {url-slug}
meta_description: "{150-160 chars, includes primary keyword}"
keywords: [{primary}, {secondary keywords}]
author: {from project context or "Author"}
status: draft
created: {ISO timestamp}
project: {project}
word_count: {actual count}
target_word_count: {from outline}
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

## Content Upgrades (Optional)

| Content Type | Best Upgrade |
|-------------|-------------|
| How-to guide | Checklist/Cheatsheet |
| Listicle | Downloadable list |
| Strategy guide | Template/Workbook |
| Data post | Spreadsheet/Calculator |

**Placement:** After the most valuable section, not at the end.
