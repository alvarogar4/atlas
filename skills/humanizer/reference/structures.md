# Structures

Sentence and paragraph shape patterns. A linter cannot find these: they live in the shape of the writing, not in its vocabulary, which is why they survive a word-level pass and still read as AI.

Apply these during generation. Patterns 25 to 29 in particular cannot be fixed afterwards without a rewrite.

| # | Pattern |
| --- | --- |
| 3 | Superficial Analyses with -ing Endings |
| 6 | Outline-like "Challenges and Future Prospects" Sections |
| 8 | Avoidance of "is"/"are" (Copula Avoidance) |
| 9 | Negative Parallelisms |
| 10 | Rule of Three Overuse |
| 11 | Elegant Variation (Synonym Cycling) |
| 12 | False Ranges |
| 25 | Uniform paragraph lengths |
| 26 | Uniform sentence lengths |
| 27 | Parallel section structures |
| 28 | Uniform information density |
| 29 | Too-clean logical flow |
| 34 | Rhetorical Setups |
| 38 | False Agency |
| 39 | Passive Voice and the Hidden Actor |
| 40 | Narrator-from-a-Distance |
| 41 | Wh- Sentence Starters |
| 42 | Dramatic Fragmentation |
| 43 | Pull-Quote Sentences |

---

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**

> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**

> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**

> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**

> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## LANGUAGE AND GRAMMAR PATTERNS

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**

> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**

> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 9. Negative Parallelisms

**Problem:** Any sentence pair where the first negates and the second affirms in parallel structure. "Not only...but...", "It's not just about X, it's Y", and every variant below. This is one of the strongest AI tells and it survives casual review because each variant looks different on the page.

**The full family.** All of these are the same pattern. Do not treat this as an exact-phrase list, treat it as a shape: negate, then reveal.

| Pattern                                                   | Problem                       |
| --------------------------------------------------------- | ----------------------------- |
| "Not because X. Because Y." / "Not because X, but because Y." | Telegraphed reversal          |
| "[X] isn't the problem. [Y] is."                          | Formulaic reframe             |
| "The answer isn't X. It's Y."                             | Predictable pivot             |
| "The question isn't X. It's Y."                           | Rhetorical misdirection       |
| "It feels like X. It's actually Y."                       | Setup and reveal cliche       |
| "We weren't X. We were Y."                                | Same shape, first person past |
| "Not X. But Y." / "not X, it's Y" / "isn't X, it's Y"     | Mechanical contrast           |
| "It's not this. It's that."                               | Same formula, different words |
| "stops being X and starts being Y"                        | False transformation arc      |
| "doesn't mean X, but actually Y"                          | Negation then assertion       |
| "is about X but not Y"                                    | False distinction             |
| "not just X but also Y"                                   | Additive hedge                |

**Negative listing.** The multi-beat version, a rhetorical striptease. "Not a X... Not a Y... A Z." and "It wasn't X. It wasn't Y. It was Z." State Z. The reader does not need the runway.

**Fix:** state the affirmative directly and drop the negation entirely. If the negated half carries real information, it belongs in its own sentence with its own reason, not as a setup beat.

**Before:**

> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement. We weren't experimenting with the format. We were betting on it.

**After:**

> The heavy beat adds to the aggressive tone. We bet the whole record on the format.

---

### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**

> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**

> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**

> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**

> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**

> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**

> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## STYLE PATTERNS

---

### 25. Uniform paragraph lengths

**How to detect:** 4+ consecutive paragraphs within ~20% of the same word count.

**Problem:** LLMs produce paragraphs of remarkably similar length. Real writing has natural variance: a one-sentence paragraph followed by a five-sentence one, a dense technical block followed by a short aside.

**Before:**

> ClickHouse stores data in columnar format. Each column is compressed independently and read separately during queries. This means queries that touch few columns skip the rest entirely, which reduces I/O significantly.
>
> The MergeTree engine sorts data on disk by the ORDER BY key. A sparse index maps key ranges to granules of 8,192 rows. Queries use this index to skip irrelevant granules, which is how ClickHouse achieves fast scans.
>
> Background merges combine small parts into larger ones over time. This process is asynchronous and heuristic-based. During merges, the engine applies any special logic defined by the engine variant being used.

**After:**

