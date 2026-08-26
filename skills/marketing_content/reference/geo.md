# GEO: Generative Engine Optimization

Structuring content so answer engines (ChatGPT, Claude, Perplexity, Google AI Mode/AI Overviews, Copilot) can retrieve, quote, and cite it.

GEO does not replace the SEO rules in `channels/blog.md`. It targets a different retrieval mechanic and mostly changes **structure and information order**, not keywords.

## Why the structure rules exist

Answer engines do not rank pages, they retrieve passages. A page is split into chunks, each chunk is scored independently against the query, and the strongest individual passages get cited.

The consequence drives every rule below: **a page with strong average quality but weak passage structure loses to a page with clear, self-contained sections.** Every section has to survive being read alone, lifted out of the page, with none of the paragraphs above it for context.

Two tests to apply while writing:

| Test              | Question                                                                    |
| ----------------- | --------------------------------------------------------------------------- |
| Extraction test   | If this section is quoted alone, does it still answer something?             |
| Antecedent test   | Does this section resolve its own pronouns, or does it lean on the one above? |

## Article structure

```
1. Hero image (schema or diagram, per channels/blog.md image rules)
2. Answer capsule          <- the opening paragraph, above the fold
3. Table of contents
4. H2 sections             <- each opens by answering its own question
5. FAQ (H2, questions as H3)
6. Sources
```

### Answer capsule

The first paragraph after the title. It answers the article's core question completely and on its own.

| Rule            | Detail                                                                       |
| --------------- | ---------------------------------------------------------------------------- |
| Length          | 40-80 words                                                                  |
| Position        | Directly after H1/hero, before the table of contents                         |
| Self-contained  | Names the subject explicitly. No "it", "this approach", "the tool"           |
| Concrete        | At least one number, version, date, or named entity                          |
| Unlabeled       | No "TL;DR:" prefix. Write it as the opening paragraph                        |
| Resolves        | Answers the question, does not tease it                                      |

A capsule is not a hook. If the paragraph opens a loop instead of closing one, it is a hook. Both can exist in the same article: capsule first, hook paragraph second, then the article proper.

**Weak** (teases, needs the page around it):

> Choosing a database is one of the hardest calls a data team makes. In this guide we break down what actually matters.

**Strong** (answers, survives extraction):

> ClickHouse handles analytical queries over billions of rows in under a second, but it has no transactional guarantees and updates are asynchronous. Pick it for dashboards, event analytics, and log search. Do not pick it as a primary application database. Postgres with a columnar extension covers the middle ground up to roughly 100GB.

### Section leads

Every H2 opens by resolving that section's question, then expands into detail. Inverted pyramid, applied per section rather than once per article.

> [!warning] This is information order, not a template
> A literal "every section starts with a summary paragraph" collides with humanizer patterns **6** (formulaic sections), **25** (uniform paragraph lengths), and **27** (parallel section structures). Answer-first governs *what information comes first*. It says nothing about the shape, length, or rhetorical device of the lead, and those must vary.

Vary the lead form across sections:

| Form         | Example                                                                        |
| ------------ | ------------------------------------------------------------------------------ |
| Direct claim | "Columnar storage cuts scan cost because a query reads 3 columns, not 200."     |
| Number first | "340ms. That is the same query on a 12-node cluster."                           |
| Definition   | "A materialized view here is an insert trigger, not a cached result."           |
| Verdict      | "Skip this one unless you are already running Kafka."                           |
| Contrast     | "Postgres solves this with an index. ClickHouse has no index to reach for."     |
| Concession   | "This is the part we got wrong for eight months."                               |

Never do:

- A literal `TL;DR:` label on each section
- The same lead form in consecutive sections
- Leads of near-identical length throughout
- One summary sentence template with the nouns swapped

### Self-containment

Each section names its own subject. Pronouns that reach back across an H2 boundary break the chunk.

> Before: "It handles this differently, and that has consequences for merges."
> After: "ClickHouse deduplicates asynchronously during background merges."

### FAQ

Placed after the article body, before sources.

