# Examples

Before and after transformations. Read these when a pattern description is clear but the fix is not.

---

## Voice: clean but soulless, versus a pulse

Removing AI patterns is not the same as having a voice. Both versions below are free of banned
vocabulary. Only one sounds like a person who did the work.

**Before (clean but soulless):**

> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

**After (has a pulse):**

> The agents wrote three million lines of code overnight while the humans slept. Half the dev community called it the end of software engineering and the other half spent the morning explaining why generated line count measures nothing. Both camps have a point, which is the least satisfying place to land. I have run swarms overnight and read the diff in the morning: most of it is scaffolding, and the parts that are wrong take longer to find than they would have taken to write.

---

## Short transformations

### Throat-clearing and binary contrast (31, 9, 32)

**Before:**

> Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in.

**After:**

> Building products is hard. The technology is the manageable half.

---

### Filler and unnecessary reassurance (31, 22, 34)

**Before:**

> It turns out that most teams struggle with alignment. The uncomfortable truth is that nobody wants to admit they're confused. And that's okay.

**After:**

> Teams struggle with alignment because nobody wants to be the person who admits they are lost in the roadmap doc.

---

### Business jargon stack (30, 22, 32)

**Before:**

> In today's fast-paced landscape, we need to lean into discomfort and navigate uncertainty with clarity. This matters because your competition isn't waiting.

**After:**

> Ship the half-finished version this quarter. Two of your competitors already did.

---

### Dramatic fragmentation (42, 10)

**Before:**

> Speed. Quality. Cost. You can only pick two. That's it. That's the tradeoff.

**After:**

> You get two of speed, quality, and cost. Every team that has tried for all three shipped late and shipped it broken.

---

### Rhetorical setup (34, 41)

**Before:**

> What if I told you that the best teams don't optimize for productivity? Here's what I mean: they optimize for learning. Think about it.

**After:**

> The best teams optimize for learning. Productivity follows, about two quarters later than anyone wants.

---

### False agency and passive voice (38, 39)

**Before:**

> The data tells us the query pattern changed, and a decision was reached to migrate the schema.

**After:**

> We read the query log, saw the pattern had changed, and migrated the schema that week.

---

## Full transformation

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