> ClickHouse stores data in columnar format. Each column is compressed independently, read separately. Queries that touch three columns on a 200-column table skip the other 197 entirely.
>
> The MergeTree engine sorts data on disk by the ORDER BY key and maps key ranges to granules of 8,192 rows via a sparse index. This is how it achieves fast scans without reading everything.
>
> Then there are background merges.
>
> They run asynchronously, combining small parts into larger ones. The timing is heuristic, not deterministic, which catches people off guard. You insert a row, and for some period of time both the old and new version exist. How long? Depends on load, part sizes, and merge scheduling. I've seen it take seconds and I've seen it take hours.

---

### 26. Uniform sentence lengths

**How to detect:** Most sentences cluster around 15-20 words with low variance. Compute the standard deviation of sentence word counts across a section.

**Problem:** LLMs gravitate toward a narrow band of sentence length. Human writing has much higher variance: a 4-word sentence next to a 30-word one.

**The trap:** the fix for uniformity is variance, not staccato. Stacking short punchy sentences for drama is its own tell (pattern 42). One short sentence among long ones is rhythm. Four in a row is a tell. Vary length by varying what each sentence has to carry, not by chopping.

**Before:**

> The system processes incoming data in real time. It validates each record against the schema definition. Invalid records are sent to a dead letter queue. The pipeline then aggregates valid records by key.

**After:**

> The system processes incoming data in real time, validating against the schema and routing invalid records to a dead letter queue before aggregating what survives by key. That holds until someone changes the schema mid-stream, at which point every consumer downstream starts rejecting rows it accepted an hour ago.

---

### 27. Parallel section structures

**How to detect:** Multiple sections follow the same template (intro sentence, explanation, list, summary). Each section opens the same way or uses the same rhetorical device.

**Problem:** LLMs generate sections as independent completions from similar prompts, producing mirror-image structures. Real articles have sections with distinct shapes: one might be a narrative, the next a code walkthrough, the next a short opinionated aside.

**Before:**

> ## Feature A
>
> Feature A is an important capability. It works by doing X. Here are the key benefits:
>
> - Benefit 1
> - Benefit 2
> - Benefit 3
>
> ## Feature B
>
> Feature B is an important capability. It works by doing Y. Here are the key benefits:
>
> - Benefit 1
> - Benefit 2
> - Benefit 3

**After:**

> ## Feature A
>
> Feature A does X. We shipped it after three customers independently asked for the same thing in the same week.
>
> ## Feature B
>
> I almost cut this one. The implementation took twice as long as Feature A and the usage numbers were mediocre for the first month. Then one enterprise customer built their entire workflow around it, and now it's our most-retained feature.

---

### 28. Uniform information density

**How to detect:** Every paragraph is equally packed with facts, data, or claims. No breathing room, no reflection, no opinion paragraphs.

**Problem:** LLMs maximize information per token. Human writing alternates between dense technical content and lighter opinion, reflection, or narrative. The variation is what makes it readable.

**Before:**

> ReplacingMergeTree deduplicates by ORDER BY key during background merges. Dedup is eventual, not immediate. Queries must use FINAL or explicit GROUP BY to handle pre-merge duplicates. FINAL has been multi-threaded since v22.6. The setting do_not_merge_across_partitions_select_final=1 reduces overhead by 7x.

**After:**

> ReplacingMergeTree deduplicates by ORDER BY key during background merges. The catch: dedup is eventual, not immediate. Between insert and merge, both rows exist.
>
> This is where PostgreSQL habits break. There's no atomic UPDATE. You insert the new row and wait.
>
> Queries must use FINAL or explicit GROUP BY. FINAL used to be painfully slow (~10x penalty), but since v22.6 it's multi-threaded. Setting `do_not_merge_across_partitions_select_final=1` can reduce overhead by another 7x.

---

### 29. Too-clean logical flow

**How to detect:** Every paragraph follows logically from the previous one. No tangents, no self-corrections, no asides. The argument moves in a perfectly straight line from A to B to C.

**Problem:** Real writing has controlled messiness: the author doubles back, qualifies a previous statement, introduces a tangent, or admits uncertainty. LLMs optimize for coherence, which paradoxically makes text feel less human.

**Before:**

> First, choose your engine based on your data pattern. Second, design your ORDER BY to serve both queries and engine semantics. Third, set your partition key. Fourth, add materialized views if needed. Following these steps ensures a well-designed schema.

**After:**

