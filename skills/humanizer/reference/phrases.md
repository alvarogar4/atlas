# Phrases

Word and phrase level patterns. These are found by reading for specific words. Roughly half are caught mechanically by `tools/lint.sh`; the rest need you to read for intent.

Scan every paragraph for each pattern. Check for **variant forms**, not just the exact examples listed.

| # | Pattern |
| --- | --- |
| 1 | Undue Emphasis on Significance, Legacy, and Broader Trends |
| 2 | Undue Emphasis on Notability and Media Coverage |
| 4 | Promotional and Advertisement-like Language |
| 5 | Vague Attributions and Weasel Words |
| 7 | Overused "AI Vocabulary" Words |
| 19 | Collaborative Communication Artifacts |
| 20 | Knowledge-Cutoff Disclaimers |
| 21 | Sycophantic/Servile Tone |
| 22 | Filler Phrases |
| 23 | Excessive Hedging |
| 24 | Generic Positive Conclusions |
| 30 | Business Jargon |
| 31 | Throat-Clearing Openers |
| 32 | Emphasis Crutches |
| 33 | Meta-Commentary and Self-Referential Asides |
| 35 | Adverbs and Intensifiers |
| 36 | Lazy Extremes |
| 37 | Vague Declaratives |

---

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**

> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**

> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**

> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**

> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**

> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**

> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**

> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**

> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Pseudo-insight openers:** "the real unlock is", "the part nobody mentions is", "the bigger concern is", "here's the thing nobody talks about", "what most people miss is", "the real question is". These are fine when followed by actual insight or specific knowledge. They become AI slop when they frame obvious or generic statements as hidden wisdom.

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**Before:**

> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**

> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 19. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**

> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**

> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

### 20. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**

> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**

> The company was founded in 1994, according to its registration documents.

---

### 21. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**

> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**

> The economic factors you mentioned are relevant here.

---

## FILLER AND HEDGING

---

### 22. Filler Phrases

**Before → After:**

- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

---

### 23. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**

> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**

> The policy may affect outcomes.

---

### 24. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**

> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**

> The company plans to open two more locations next year.

---

## STRUCTURAL PATTERNS

AI detectors don't just look at words. They analyze statistical patterns across the whole text: sentence length distribution, paragraph uniformity, section symmetry, information density. These structural signals are harder to fix after the fact because they're baked into how the content was generated. Apply these rules during writing, not after.

---

### 30. Business Jargon

**Problem:** Consultant vocabulary that replaces a plain verb with a longer one. It signals effort without adding meaning.

| Avoid                  | Use instead         |
| ---------------------- | ------------------- |
| Navigate (challenges)  | Handle, address     |
| Unpack (analysis)      | Explain, examine    |
| Lean into              | Accept, commit to   |
| Landscape (context)    | Situation, field    |
| Game-changer           | Significant         |
| Double down            | Commit, increase    |
| Deep dive              | Analysis            |
| Take a step back       | Reconsider          |
| Moving forward         | Next, from now      |
| Circle back            | Return to, revisit  |
| On the same page       | Aligned, agreed     |
| Leverage (verb)        | Use                 |
| Surface (verb)         | Show, raise         |

**Before:**

> As we navigate this landscape, let's unpack the tradeoffs and lean into what the data tells us.

**After:**

> The tradeoffs are worth examining. Two of them decide the architecture.

---

### 31. Throat-Clearing Openers

**Words to watch:** "Here's the thing:", "Here's what/why/how [X]", "The uncomfortable truth is", "It turns out", "The real [X] is", "Let me be clear", "The truth is,", "I'll say it again:", "I'm going to be honest", "Can we talk about", "Here's what I find interesting", "Here's the problem though", "What most people miss is", "The real question is"

**Problem:** Any "here's what/this/that" construction announces a point before making it. The announcement carries no information and primes the reader to expect insight that the following sentence often fails to deliver.

**Test:** delete the opener. If the sentence still works, the opener was throat-clearing. It almost always still works.

**Before:**

> Here's the thing about columnar storage: it turns out that the real win isn't compression. What most people miss is that column pruning does the heavy lifting.

