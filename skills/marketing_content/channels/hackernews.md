# Hacker News Show HN Writing Guidelines

The HN audience strongly favors open-source, privacy-first projects presented by creators who "talk to HN as fellow builders and engineers."

## The Golden Rule: No Marketing Language

Marketing language is an instant turnoff for HN. Modest, factual descriptions outperform superlatives. Write as a fellow developer, not a marketer.

## Title Format

### Title Formula

```
Show HN: [Product Name] - [clear use-case description]
```

### Title Rules

| Rule                 | Details                                                   |
| -------------------- | --------------------------------------------------------- |
| Start exactly with   | "Show HN: " (places you on the less-competitive Show tab) |
| Follow with          | Product name, then dash or comma                          |
| Describe             | Specific use-case in active voice                         |
| Keep tagline         | 50 characters or less                                     |
| State if open-source | "Show HN: [Name] - Open-source alternative to X"          |

### Strong Title Examples

```
Show HN: Layerform - Open-source development environments using Terraform files
Show HN: PromptTools - open-source tools for evaluating LLMs and vector DBs
Show HN: Telescope - an open-source web-based log viewer for logs in ClickHouse
```

### Title Mistakes

- Vague descriptions ("A new database tool")
- Superlatives ("fastest," "best," "revolutionary")
- Passive voice ("app that offers")
- Clickbait patterns
- Marketing speak

## First Comment Structure (Critical)

The founding author's first comment seeds the discussion.

### Required 7-Part Structure

1. Personal introduction - Briefly who you are
2. One-sentence definition - What the tool does
3. Problem statement - The pain point you felt
4. Your backstory - Why YOU built this
5. Technical approach - How it works, key decisions
6. What's different - Honest differentiation
7. Invitation for feedback - Ask for specific input

### First Comment Template

```
Hey HN, I'm [name]. I've been working on [project] for [time period].

[One sentence: what it does]

The problem: [Specific pain point you experienced]

I built this because [personal motivation/backstory].

Technically, it [brief architecture/approach]. Key decisions:
- [Decision 1 and why]
- [Decision 2 and why]

What's different from [alternatives]: [honest differentiation]

I'd love feedback on [specific aspect]. What would make this useful for you?

GitHub: [link]
```

### Rules

- Keep it 100-200 words
- Factual, direct language
- Share technical details
- Don't use it for additional promotion

## Link Strategy

Link to GitHub - not a marketing page.

- Signals actual working product
- README becomes your landing page
- HN audience expects to see code

### Access Rules

- Make it trivially easy to try
- No signup required if possible
- Free tier or demo available

## Voice and Tone

### What Works

- First person ("I built", "I noticed")
- Personal backstory
- Technical honesty (challenges, trade-offs, limitations)
- Modest language
- Direct, factual

### What Fails

- Corporate voice or marketing tone
- Superlatives or hype
- Hiding affiliation
- Fake enthusiasm from friends/employees

## Complete Draft Format

```markdown
# Show HN Post

## Title

Show HN: {Product Name} - {clear use-case in under 50 chars}

## Link

{GitHub URL}

---

## First Comment

Hey HN, I'm {name}. I've been working on {project} for {time period}.

{One sentence definition}

**The problem:** {Specific pain point}

I built this because {personal motivation}.

**How it works:** {Brief technical approach}

- {Key design decision 1}
- {Key design decision 2}

**What's different from {alternatives}:** {honest differentiation}

I'd love feedback on {specific aspect}. What would make this useful for you?

---

**Prepared responses for likely questions:**

- Q: {anticipated question 1}
- Q: {anticipated question 2}
- Q: {anticipated question 3}
```

## Common Mistakes That Get Flagged

| Mistake                  | Consequence                       |
| ------------------------ | --------------------------------- |
| Vote manipulation        | Votes don't count; post penalized |
| Hidden affiliation       | Community flames you; lost trust  |
| Marketing/sales language | Ignored by audience               |
| Reposting same link      | Flagged as duplicate              |

## Engagement Strategy

Comments are a stronger ranking signal than upvotes.

### Do

- Respond to every comment
- Go deep into technical details
- Share benchmarks, architecture diagrams
- When criticized, find something to agree with first
- Stay factual and non-defensive

### Don't

- Solicit upvotes
- Get defensive about criticism
- Add promotional top-level comments
- Argue with critics

## Timing

| Time                 | Rationale                            |
| -------------------- | ------------------------------------ |
| Sunday 11am-12pm     | Highest average points               |
| 12:00 UTC            | Catches EU midday + early NA readers |
| 9 AM - 12 PM Pacific | Peak user activity                   |

## HN Post Frontmatter

```yaml
---
channel: "hackernews"
topic: "{topic}"
project: { project }
status: draft
created: { ISO timestamp }
title: "Show HN: {name} - {tagline}"
link_type: github | website
github_url: "{url}"
---
```

## Image Requirements

None. Hacker News is text-only.

## HN Quality Checklist

- [ ] Title starts with "Show HN: " exactly
- [ ] Title tagline is under 50 characters
- [ ] No superlatives or marketing language in title
- [ ] First comment follows the 7-part structure
- [ ] First comment is 100-200 words
- [ ] Technical details included
- [ ] Limitations/trade-offs honestly stated
- [ ] Specific feedback question included
- [ ] Links to GitHub (not landing page)
- [ ] No signup/email gate to try it
- [ ] Voice is personal ("I built") not corporate
- [ ] No asks for upvotes anywhere

## Engagement Preparation

Before posting, prepare:

- [ ] Answers for likely technical questions
- [ ] Benchmarks or examples ready to share
- [ ] Architecture diagrams to paste
- [ ] Responses to common criticisms
- [ ] 2-3 hours blocked to respond immediately