> Start with the engine. That part is usually straightforward.
>
> ORDER BY is where it gets interesting, because it has to serve two masters: query performance and engine semantics. I'll come back to this. It causes more production incidents than the other decisions combined.
>
> Partition key comes next, and for most tables `toYYYYMM(timestamp)` is the right answer. I have watched teams spend a week tuning partition strategy on tables where it changed nothing measurable.

---

## DIRECTNESS PATTERNS

Patterns 30 to 34 all share one failure: the sentence announces that content is coming instead of delivering it. Cut the announcement and keep the content.

---

### 34. Rhetorical Setups

**Words to watch:** "What if [reframe]?", "Here's what I mean:", "Think about it:", "And that's okay.", "Sound familiar?", "But wait."

**Problem:** These announce insight rather than deliver it. "What if" reframes are Socratic posturing, "Think about it" is condescending, and "And that's okay" grants permission nobody asked for.

**Rhetorical questions** get one per piece at most, and only if the answer does not arrive in the next sentence. A question answered immediately is a statement wearing a costume.

**Before:**

> What if the bottleneck was never the query engine? Think about it: your data model was wrong the whole time. And that's okay.

**After:**

> The query engine was never the bottleneck. The data model was, and most teams find that out after they have already paid for a bigger cluster.

---

## PRECISION PATTERNS

---

### 38. False Agency

**Problem:** giving inanimate things human verbs. Complaints do not become fixes, decisions do not emerge, cultures do not shift. A person does something. AI reaches for this construction because it avoids naming an actor it does not know.

| Pattern                        | Problem                                              |
| ------------------------------ | ---------------------------------------------------- |
| "a complaint becomes a fix"    | The complaint did nothing. Someone fixed it.         |
| "the decision emerges"         | Decisions do not emerge. Someone decides.            |
| "the culture shifts"           | Cultures do not shift. People change behavior.       |
| "the conversation moves toward" | Conversations do not move. Someone steers.          |
| "the data tells us"            | Data sits there. Someone reads it and concludes.     |
| "the market rewards"           | Markets do not reward. Buyers pay for things.        |
| "the architecture demands"     | Architecture does not demand. An engineer decided.   |

**Fix:** name the human. "The team shipped the fix that week" beats "the complaint becomes a fix." If no specific person fits, use "you" and put the reader in the seat.

**Before:**

> The data tells us the query pattern changed, and the architecture demands a new sort key.

**After:**

> We read the query log and found the pattern had changed. You will need a new sort key.

---

### 39. Passive Voice and the Hidden Actor

**Problem:** passive voice hides who did the thing and drains energy from the sentence. It is also the default register of corporate blame avoidance, which readers hear.

| Pattern                   | Fix                    |
| ------------------------- | ---------------------- |
| "X was created"           | Name who created it    |
| "It is believed that"     | Name who believes it   |
| "Mistakes were made"      | Name who made them     |
| "The decision was reached" | Name who decided      |
| "Records are sent to"     | Name what sends them   |

**Exception:** passive is correct when the actor is unknown or irrelevant, or when the object is the real subject of the paragraph ("the table is partitioned by month" is fine).

**Before:**

> The schema was migrated last quarter and several issues were identified during the rollout.

**After:**

> We migrated the schema last quarter. Support found four issues in the first week, all of them nullable columns that had never been nullable.

---

### 40. Narrator-from-a-Distance

**Words to watch:** "Nobody designed this.", "This happens because...", "This is why...", "People tend to...", "There's a reason...", "Teams often find..."

**Problem:** the lecturer voice, floating above the scene. It describes a situation the reader is standing in as though observing it from orbit.

**Fix:** put the reader in the room. "You don't sit down one day and decide to build a distributed system" beats "Nobody designed this." Second person beats "people."

**Before:**

> People tend to over-partition. This happens because teams optimize for the wrong metric. There's a reason this keeps recurring.

**After:**

> You partition by day because it feels safer, then three years later you have 1,095 partitions and every query pays for the fan-out.

---

### 41. Wh- Sentence Starters

**Problem:** sentences opening with What, When, Where, Which, Who, Why, or How become a crutch that delays the subject. "What makes this hard is the sort key" is three words of scaffolding before the content.

**Fix:** restructure. Lead with the subject or the verb. "What makes this hard is..." becomes "The sort key is the hard part" or better, name the specific constraint.