| Rule       | Detail                                                                  |
| ---------- | ----------------------------------------------------------------------- |
| Count      | 4-8 questions                                                           |
| Format     | One H3 per question, phrased as a full spoken question                  |
| Answer     | 40-60 words, self-contained, answer in the first sentence               |
| Source     | Real questions: search suggestions, sales calls, support tickets, forums |
| Uniqueness | Cover adjacent questions the body does not already answer verbatim      |

Invented questions read as filler and get skipped. If there is no real question list, the FAQ waits for the first refresh pass rather than getting padded.

## Structured data

Two blocks in the page head.

**`Article` / `BlogPosting`**: `headline`, `description`, `datePublished`, `dateModified`, `author`, `publisher`.

**`FAQPage`**: mirrors the visible FAQ exactly. Never mark up questions that are not on the page.

Set expectations honestly. Google retired FAQ rich results on 7 May 2026, and the schema.org type remains valid. On AI citations, Ahrefs tracked 1,885 pages that added JSON-LD against 4,000 control pages and measured +2.4% on Google AI Mode, +2.2% on ChatGPT (both indistinguishable from zero) and -4.6% on AI Overviews (significant, and in the wrong direction). That study only covered pages already heavily cited, so it does not rule out a benefit for pages starting from zero, and Microsoft states schema helps Copilot parse content. Add the markup because it cleanly bounds each Q&A pair for extraction. Do not add it expecting a citation lift.

`dateModified` carries the freshness signal, so it has to stay in sync with the visible "Last updated" date on the page. A `dateModified` newer than the visible date is a mismatch worth avoiding.

**Skip `llms.txt`.** A 300,000-domain study found 10.13% adoption and no correlation with citation frequency, only 1 of the 50 most AI-cited domains had the file, and Google documented in June 2026 that it ignores it entirely. It is maintenance with no measured return.

## GEO-native formats

Two different numbers matter, and they point in different directions.

**Share of all citations** (Peec AI / Wix AI Search Lab, March 2026: 75,000 AI answers, 1,056,727 citations across ChatGPT, Google AI Mode, Perplexity):

| Format                        | Share of citations |
| ----------------------------- | ------------------ |
| Listicles                     | 21.9%              |
| Articles                      | 16.7%              |
| Product pages                 | 13.7%              |
| Comparison / alternative pages | under 3%           |

**Per-page citation rate** (MaxAEO, 61,400 citations over 8 weeks, 9,200 B2B/SaaS queries; vendor research, directional, not independently replicated):

| Format               | Citation rate |
| -------------------- | ------------- |
| Original-data study  | 71%           |
| Comparison page      | 64%           |
| Ranked listicle      | 61%           |

Read together: listicles win on **volume** because they match how people prompt ("best X for Y", "top tools for Z"). Comparison pages win on **rate** because far fewer exist and the ones that do get pulled in when someone is already choosing. Publish both. The listicle catches the broad prompt, the comparison page catches the buyer mid-decision.

Commercial intent skews harder still: listicles took 40.86% of citations on commercial queries in the Peec study.

### Comparison pages

```
1. Verdict capsule        <- who should pick which, in 40-80 words
2. Feature comparison table
3. One section per dimension that actually differs
4. Where the competitor wins
5. Who should not pick us
```

The table is the extractable unit. Engines lift tables whole, so it carries most of the citation weight:

- One claim per cell
- Concrete values over checkmarks. "8,192-row granules" beats a tick
- No empty cells. Write "Not supported" or "Manual only"
- A grid of ✓ and ✗ carries no meaning once separated from the page

Sections 4 and 5 are not humility exercises. A page that concedes nothing reads as marketing to both the reader and the engine, and balanced sources get cited over one-sided ones.

**Before writing one**, check `${PROJECT_PATH}/context.md` for trademark and naming rules on the competitor. `workflow/review.md` treats unsourced competitor claims as BLOCKING, so every comparative claim needs a dated source or a link to a reproducible benchmark you own.

### Pain-led pages