**After:**

> Column pruning does more for query speed than compression does. A query touching three columns of a 200-column table reads three columns.

---

### 32. Emphasis Crutches

**Words to watch:** "Full stop.", "Period.", "Let that sink in.", "This matters because", "Make no mistake", "Here's why that matters", "I keep coming back to", "And I mean that"

**Problem:** These instruct the reader to find the previous sentence important. A sentence that needs the instruction is not important enough to keep.

**Before:**

> Queries dropped from 40 seconds to 200 milliseconds. Let that sink in. This matters because your users notice every one of those seconds.

**After:**

> Queries dropped from 40 seconds to 200 milliseconds, which is the difference between a user waiting and a user not noticing.

---

### 33. Meta-Commentary and Self-Referential Asides

**Words to watch:** "Hint:", "Plot twist:", "Spoiler:", "You already know this, but", "But that's another post", "X is a feature, not a bug", "Dressed up as", "The rest of this essay explains...", "Let me walk you through...", "In this section, we'll...", "As we'll see...", "I want to explore...", "More on that later"

**Problem:** The piece narrates its own structure instead of moving. Readers do not need a table of contents in prose form.

**Note:** this is distinct from pattern 19. Pattern 19 is chatbot correspondence left in the text ("I hope this helps"). This one is the essay talking about itself.

**Before:**

> In this section, we'll walk through the merge process. Plot twist: it's not deterministic. More on that later.

**After:**

> Merges run on a heuristic schedule. Part sizes and current load decide when, which means the same insert can settle in two seconds or in two hours.

---

### 35. Adverbs and Intensifiers

**Rule:** default zero adverbs. Keep one only when it carries meaning no other word does ("the merge runs asynchronously" survives, "this is genuinely hard" does not).

**Ban list, no budget:** really, just, literally, genuinely, honestly, simply, actually, deeply, truly, fundamentally, inherently, inevitably, interestingly, importantly, crucially, incredibly, remarkably, notably

**Also cut these filler openers:** "At its core", "In today's [X]", "It's worth noting", "At the end of the day", "When it comes to", "In a world where", "The reality is"

**Problem:** adverbs add emphasis instead of information. "This is genuinely hard" tells the reader to believe difficulty. Showing the difficulty proves it. The confessional adverbs (genuinely, honestly, truly) are the worst offenders because they read as manufactured sincerity.

**Related failure, telling instead of showing:** "This is genuinely hard", "This is what leadership actually looks like", "That actually matters". Replace the claim with the thing that makes it true.

**Before:**

> This is genuinely hard. The migration was really complex and honestly took much longer than we simply expected.

**After:**

> The migration took eleven weeks. We had budgeted four, and the gap was almost entirely schema rewrites nobody scoped.

---

### 36. Lazy Extremes

**Words to watch:** every, always, never, everyone, everybody, nobody, all, none, any

**Problem:** absolutes claim authority the writer has not earned and the reader can disprove with one counterexample. They are also a hedge in disguise: "everyone knows" means "I did not check."

**Fix:** replace with the specific scope. "Every team struggles with this" becomes "three of the four teams I have onboarded hit this in week one."

**Before:**

> Everyone struggles with this. Nobody gets partitioning right the first time and it always causes problems.

**After:**

> Most teams I have onboarded get partitioning wrong on the first table. The usual failure is one partition per day on a table with three years of history.

---

### 37. Vague Declaratives

**Words to watch:** "The reasons are structural", "The implications are significant", "This is the deepest problem", "The stakes are high", "The consequences are real", "It runs deeper than that"

**Problem:** the sentence announces that something is important, deep, or structural without naming it. It is pattern 1 at sentence scale, and it reads as filler because it is.

**Test:** if a sentence claims significance without naming the specific thing, cut it or replace it with the specific thing.

**Before:**

> The implications for the data team are significant. The reasons are structural and the stakes are high.

**After:**

> The data team loses its Monday to re-running failed backfills. Two engineers, every week, on work that produces nothing new.

---

## AGENCY AND VOICE PATTERNS

---