**Also:** paragraphs starting with "So", and sentences starting with "Look,".

**Before:**

> What most teams discover is that the sort key matters more than the engine. How you order columns is what determines scan cost.

**After:**

> The sort key matters more than the engine choice. Column order determines scan cost.

---

### 42. Dramatic Fragmentation

**Problem:** sentence fragments deployed for emphasis read as manufactured profundity. One fragment in a section is rhythm. Two is a habit. Three is a tell.

| Pattern                              | Problem                 |
| ------------------------------------ | ----------------------- |
| "[Noun]. That's it. That's the [thing]." | Performative simplicity |
| "X. And Y. And Z."                   | Staccato drama          |
| "This unlocks something. [Word]."    | Artificial revelation   |
| "Not always. Not perfectly."         | Hedging as reassurance  |

**Budget:** max one fragment per section, never stacked, never as a paragraph ender. Paragraph-ending fragments are the specific form AI detectors catch, because LLMs use them to close almost every paragraph.

**Interaction with pattern 26:** varying sentence length is required. Chopping sentences into fragments is not how you do it. Vary by varying what each sentence carries.

**Before:**

> Speed. Quality. Cost. You can only pick two. That's it. That's the tradeoff.

**After:**

> You get two of speed, quality, and cost. Every team that has tried for all three has shipped late and shipped it broken.

---

### 43. Pull-Quote Sentences

**Problem:** sentences engineered to be quotable. They read as written for a screenshot rather than for the paragraph they sit in, and they are the single most recognizable LinkedIn-slop signature.

**How to detect:** read each sentence alone. If it works as a standalone graphic with the author's name under it, it is a pull-quote. Aphorisms, chiasmus ("X isn't about Y, Y is about X"), and any sentence that generalizes far beyond the surrounding evidence.

**Fix:** rewrite it as a claim tied to the specific case in front of you.

**Before:**

> Data doesn't lie, but the people reading it do. Every dashboard is a story someone chose to tell.

**After:**

> The dashboard showed a 40% conversion lift because it filtered out the cohort that churned in week one. The filter was added by the person whose bonus depended on the number.

---

## SCORING

Use this on the review pass, after the checklist scan. Rate the draft 1-10 on each dimension.

| Dimension    | Question                                             |
| ------------ | ---------------------------------------------------- |
| Directness   | Does it state things, or announce that it will?      |
| Rhythm       | Varied, or metronomic?                               |
| Trust        | Does it respect the reader's intelligence?           |
| Authenticity | Does it sound like a person who did the work?        |
| Density      | Is anything cuttable without loss?                   |

Below 35/50: revise before showing the user. Below 40/50 on content going to a public channel: revise.

Scoring is not a substitute for the checklist scan. It catches the failures that survive a pattern-by-pattern pass because they live in the aggregate rather than in any single sentence.

---

## Process

1. Read the input text carefully
2. **Mandatory systematic checklist scan.** Go through all 43 patterns one by one. For each pattern: read its description, then scan the entire text looking specifically for that pattern. Do NOT do a "read and spot what jumps out" pass. That catches obvious issues but misses subtle variants. Check for **variant forms**, not just the exact examples listed. Every pattern must be actively searched for across every paragraph.
3. Rewrite each problematic section
4. Ensure the revised text:
   - Sounds natural when read aloud
   - Varies sentence structure naturally
   - Uses specific details over vague claims
   - Maintains appropriate tone for context
   - Uses simple constructions (is/are/has) where appropriate
   - Stays inside the voice budgets (adverbs, fragments, first-person openers, rhetorical questions)
5. **Score it.** Rate the draft on the five dimensions in the SCORING section. Below 35/50, revise and scan again before presenting.
6. Present the humanized version

## Output Format

Provide:

1. The rewritten text
2. A brief summary of changes made (optional, if helpful)

---

## Full Example

**Before (AI-sounding):**