Start from the pain the reader types, not the capability being sold. "Queries keep OOM-ing on large joins" is a query someone runs. "Introducing our new memory manager" is not.

Pull pains from support tickets, sales objections, and competitor forum threads. Each pain becomes an H2, and the section answers it before positioning anything.

### Proprietary data

The strongest asset available, because it is the one thing an engine cannot find on another site. Benchmarks you ran, usage statistics, survey results, cost breakdowns, migration timings.

The original GEO research (Aggarwal et al., KDD 2024, ~10,000 queries across 9 datasets) found that adding statistics, quotations, and cited sources to source content produced 30-40% relative improvement in visibility, with statistics and quotation addition the two strongest single interventions. Cite inline. The same claim with a source outperforms the claim without one.

## Publishing and refresh cadence

Freshness is a real ranking input for answer engines. Content under 30 days old draws roughly 3.2x the AI citations, about half of all AI-cited content is under 13 weeks old, and comparison and category pages hold their citation frequency for 60-90 days before measurable decay.

Plan three substantive refresh passes at publish time and put them on the calendar:

| Pass    | When        | What changes                                                                      |
| ------- | ----------- | --------------------------------------------------------------------------------- |
| Publish | Day 0       | Complete article: capsule, sections, FAQ, hero, schema                            |
| Pass 1  | +2 weeks    | Add diagrams, expand the thinnest section with data                               |
| Pass 2  | +4-6 weeks  | Add FAQ entries from questions actually received, refresh any stat that moved     |
| Pass 3  | +8-12 weeks | Add proprietary data, or a section covering a query the page started surfacing for |

Every pass updates `dateModified`, updates the visible "Last updated" date, and records what changed in `5_results-blog.md`.

> [!warning] Publish complete, then improve
> A tempting variant of this is to ship a deliberately raw version and add the capsule, images, and FAQ later, manufacturing three freshness events. Do not. The first crawl indexes the weak version, and the page can be cited in that state for weeks before anything gets added. The staged schedule earns the same freshness signal without betting on the first version going unread.

A pass that only touches the date is detectable and worthless. Each one adds substance.

## GEO checklist

Applied during writing, verified during review.

- [ ] Answer capsule present, 40-80 words, self-contained, contains a concrete number or entity
- [ ] Capsule answers rather than teases
- [ ] Table of contents after the capsule
- [ ] Every H2 section leads with its own answer
- [ ] Lead forms vary across sections (no repeated template, no `TL;DR:` labels)
- [ ] No pronoun in a section opener refers back across an H2 boundary
- [ ] FAQ present with 4-8 real questions, each answered in 40-60 words
- [ ] `Article`/`BlogPosting` JSON-LD with `dateModified`
- [ ] `FAQPage` JSON-LD mirrors the visible FAQ exactly
- [ ] Visible "Last updated" date matches `dateModified`
- [ ] Statistics and quotes cited inline with sources
- [ ] Comparison content includes a populated table, competitor strengths, and who should not pick us
- [ ] Refresh passes scheduled on the calendar
- [ ] Humanizer patterns 6, 25, 27 verified against the section leads

## Sources

- [GEO: Generative Engine Optimization](https://arxiv.org/abs/2311.09735) - Aggarwal et al., KDD 2024
- [The content types most cited by LLMs](https://www.wix.com/studio/ai-search-lab/research/content-types-most-cited-by-llms) - Wix AI Search Lab / Peec AI, March 2026
- [Content formats for AI citations](https://maxaeo.ai/blog/content-formats-ai-citations/) - MaxAEO, 2026 (vendor research)
- [We tracked 1,885 pages adding schema](https://ahrefs.com/blog/schema-ai-citations/) - Ahrefs, 2026
- [Content chunking and AI extractability](https://www.lumar.io/blog/best-practice/content-chunking-ai-extractability-geo-aeo-explainer/) - Lumar
- [How content freshness affects AI citations](https://writesonic.com/blog/how-content-freshness-affects-ai-citations) - Writesonic, 2026
- [FAQ rich results deprecation](https://developers.google.com/search/blog) - Google, May 2026
