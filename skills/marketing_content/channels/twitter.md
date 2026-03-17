# Twitter/X Writing Guidelines

## Character Limits

| Element        | Limit            |
| -------------- | ---------------- |
| Tweet          | 280 characters   |
| Thread         | Unlimited tweets |
| Optimal thread | 5-15 tweets      |
| Image alt text | 1,000 characters |

## The First Tweet Rule

The first tweet MUST stand alone. It should:

- Hook the reader immediately
- Make sense without the thread
- Work as a standalone viral tweet
- Create curiosity for the thread

### First Tweet Formulas

```
[Bold/Contrarian statement or question]

A thread:
```

or

```
[Numbered promise]

Here's what I learned:
```

### Hook Techniques

| Technique     | Example                                             |
| ------------- | --------------------------------------------------- |
| Contrarian    | "Hustle culture is killing your startup."           |
| Numbered list | "10 lessons from building a $10M company:"          |
| Question      | "Why do 90% of startups fail?"                      |
| Story setup   | "In 2019, I lost everything. Here's how I rebuilt:" |
| Bold claim    | "Email marketing is dead. Here's what's next:"      |
| Promise       | "I'll explain compound interest in 60 seconds:"     |
| Achievement   | "I went from $0 to $1M ARR. Here's the playbook:"   |

## Thread Structure (7-12 Tweets)

```
Tweet 1: HOOK
- Bold statement or promise
- Must work standalone
- "A thread:" or "Here's what I learned:"

Tweet 2-3: CONTEXT
- Set up the story/problem
- Why should they care?

Tweet 4-N: VALUE
- One point per tweet
- Numbered for scanability
- Examples and specifics

Tweet N-1: SUMMARY
- Key takeaway, tie it together

Tweet N: CLOSE
- Strong closing thought, or
- CTA adapted to brand voice
```

### Tweet Formatting

**Each tweet should:**

- Have one main idea
- Be readable independently
- Flow to the next tweet
- Use numbers when listing points

**Good tweet structure:**

```
[NUMBER]. [POINT]

[Brief explanation or example]
```

## Single Tweet Formulas

**The Observation:**

```
I noticed something interesting about [topic]:

[Observation with specific detail]

[What it means]
```

**The Tip:**

```
[Topic] tip that changed my life:

[The tip]

[Why it works]
```

**The Contrarian:**

```
Unpopular opinion:

[Contrarian take]

Here's why:
```

## Formatting Tips

### Line Breaks

Use line breaks to create rhythm:

**Bad:**

```
Here's what I learned about writing online. First, be consistent. Second, be specific. Third, be yourself.
```

**Good:**

```
Here's what I learned about writing online:

Be consistent.
Be specific.
Be yourself.

These 3 things > everything else.
```

### Symbols and Formatting

| Symbol | Use For              |
| ------ | -------------------- |
| →      | Transitions, results |
| •      | Bullet lists         |
| ↓      | Continue reading     |
| 1/     | Thread numbering     |

## Image Requirements

At least 1 image per post for the first tweet in a thread. The typical approach is an AI-generated image with a schema overlay — combining visual appeal with content value. Generate the image prompt and schema as part of the draft and save to `${CONTENT_FOLDER}/resources/`.

| Content Type    | Image?      | Why                       |
| --------------- | ----------- | ------------------------- |
| Thread hook     | Optional    | Can increase engagement   |
| Tutorial thread | Recommended | Screenshots help explain  |
| Data/stats      | Recommended | Charts are more shareable |
| Quote tweet     | No          | Focus on text             |

- Use 16:9 or 1:1 aspect ratios
- Keep text on images minimal
- Add alt text for accessibility

## CTA Strategies

### End of Thread CTAs

Adapt to brand voice. Common patterns:

- **Minimal**: "If this was useful, follow."
- **Action-oriented** (product): "Try it free at [link]"
- **Engagement** (community): Ask a genuine question related to the content
- **Strong close**: End with a takeaway that stands on its own — no CTA needed

Always check `brand-voice.md` for the project's preferred CTA style.

## Thread Pacing

- Each tweet should earn the next
- Cut tweets that don't add value
- 7-12 tweets is the sweet spot
- End before they're bored

## Twitter Post Frontmatter

```yaml
---
channel: "twitter"
topic: "{topic}"
project: { project }
status: draft
created: { ISO timestamp }
thread_length: { number of tweets }
first_tweet_preview: "{first tweet content}"
---
```

## Twitter Quality Checklist

- [ ] First tweet hooks and works standalone
- [ ] Each tweet is under 280 characters
- [ ] One main idea per tweet
- [ ] Thread flows logically
- [ ] Numbers/bullets for scanability
- [ ] Specific examples, not generic advice
- [ ] Clear CTA at the end
- [ ] Thread is 7-12 tweets (or justified if longer)
- [ ] No filler tweets
- [ ] Would you retweet this?

## What to Avoid

- First tweet that needs context from thread
- Tweets that just say "Let me explain:"
- Too many emojis
- Padding threads to hit a number
- Vague, generic advice
- Threads longer than 15 tweets without exceptional value
- "Thread time!" as a hook
- Hashtags in threads (they look spammy on most personal brands)
- Generic engagement questions that don't serve the content