> Great question! Here is an essay on this topic. I hope this helps!
>
> AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development. In today's rapidly evolving technological landscape, these groundbreaking tools—nestled at the intersection of research and practice—are reshaping how engineers ideate, iterate, and deliver, underscoring their vital role in modern workflows.
>
> At its core, the value proposition is clear: streamlining processes, enhancing collaboration, and fostering alignment. It's not just about autocomplete; it's about unlocking creativity at scale, ensuring that organizations can remain agile while delivering seamless, intuitive, and powerful experiences to users. The tool serves as a catalyst. The assistant functions as a partner. The system stands as a foundation for innovation.
>
> Industry observers have noted that adoption has accelerated from hobbyist experiments to enterprise-wide rollouts, from solo developers to cross-functional teams. The technology has been featured in The New York Times, Wired, and The Verge. Additionally, the ability to generate documentation, tests, and refactors showcases how AI can contribute to better outcomes, highlighting the intricate interplay between automation and human judgment.
>
> - 💡 **Speed:** Code generation is significantly faster, reducing friction and empowering developers.
> - 🚀 **Quality:** Output quality has been enhanced through improved training, contributing to higher standards.
> - ✅ **Adoption:** Usage continues to grow, reflecting broader industry trends.
>
> While specific details are limited based on available information, it could potentially be argued that these tools might have some positive effect. Despite challenges typical of emerging technologies—including hallucinations, bias, and accountability—the ecosystem continues to thrive. In order to fully realize this potential, teams must align with best practices.
>
> In conclusion, the future looks bright. Exciting times lie ahead as we continue this journey toward excellence. Let me know if you'd like me to expand on any section!

**After (Humanized):**

> AI coding assistants speed up some tasks. In a 2024 study by Google, developers using Codex completed simple functions 55% faster than a control group, but showed no improvement on debugging or architectural decisions.
>
> The tools are good at boilerplate: config files, test scaffolding, the fourth CRUD endpoint that looks like the previous three. They are bad at knowing when they are wrong. I have mass-accepted suggestions that compiled, passed lint, and still did the wrong thing because I stopped reading.
>
> Mira, an engineer at a fintech startup I interviewed, said she uses Copilot "like autocomplete for boring code" but reviews every line before committing. Jake, a senior dev at a larger company, disabled it after it kept suggesting patterns from a deprecated internal library.
>
> The productivity claims are hard to verify. GitHub says Copilot users "accept 30% of suggestions," though an accepted suggestion still has to survive review. The 2024 Uplevel study found no measurable difference in pull-request throughput between teams with and without AI assistants.
>
> The tools earn their place and they need supervision. Without a test suite you cannot tell whether a suggestion is right, which was already true before Copilot shipped. The assistant just produces wrong code faster than you used to.

**Changes made:**

- Removed chatbot artifacts ("Great question!", "I hope this helps!", "Let me know if...")
- Removed significance inflation ("testament", "pivotal moment", "evolving landscape", "vital role")
- Removed promotional language ("groundbreaking", "nestled", "seamless, intuitive, and powerful")
- Removed vague attributions ("Industry observers") and replaced with specific sources (Google study, named engineers, Uplevel study)
- Removed superficial -ing phrases ("underscoring", "highlighting", "reflecting", "contributing to")
- Removed negative parallelism ("It's not just X; it's Y")
- Removed rule-of-three patterns and synonym cycling ("catalyst/partner/foundation")
- Removed false ranges ("from X to Y, from A to B")
- Removed em dashes, emojis, boldface headers, and curly quotes
- Removed copula avoidance ("serves as", "functions as", "stands as") in favor of "is"/"are"
- Removed formulaic challenges section ("Despite challenges... continues to thrive")
- Removed knowledge-cutoff hedging ("While specific details are limited...")
- Removed excessive hedging ("could potentially be argued that... might have some")
- Removed filler phrases ("In order to", "At its core")
- Removed generic positive conclusion ("the future looks bright", "exciting times lie ahead")
- Replaced media name-dropping with specific claims from specific sources
- Removed adverbs and intensifiers, and cut the confessional register ("genuinely", "honestly")
- Named the actor instead of letting tools and data act on their own
- Cut the pull-quote closer ("acceptance is not correctness, and correctness is not value")
- Used simple sentence structures and concrete examples

---

## Reference

Word and phrase patterns (1-24) are based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Structural patterns (25-29) are original additions based on observed AI detector behavior and content that was flagged despite passing word-level humanizer checks.

Directness, precision, and agency patterns (30-43), the voice budgets, and the scoring rubric are adapted from [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya (MIT), merged in after review feedback that word-level checks were leaving structural and voice-level tells in published drafts.

Original skill by [@blader](https://github.com/blader/humanizer). Forked and extended for the atlas marketing content workflow.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

---
